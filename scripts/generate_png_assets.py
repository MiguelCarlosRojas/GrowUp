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

    # Draw Emblem on the Left (center around x=125*scale, y=110*scale)
    cx, cy = 125 * scale, 110 * scale
    r = 82 * scale

    # Modern Glowing Emblem: Hexagonal rounded badge with layered wings and play-portal
    for dr in range(12 * scale, 0, -1):
        alpha = int(24 * (1 - dr / (12 * scale)))
        draw.ellipse([cx - r - dr, cy - r - dr, cx + r + dr, cy + r + dr], fill=(255, 42, 84, alpha))

    # Base emblem badge: rounded rect
    badge_box = [cx - r, cy - r, cx + r, cy + r]
    draw.rounded_rectangle(badge_box, radius=24 * scale, fill=(18, 24, 38, 255), outline=(255, 42, 84, 240), width=6 * scale)

    # Stylized Geometric 'G' / Portal wings
    draw.arc([cx - 56 * scale, cy - 56 * scale, cx + 56 * scale, cy + 56 * scale], start=45, end=315, fill=(255, 60, 95, 255), width=12 * scale)
    # Crossbar
    draw.line([cx - 8 * scale, cy + 8 * scale, cx + 38 * scale, cy + 8 * scale], fill=(255, 110, 60, 255), width=12 * scale)
    draw.line([cx + 34 * scale, cy + 8 * scale, cx + 34 * scale, cy + 38 * scale], fill=(255, 110, 60, 255), width=12 * scale)
    
    # Forward glowing accent triangle
    triangle = [
        (cx - 12 * scale, cy - 22 * scale),
        (cx - 12 * scale, cy + 6 * scale),
        (cx + 14 * scale, cy - 8 * scale)
    ]
    draw.polygon(triangle, fill=(255, 255, 255, 255))

    # Text: "GROW" in Pure White
    text_x = 236 * scale
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
    print("Saved static/images/logo.png successfully!")

def create_super_favicon():
    # Make the favicon fill the canvas completely (no excessive empty margins)
    scale = 4
    size = 256 * scale
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = size // 2, size // 2
    # Radius nearly fills 256*4 (leaving just 4px margin for outer glow)
    r = 122 * scale

    # Subtle outer rim glow
    for dr in range(6 * scale, 0, -1):
        alpha = int(28 * (1 - dr / (6 * scale)))
        draw.rounded_rectangle([cx - r - dr, cy - r - dr, cx + r + dr, cy + r + dr], radius=36 * scale, fill=(255, 42, 84, alpha))

    # Background rounded container filling the canvas
    draw.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], radius=32 * scale, fill=(14, 18, 28, 255), outline=(255, 42, 84, 255), width=10 * scale)

    # Stylized G arc (prominently large)
    draw.arc([cx - 78 * scale, cy - 78 * scale, cx + 78 * scale, cy + 78 * scale], start=45, end=315, fill=(255, 60, 95, 255), width=22 * scale)
    # Crossbar
    draw.line([cx - 10 * scale, cy + 10 * scale, cx + 52 * scale, cy + 10 * scale], fill=(255, 110, 60, 255), width=22 * scale)
    draw.line([cx + 42 * scale, cy + 10 * scale, cx + 42 * scale, cy + 54 * scale], fill=(255, 110, 60, 255), width=22 * scale)
    
    # Play arrow
    triangle = [
        (cx - 16 * scale, cy - 30 * scale),
        (cx - 16 * scale, cy + 6 * scale),
        (cx + 20 * scale, cy - 12 * scale)
    ]
    draw.polygon(triangle, fill=(255, 255, 255, 255))

    # Save 256x256
    final_256 = img.resize((256, 256), Image.Resampling.LANCZOS)
    final_256.save('static/images/favicon.png', 'PNG')
    final_256.save('static/images/logo-icon.png', 'PNG')

    # Save 32x32 & 16x16 for crisp browser tabs
    final_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
    final_32.save('static/images/favicon-32x32.png', 'PNG')

    final_16 = img.resize((16, 16), Image.Resampling.LANCZOS)
    final_16.save('static/images/favicon-16x16.png', 'PNG')

    # Multi-resolution .ico file (direct root & static/images)
    final_256.save('static/favicon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    final_256.save('static/images/favicon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("Saved ultra-large edge-to-edge favicon set (PNG + multi-res ICO) successfully!")

if __name__ == '__main__':
    create_super_logo()
    create_super_favicon()
