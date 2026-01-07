let extractedData = [];
let debugInfo = null;

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

    const result = results[0].result;
    extractedData = result.items;
    debugInfo = result.debug;

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
      statusDiv.innerHTML = `
        ✗ No menu items found.<br><br>
        <strong>Debug Info:</strong><br>
        • Found ${debugInfo.elementsChecked} potential elements<br>
        • Price matches: ${debugInfo.priceMatches}<br>
        • Calorie matches: ${debugInfo.calorieMatches}<br>
        • Complete items: ${debugInfo.completeItems}<br><br>
        <strong>Tips:</strong><br>
        • Make sure you're on the menu page<br>
        • Click on menu items to expand details<br>
        • Try clicking "View Menu" or similar buttons<br>
        • Some sites need you to select a date first
      `;

      // Show sample text if available
      if (debugInfo.sampleText) {
        itemListDiv.innerHTML = `<strong>Sample text found on page:</strong><br>
          <div style="font-size:11px; color:#666; max-height:100px; overflow-y:auto;">
            ${debugInfo.sampleText.substring(0, 500)}...
          </div>`;
      }

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
  const debug = {
    elementsChecked: 0,
    priceMatches: 0,
    calorieMatches: 0,
    completeItems: 0,
    sampleText: ''
  };

  // Strategy 1: Try specific Cafe Bon Appetit selectors
  const specificSelectors = [
    'button[class*="menu"]',
    'button[class*="item"]',
    'div[class*="menu-item"]',
    'div[class*="food-item"]',
    'li[class*="item"]',
    '[data-test-id*="menu"]',
    '[data-test-id*="item"]',
    '.c-menu-item',
    '.menu-station-item',
    '.site-panel__daypart-item',
  ];

  let elements = [];

  for (const selector of specificSelectors) {
    try {
      const found = document.querySelectorAll(selector);
      if (found.length > 0) {
        elements = Array.from(found);
        console.log(`Found ${elements.length} elements with selector: ${selector}`);
        break;
      }
    } catch (e) {
      continue;
    }
  }

  // Strategy 2: Look for interactive elements (buttons, links) that might have menu data
  if (elements.length === 0) {
    elements = Array.from(document.querySelectorAll('button, a, li, article, div[role="button"]'));
    elements = elements.filter(el => {
      const text = el.textContent || '';
      // Must have reasonable length and contain either price or calorie info
      return text.length > 10 && text.length < 1000 &&
             (text.includes('$') || text.match(/\d+\s*cal/i));
    });
  }

  // Strategy 3: Broad search - any element with price AND calories
  if (elements.length === 0) {
    elements = Array.from(document.querySelectorAll('*')).filter(el => {
      const text = el.textContent || '';
      return text.length > 10 && text.length < 500 &&
             text.includes('$') &&
             text.match(/\d+\s*cal/i) &&
             el.children.length < 20; // Avoid large containers
    });
  }

  debug.elementsChecked = elements.length;
  debug.sampleText = elements.length > 0 ? elements[0].textContent : document.body.textContent;

  // Process each element
  for (const element of elements) {
    const text = element.textContent || '';
    const html = element.innerHTML || '';

    // Extract name - try multiple strategies
    let name = '';

    // Strategy 1: Look for name in specific elements
    const nameElem = element.querySelector('h1, h2, h3, h4, h5, h6, strong, b, [class*="name"], [class*="title"]');
    if (nameElem && nameElem.textContent.trim().length > 0 && nameElem.textContent.trim().length < 100) {
      name = nameElem.textContent.trim();
    }

    // Strategy 2: Look for aria-label
    if (!name) {
      name = element.getAttribute('aria-label') || element.getAttribute('title') || '';
    }

    // Strategy 3: Get first line of text (before price/calories)
    if (!name) {
      const lines = text.split('\n').map(l => l.trim()).filter(l => l.length > 0);
      for (const line of lines) {
        if (!line.includes('$') && !line.match(/\d+\s*cal/i) && line.length > 3 && line.length < 100) {
          name = line;
          break;
        }
      }
    }

    // Extract price - multiple patterns
    let price = 0;
    const pricePatterns = [
      /\$\s*(\d+\.?\d{0,2})/,           // $5.99
      /(\d+\.?\d{0,2})\s*\$/,           // 5.99$
      /\$(\d+)/,                         // $5
      /price[:\s]+\$?(\d+\.?\d{0,2})/i  // Price: $5.99
    ];

    for (const pattern of pricePatterns) {
      const match = text.match(pattern);
      if (match) {
        const p = parseFloat(match[1]);
        if (p > 0 && p < 100) { // Reasonable price range
          price = p;
          debug.priceMatches++;
          break;
        }
      }
    }

    // Extract calories - multiple patterns
    let calories = 0;
    const caloriePatterns = [
      /(\d+)\s*cal(?:ories)?(?!\w)/i,          // 350 cal, 350 calories
      /(\d+)\s*kcal/i,                         // 350 kcal
      /calories?[:\s]+(\d+)/i,                 // Calories: 350
      /(\d{2,4})\s*(?=cal)/i                   // 350 (before cal)
    ];

    for (const pattern of caloriePatterns) {
      const match = text.match(pattern);
      if (match) {
        const c = parseInt(match[1]);
        if (c >= 10 && c <= 5000) { // Reasonable calorie range
          calories = c;
          debug.calorieMatches++;
          break;
        }
      }
    }

    // Clean up name
    name = name
      .replace(/\s+/g, ' ')
      .replace(/[•·▪▫]/g, '')
      .trim()
      .substring(0, 200);

    // Only add if we have all three pieces
    if (name && name.length > 2 && price > 0 && calories > 0) {
      // Check for duplicates
      const isDuplicate = items.some(item =>
        item.name.toLowerCase() === name.toLowerCase() ||
        (Math.abs(item.price - price) < 0.01 && Math.abs(item.calories - calories) < 10)
      );

      if (!isDuplicate) {
        items.push({ name, price, calories });
        debug.completeItems++;
      }
    }
  }

  // Sort by name for consistency
  items.sort((a, b) => a.name.localeCompare(b.name));

  return { items, debug };
}
