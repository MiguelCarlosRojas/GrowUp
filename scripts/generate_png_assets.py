import os
from PIL import Image, ImageDraw, ImageFont

def create_super_logo():
    # 4x Supersampling for ultra-crisp edges
    scale = 4
    w, h = 760 * scale, 160 * scale
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Fonts
    font_bold = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 72 * scale)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 20 * scale)

    # Draw Emblem on the Left (center around x=100*scale, y=80*scale)
    cx, cy = 95 * scale, 80 * scale
    r = 54 * scale

    # Modern Glowing Emblem: Hexagonal rounded badge with layered wings and play-portal
    # Outer rounded polygon/circle glow
    for dr in range(8 * scale, 0, -1):
        alpha = int(18 * (1 - dr / (8 * scale)))
        draw.ellipse([cx - r - dr, cy - r - dr, cx + r + dr, cy + r + dr], fill=(255, 42, 84, alpha))

    # Base emblem badge: rounded rect/pill
    badge_box = [cx - r, cy - r, cx + r, cy + r]
    draw.rounded_rectangle(badge_box, radius=18 * scale, fill=(18, 22, 34, 255), outline=(255, 42, 84, 220), width=4 * scale)

    # Stylized Geometric 'G' / Portal wings
    # Left vertical stem & top/bottom arcs
    draw.arc([cx - 36 * scale, cy - 36 * scale, cx + 36 * scale, cy + 36 * scale], start=45, end=315, fill=(255, 60, 95, 255), width=8 * scale)
    # Right inner crossbar
    draw.line([cx - 4 * scale, cy + 4 * scale, cx + 24 * scale, cy + 4 * scale], fill=(255, 110, 60, 255), width=8 * scale)
    draw.line([cx + 20 * scale, cy + 4 * scale, cx + 20 * scale, cy + 24 * scale], fill=(255, 110, 60, 255), width=8 * scale)
    # Forward glowing accent triangle (Play / Fast-forward arrow inside)
    triangle = [
        (cx - 8 * scale, cy - 14 * scale),
        (cx - 8 * scale, cy + 2 * scale),
        (cx + 8 * scale, cy - 6 * scale)
    ]
    draw.polygon(triangle, fill=(255, 255, 255, 255))

    # Text: "GROW" in Pure White
    text_x = 180 * scale
    text_y = 30 * scale
    draw.text((text_x, text_y), "GROW", font=font_bold, fill=(255, 255, 255, 255))

    # Get width of "GROW"
    bbox_grow = draw.textbbox((text_x, text_y), "GROW", font=font_bold)
    up_x = bbox_grow[2] + 4 * scale

    # Text: "UP" in Coral Crimson Gradient
    draw.text((up_x, text_y), "UP", font=font_bold, fill=(255, 51, 88, 255))

    # Subtitle: "MANGA • ANIME • NOVELAS"
    sub_y = text_y + 78 * scale
    draw.text((text_x + 2 * scale, sub_y), "MANGA  •  ANIME  •  NOVELAS LIGERAS", font=font_sub, fill=(156, 163, 175, 230))

    # Downscale with LANCZOS for super clean anti-aliasing
    final_img = img.resize((760, 160), Image.Resampling.LANCZOS)
    os.makedirs('static/images', exist_ok=True)
    final_img.save('static/images/logo.png', 'PNG')
    print("Saved static/images/logo.png successfully!")

def create_super_favicon():
    scale = 4
    size = 128 * scale
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = size // 2, size // 2
    r = 50 * scale

    # Outer glow
    for dr in range(6 * scale, 0, -1):
        alpha = int(22 * (1 - dr / (6 * scale)))
        draw.ellipse([cx - r - dr, cy - r - dr, cx + r + dr, cy + r + dr], fill=(255, 42, 84, alpha))

    # Background rounded container
    draw.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], radius=16 * scale, fill=(14, 18, 28, 255), outline=(255, 42, 84, 230), width=4 * scale)

    # Stylized G arc
    draw.arc([cx - 32 * scale, cy - 32 * scale, cx + 32 * scale, cy + 32 * scale], start=45, end=315, fill=(255, 60, 95, 255), width=8 * scale)
    # Crossbar
    draw.line([cx - 2 * scale, cy + 4 * scale, cx + 22 * scale, cy + 4 * scale], fill=(255, 110, 60, 255), width=8 * scale)
    draw.line([cx + 18 * scale, cy + 4 * scale, cx + 18 * scale, cy + 22 * scale], fill=(255, 110, 60, 255), width=8 * scale)
    # Play arrow
    triangle = [
        (cx - 6 * scale, cy - 12 * scale),
        (cx - 6 * scale, cy + 2 * scale),
        (cx + 8 * scale, cy - 5 * scale)
    ]
    draw.polygon(triangle, fill=(255, 255, 255, 255))

    final_ico = img.resize((128, 128), Image.Resampling.LANCZOS)
    final_ico.save('static/images/favicon.png', 'PNG')
    final_ico.save('static/images/logo-icon.png', 'PNG')
    print("Saved static/images/favicon.png and logo-icon.png successfully!")

if __name__ == '__main__':
    create_super_logo()
    create_super_favicon()
