#!/usr/bin/env python3
"""
Create simple icon placeholders for the browser extension
Run this once to generate icon files
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("PIL not available. Creating placeholder files...")

def create_icon(size, filename):
    """Create a simple icon"""
    if HAS_PIL:
        # Create image with PIL
        img = Image.new('RGB', (size, size), color='#3498db')
        draw = ImageDraw.Draw(img)

        # Draw a simple fork/knife icon representation (just circles for simplicity)
        center = size // 2
        radius = size // 3
        draw.ellipse([center - radius, center - radius,
                     center + radius, center + radius],
                    fill='white')

        img.save(filename, 'PNG')
        print(f"Created {filename}")
    else:
        # Create minimal valid PNG file
        # 1x1 blue pixel
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xa8\xc0\xc0\xc0\x00\x00\x00\x04\x00\x01\xa7\xd8r\xcb\x00\x00\x00\x00IEND\xaeB`\x82'

        with open(filename, 'wb') as f:
            f.write(png_data)
        print(f"Created placeholder {filename}")

if __name__ == '__main__':
    import os
    os.chdir(os.path.dirname(__file__))

    create_icon(16, 'icon16.png')
    create_icon(48, 'icon48.png')
    create_icon(128, 'icon128.png')

    print("\n✓ Icons created!")
    print("Note: These are simple placeholders. You can replace them with custom icons.")
