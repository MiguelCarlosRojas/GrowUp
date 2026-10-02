import os
from PIL import Image, ImageDraw, ImageFont

def create_super_logo():
    # 4x Supersampling for ultra-crisp edges
    scale = 4
    w, h = 960 * scale, 220 * scale
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Fonts
    font_bold = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 100 * scale)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 26 * scale)

    # Draw Emblem on the Left (center around x=120*scale, y=110*scale)
    cx, cy = 125 * scale, 110 * scale
    r = 74 * scale

    # Modern Glowing Emblem: Hexagonal rounded badge with layered wings and play-portal
    for dr in range(12 * scale, 0, -1):
        alpha = int(22 * (1 - dr / (12 * scale)))
        draw.ellipse([cx - r - dr, cy - r - dr, cx + r + dr, cy + r + dr], fill=(255, 42, 84, alpha))

    # Base emblem badge: rounded rect
    badge_box = [cx - r, cy - r, cx + r, cy + r]
    draw.rounded_rectangle(badge_box, radius=24 * scale, fill=(18, 24, 38, 255), outline=(255, 42, 84, 230), width=5 * scale)

    # Stylized Geometric 'G' / Portal wings
    draw.arc([cx - 50 * scale, cy - 50 * scale, cx + 50 * scale, cy + 50 * scale], start=45, end=315, fill=(255, 60, 95, 255), width=10 * scale)
    # Crossbar
    draw.line([cx - 6 * scale, cy + 6 * scale, cx + 32 * scale, cy + 6 * scale], fill=(255, 110, 60, 255), width=10 * scale)
    draw.line([cx + 28 * scale, cy + 6 * scale, cx + 28 * scale, cy + 32 * scale], fill=(255, 110, 60, 255), width=10 * scale)
    
    # Forward glowing accent triangle
    triangle = [
        (cx - 10 * scale, cy - 20 * scale),
        (cx - 10 * scale, cy + 4 * scale),
        (cx + 12 * scale, cy - 8 * scale)
    ]
    draw.polygon(triangle, fill=(255, 255, 255, 255))

    # Text: "GROW" in Pure White
    text_x = 230 * scale
    text_y = 35 * scale
    draw.text((text_x, text_y), "GROW", font=font_bold, fill=(255, 255, 255, 255))

    # Get width of "GROW"
    bbox_grow = draw.textbbox((text_x, text_y), "GROW", font=font_bold)
    up_x = bbox_grow[2] + 6 * scale

    # Text: "UP" in Coral Crimson Gradient
    draw.text((up_x, text_y), "UP", font=font_bold, fill=(255, 51, 88, 255))

    # Subtitle: "MANGA • ANIME • NOVELAS LIGERAS"
    sub_y = text_y + 112 * scale
    draw.text((text_x + 4 * scale, sub_y), "MANGA   •   ANIME   •   NOVELAS LIGERAS", font=font_sub, fill=(156, 163, 175, 240))

    # Downscale with LANCZOS for super clean anti-aliasing
    final_img = img.resize((960, 220), Image.Resampling.LANCZOS)
    os.makedirs('static/images', exist_ok=True)
    final_img.save('static/images/logo.png', 'PNG')
    print("Saved static/images/logo.png (large high-res) successfully!")

def create_super_favicon():
    scale = 4
    size = 256 * scale
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = size // 2, size // 2
    r = 100 * scale

    # Outer glow
    for dr in range(12 * scale, 0, -1):
        alpha = int(24 * (1 - dr / (12 * scale)))
        draw.ellipse([cx - r - dr, cy - r - dr, cx + r + dr, cy + r + dr], fill=(255, 42, 84, alpha))

    # Background rounded container
    draw.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], radius=32 * scale, fill=(14, 18, 28, 255), outline=(255, 42, 84, 240), width=8 * scale)

    # Stylized G arc
    draw.arc([cx - 64 * scale, cy - 64 * scale, cx + 64 * scale, cy + 64 * scale], start=45, end=315, fill=(255, 60, 95, 255), width=16 * scale)
    # Crossbar
    draw.line([cx - 6 * scale, cy + 8 * scale, cx + 44 * scale, cy + 8 * scale], fill=(255, 110, 60, 255), width=16 * scale)
    draw.line([cx + 36 * scale, cy + 8 * scale, cx + 36 * scale, cy + 44 * scale], fill=(255, 110, 60, 255), width=16 * scale)
    
    # Play arrow
    triangle = [
        (cx - 12 * scale, cy - 24 * scale),
        (cx - 12 * scale, cy + 4 * scale),
        (cx + 16 * scale, cy - 10 * scale)
    ]
    draw.polygon(triangle, fill=(255, 255, 255, 255))

    final_ico = img.resize((256, 256), Image.Resampling.LANCZOS)
    final_ico.save('static/images/favicon.png', 'PNG')
    final_ico.save('static/images/logo-icon.png', 'PNG')
    print("Saved static/images/favicon.png (large 256x256) successfully!")

if __name__ == '__main__':
    create_super_logo()
    create_super_favicon()
