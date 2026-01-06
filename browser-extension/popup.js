let extractedData = [];

document.getElementById('extractBtn').addEventListener('click', async () => {
  const statusDiv = document.getElementById('status');
  const itemListDiv = document.getElementById('itemList');
  const downloadBtn = document.getElementById('downloadBtn');

  statusDiv.style.display = 'block';
  statusDiv.className = 'info';
  statusDiv.textContent = 'Extracting menu data...';

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: extractMenuData
    });

    extractedData = results[0].result;

    if (extractedData && extractedData.length > 0) {
      statusDiv.className = 'success';
      statusDiv.textContent = `✓ Found ${extractedData.length} menu items!`;

      // Display items
      itemListDiv.innerHTML = '<strong>Items found:</strong><br>' +
        extractedData.map(item =>
          `<div class="item">${item.name} - $${item.price} - ${item.calories} cal</div>`
        ).join('');

      downloadBtn.style.display = 'block';
    } else {
      statusDiv.className = 'error';
      statusDiv.textContent = '✗ No menu items found. Try navigating to the menu page.';
      itemListDiv.innerHTML = '';
      downloadBtn.style.display = 'none';
    }
  } catch (error) {
    statusDiv.className = 'error';
    statusDiv.textContent = '✗ Error: ' + error.message;
    console.error(error);
  }
});

document.getElementById('downloadBtn').addEventListener('click', () => {
  if (extractedData.length === 0) return;

  const dataStr = JSON.stringify(extractedData, null, 2);
  const blob = new Blob([dataStr], { type: 'application/json' });
  const url = URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.href = url;
  a.download = `menu_data_${new Date().toISOString().split('T')[0]}.json`;
  a.click();

  URL.revokeObjectURL(url);

  document.getElementById('status').textContent = '✓ Downloaded menu_data.json!';
});

// This function runs in the context of the web page
function extractMenuData() {
  const items = [];

  // Strategy 1: Look for common menu item patterns
  const selectors = [
    '.menu-item',
    '.food-item',
    '.item',
    '[data-name]',
    '.site-panel__daypart-item',
    '.nutrition-item',
    'article',
    '.station-item'
  ];

  let elements = [];
  for (const selector of selectors) {
    const found = document.querySelectorAll(selector);
    if (found.length > 0) {
      elements = Array.from(found);
      break;
    }
  }

  // If no specific elements found, try all divs with enough content
  if (elements.length === 0) {
    elements = Array.from(document.querySelectorAll('div')).filter(div => {
      const text = div.textContent || '';
      return text.includes('$') && (text.includes('cal') || text.includes('Cal'));
    });
  }

  for (const element of elements) {
    const text = element.textContent || '';

    // Extract name
    let name = '';
    const nameElem = element.querySelector('h2, h3, h4, .name, .title, [data-name]');
    if (nameElem) {
      name = nameElem.textContent.trim();
    } else {
      // Use first significant text
      const firstText = element.querySelector('span, div, p');
      if (firstText) name = firstText.textContent.trim();
    }

    // Extract price
    const priceMatch = text.match(/\$\s*(\d+\.?\d*)/);
    const price = priceMatch ? parseFloat(priceMatch[1]) : 0;

    // Extract calories
    const calMatch = text.match(/(\d+)\s*(cal|kcal|calories)/i);
    const calories = calMatch ? parseInt(calMatch[1]) : 0;

    // Only add if we have all three pieces of data
    if (name && price > 0 && calories > 0) {
      // Avoid duplicates
      if (!items.some(item => item.name === name)) {
        items.push({ name, price, calories });
      }
    }
  }

  return items;
}
