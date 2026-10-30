import os
try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Error: The 'pillow' library is not installed.")
    print("Please install it by running: pip install pillow")
    exit(1)

def create_shield_icon(size_px, filename):
    # Create dark blue background (#0f172a)
    img = Image.new('RGBA', (size_px, size_px), '#0f172a')
    draw = ImageDraw.Draw(img)
    
    # Calculate shield dimensions proportional to size
    margin = size_px * 0.2
    w = size_px - (margin * 2)
    h = size_px - (margin * 2)
    x = margin
    y = margin
    
    # Shield polygon points
    # Top left to top right, down to the curve, straight to the bottom point, back up
    points = [
        (x, y), 
        (x + w, y), 
        (x + w, y + h * 0.6), 
        (x + w / 2, y + h), 
        (x, y + h * 0.6)
    ]
    
    draw.polygon(points, fill='white')
    
    # Save the file
    img.save(filename, 'PNG')
    print(f"Generated {filename} ({size_px}x{size_px})")

if __name__ == "__main__":
    # Ensure the script runs in its own directory so the icons are placed correctly
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    create_shield_icon(16, "icon16.png")
    create_shield_icon(48, "icon48.png")
    create_shield_icon(128, "icon128.png")
    
    print("\n✓ Placeholder icons successfully generated in the extension/icons/ folder.")
