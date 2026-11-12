#!/usr/bin/env python3
"""Generates every bitmap asset of the Neon Beach watch face.

All artwork is original and procedurally drawn (gradients, grid, sun, palms),
so the project carries no third-party imagery.

Outputs:
  app/src/main/res/drawable-nodpi/  backgrounds, option icons, preview
  app/src/main/res/mipmap-*/        launcher icon
  store-listing/                    Play Store icon, feature graphic, screenshots

Run from the watchface/ directory:  python3 tools/generate_assets.py
Requires Pillow.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "app", "src", "main", "res")
DRAWABLE = os.path.join(RES, "drawable-nodpi")
STORE = os.path.join(ROOT, "store-listing")
FONT_BOLD = os.path.join(RES, "font", "orbitron_bold.ttf")
FONT_MED = os.path.join(RES, "font", "orbitron_medium.ttf")

SIZE = 450          # Watch Face Format canvas
SS = 4              # supersampling factor
HORIZON = 270

# Must stay in sync with the ColorConfiguration in res/raw/watchface.xml
THEMES = [
    ("neon_rosa", "#FF3D9A", "#00E5FF"),
    ("ciano", "#00E5FF", "#FF3D9A"),
    ("dourado", "#FFC23D", "#FF3D9A"),
    ("branco", "#FFFFFF", "#00E5FF"),
    ("verde", "#39FF88", "#FFC23D"),
]

SCENES = {
    "sunset": {
        "sky": [(0, "#07011A"), (150, "#1E0640"), (215, "#4A0D5E"), (250, "#B02A6E"), (270, "#FF7A3D")],
        "ground": ("#24063F", "#050010"),
        "sun": ("#FFE45C", "#FF2E88"),
        "grid": "#FF3D9A",
        "stars": 40,
        "palm": "#06000E",
    },
    "night": {
        "sky": [(0, "#01010A"), (150, "#060C2E"), (220, "#0F1F5C"), (255, "#2A2E8C"), (270, "#5B3FB8")],
        "ground": ("#0A0F33", "#020208"),
        "sun": ("#E8FBFF", "#6FD6FF"),
        "grid": "#00E5FF",
        "stars": 140,
        "palm": "#000004",
    },
}


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(len(a)))


def vertical_gradient(w, h, stops):
    """stops: list of (y_in_450_space, hex) mapped onto height h."""
    img = Image.new("RGB", (w, h))
    px = img.load()
    scale = h / stops[-1][0] if stops[-1][0] else 1
    pts = [(y * scale, hex_rgb(c)) for y, c in stops]
    for y in range(h):
        for i in range(len(pts) - 1):
            y0, c0 = pts[i]
            y1, c1 = pts[i + 1]
            if y0 <= y <= y1 or i == len(pts) - 2:
                t = 0 if y1 == y0 else min(max((y - y0) / (y1 - y0), 0), 1)
                c = lerp(c0, c1, t)
                break
        for x in range(w):
            px[x, y] = c
    return img


def draw_palm(draw, base, top, scale, color):
    """Draws a palm silhouette (coordinates in supersampled space)."""
    bx, by = base
    tx, ty = top
    # curved, tapering trunk
    segs = 40
    pts_l, pts_r = [], []
    for i in range(segs + 1):
        t = i / segs
        cx = bx + (tx - bx) * t + math.sin(t * math.pi) * 18 * scale * (1 if tx > bx else -1)
        cy = by + (ty - by) * t
        wdt = (13 - 8 * t) * scale
        pts_l.append((cx - wdt, cy))
        pts_r.append((cx + wdt, cy))
    draw.polygon(pts_l + pts_r[::-1], fill=color)
    # trunk rings are implied by the silhouette; now the fronds
    fronds = [(-170, 1.0), (-145, 1.1), (-120, 0.9), (-60, 0.9), (-35, 1.1), (-10, 1.0), (-90, 0.7), (160, 0.6), (20, 0.6)]
    for ang, ln in fronds:
        a = math.radians(ang)
        length = 95 * scale * ln
        spts_top, spts_bot = [], []
        n = 24
        for i in range(n + 1):
            t = i / n
            # leaf droops with gravity
            px = tx + math.cos(a) * length * t
            py = ty + math.sin(a) * length * t + (length * 0.55) * t * t
            thick = math.sin(t * math.pi) * 13 * scale * ln
            nx, ny = -math.sin(a), math.cos(a)
            spts_top.append((px + nx * thick * 0.35, py + ny * thick * 0.35 - thick * 0.65))
            spts_bot.append((px - nx * thick * 0.35, py - ny * thick * 0.35 + thick * 0.35))
        draw.polygon(spts_top + spts_bot[::-1], fill=color)
        # serrated leaflets along the frond
        for i in range(3, n - 1, 2):
            t = i / n
            px = tx + math.cos(a) * length * t
            py = ty + math.sin(a) * length * t + (length * 0.55) * t * t
            lf = (1 - t) * 18 * scale * ln + 4 * scale
            draw.line([(px, py), (px + math.cos(a + 0.9) * lf, py + math.sin(a + 0.9) * lf + lf * 0.6)],
                      fill=color, width=int(3 * scale))
            draw.line([(px, py), (px + math.cos(a - 0.9) * lf * 0.7, py + math.sin(a - 0.9) * lf * 0.7 + lf * 0.5)],
                      fill=color, width=int(3 * scale))
    draw.ellipse([tx - 10 * scale, ty - 8 * scale, tx + 10 * scale, ty + 8 * scale], fill=color)


def render_background(scene_name, size=SIZE):
    sc = SCENES[scene_name]
    S = size * SS
    k = S / SIZE  # 450-space -> supersampled
    hz = int(HORIZON * k)
    rnd = random.Random(42 if scene_name == "sunset" else 7)

    img = Image.new("RGB", (S, S), "black")
    sky = vertical_gradient(1, hz, sc["sky"]).resize((S, hz))
    img.paste(sky, (0, 0))
    ground = vertical_gradient(1, S - hz, [(0, sc["ground"][0]), (1, sc["ground"][1])]).resize((S, S - hz))
    img.paste(ground, (0, hz))

    # stars
    d = ImageDraw.Draw(img, "RGBA")
    for _ in range(sc["stars"]):
        x = rnd.uniform(0, S)
        y = rnd.uniform(0, hz * 0.75)
        r = rnd.uniform(0.6, 1.8) * k
        a = int(rnd.uniform(60, 220) * (1 - y / hz))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, a))

    # sun / moon glow
    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    cx, cy, r = 225 * k, HORIZON * k, 84 * k
    gc = hex_rgb(sc["sun"][1])
    gd.ellipse([cx - r * 1.5, cy - r * 1.5, cx + r * 1.5, cy + r * 1.5], fill=gc + (110,))
    glow = glow.filter(ImageFilter.GaussianBlur(28 * k))
    img.paste(glow, (0, 0), glow)

    # striped sun
    sun = vertical_gradient(1, int(2 * r), [(0, sc["sun"][0]), (1, sc["sun"][1])]).resize((int(2 * r), int(2 * r)))
    mask = Image.new("L", sun.size, 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([0, 0, sun.size[0] - 1, sun.size[1] - 1], fill=255)
    # horizontal cut-outs that grow toward the horizon
    for i, frac in enumerate([0.52, 0.64, 0.75, 0.85, 0.94]):
        y = frac * r
        hgt = (2 + i * 2.2) * k
        md.rectangle([0, y, sun.size[0], y + hgt], fill=0)
    md.rectangle([0, r, sun.size[0], sun.size[1]], fill=0)  # below horizon
    img.paste(sun, (int(cx - r), int(cy - r)), mask)

    # perspective grid on the ground
    grid = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grid)
    gcol = hex_rgb(sc["grid"])
    for i in range(1, 12):
        t = (i / 11) ** 2.1
        y = hz + t * (S - hz)
        gdraw.line([(0, y), (S, y)], fill=gcol + (int(70 + 120 * t),), width=max(1, int(1.6 * k)))
    vx = cx
    for i in range(-14, 15):
        x_bottom = vx + i * 60 * k
        gdraw.line([(vx + i * 6 * k, hz), (x_bottom, S)], fill=gcol + (140,), width=max(1, int(1.5 * k)))
    blur = grid.filter(ImageFilter.GaussianBlur(3 * k))
    img.paste(blur, (0, 0), blur)
    img.paste(grid, (0, 0), grid)

    # horizon line
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(0, hz), (S, hz)], fill=gcol + (255,), width=int(2 * k))

    # palms
    draw_palm(d, (38 * k, 470 * k), (78 * k, 222 * k), k, hex_rgb(sc["palm"]))
    draw_palm(d, (420 * k, 470 * k), (378 * k, 240 * k), k * 0.85, hex_rgb(sc["palm"]))

    # 12 hour dots near the bezel
    for h in range(12):
        a = math.radians(h * 30 - 90)
        rr = 205 * k
        x, y = 225 * k + math.cos(a) * rr, 225 * k + math.sin(a) * rr
        dot = (3.2 if h % 3 == 0 else 2.0) * k
        d.ellipse([x - dot, y - dot, x + dot, y + dot], fill=(255, 255, 255, 200 if h % 3 == 0 else 120))

    return img.resize((size, size), Image.LANCZOS)


def circle_mask(size):
    m = Image.new("L", (size * SS, size * SS), 0)
    ImageDraw.Draw(m).ellipse([0, 0, size * SS - 1, size * SS - 1], fill=255)
    return m.resize((size, size), Image.LANCZOS)


def text_center(d, cx, cy, text, font, fill):
    l, t, r, b = d.textbbox((0, 0), text, font=font)
    d.text((cx - (l + r) / 2, cy - (t + b) / 2), text, font=font, fill=fill)


def neon_text(img, cx, cy, text, font, color):
    # Plain fill only, so the preview matches what the watch draws.
    text_center(ImageDraw.Draw(img), cx, cy, text, font, hex_rgb(color) + (255,))


def date_row(d, day, date, font, fill):
    """Day of week right-aligned to x=218, date left-aligned from x=232 (see watchface.xml)."""
    l, t, r, b = d.textbbox((0, 0), day, font=font)
    d.text((218 - r, 79 - (t + b) / 2), day, font=font, fill=fill)
    l, t, r, b = d.textbbox((0, 0), date, font=font)
    d.text((232 - l, 79 - (t + b) / 2), date, font=font, fill=fill)


def icon_steps(d, cx, cy, col):
    for dx, dy in ((-5, 2), (5, -4)):
        d.ellipse([cx + dx - 4, cy + dy - 7, cx + dx + 4, cy + dy + 5], fill=col)
        d.ellipse([cx + dx - 3, cy + dy + 6, cx + dx + 3, cy + dy + 10], fill=col)


def icon_battery(d, cx, cy, col):
    d.rounded_rectangle([cx - 11, cy - 6, cx + 9, cy + 6], 2, outline=col, width=2)
    d.rectangle([cx + 10, cy - 3, cx + 12, cy + 3], fill=col)
    d.rectangle([cx - 8, cy - 3, cx + 4, cy + 3], fill=col)


def render_face(scene, theme_idx, ambient=False, time="10:08", day="QUA", date="12.11", second=32):
    _, primary, secondary = THEMES[theme_idx]
    font_time = ImageFont.truetype(FONT_BOLD, 96)
    font_date = ImageFont.truetype(FONT_MED, 22)
    font_comp = ImageFont.truetype(FONT_MED, 22)
    if ambient:
        img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 255))
        d = ImageDraw.Draw(img)
        date_row(d, day, date, font_date, (170, 170, 170, 255))
        text_center(d, 225, 150, time, ImageFont.truetype(FONT_MED, 96), (200, 200, 200, 255))
    else:
        img = render_background(scene).convert("RGBA")
        d = ImageDraw.Draw(img, "RGBA")
        # seconds ring: track + progress (matches PartDraw/Arc in watchface.xml)
        ring = Image.new("RGBA", (SIZE * SS, SIZE * SS), (0, 0, 0, 0))
        rd = ImageDraw.Draw(ring)
        box = [7 * SS, 7 * SS, 443 * SS, 443 * SS]
        rd.ellipse(box, outline=(255, 255, 255, 40), width=3 * SS)
        rd.arc(box, -90, -90 + second * 6, fill=hex_rgb(secondary) + (255,), width=6 * SS)
        img.alpha_composite(ring.resize((SIZE, SIZE), Image.LANCZOS))
        d = ImageDraw.Draw(img, "RGBA")
        date_row(d, day, date, font_date, hex_rgb(secondary) + (255,))
        neon_text(img, 225, 150, time, font_time, primary)
        d = ImageDraw.Draw(img, "RGBA")
        # complications
        for cx, val, icon in ((160, "4218", icon_steps), (290, "85%", icon_battery)):
            d.ellipse([cx - 46, 336 - 46, cx + 46, 336 + 46], fill=(5, 0, 16, 170),
                      outline=hex_rgb(secondary) + (180,), width=2)
            icon(d, cx, 316, hex_rgb(primary) + (255,))
            text_center(d, cx, 348, val, font_comp, (255, 255, 255, 255))
    out = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    out.paste(img, (0, 0), circle_mask(SIZE))
    return out


def save(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, optimize=True)
    print("wrote", os.path.relpath(path, ROOT))


def launcher_icon(size):
    bg = render_background("sunset", 450).crop((105, 120, 345, 360)).resize((size, size), Image.LANCZOS)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(bg, (0, 0), circle_mask(size))
    return out


def main():
    for scene in SCENES:
        bg = render_background(scene)
        save(bg, os.path.join(DRAWABLE, f"bg_{scene}.png"))
        icon = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
        icon.paste(bg.resize((96, 96), Image.LANCZOS), (0, 0), circle_mask(96))
        save(icon, os.path.join(DRAWABLE, f"ic_option_{scene}.png"))

    save(render_face("sunset", 0), os.path.join(DRAWABLE, "preview.png"))

    for name, px in (("mdpi", 48), ("hdpi", 72), ("xhdpi", 96), ("xxhdpi", 144), ("xxxhdpi", 192)):
        save(launcher_icon(px), os.path.join(RES, f"mipmap-{name}", "ic_launcher.png"))

    # --- Play Store assets ---
    icon512 = Image.new("RGBA", (512, 512), (7, 1, 26, 255))
    icon512.alpha_composite(launcher_icon(512))
    save(icon512.convert("RGB"), os.path.join(STORE, "icon-512.png"))

    feature = Image.new("RGB", (1024, 500))
    bgwide = render_background("sunset", 1024).crop((0, 262, 1024, 762))
    feature.paste(bgwide, (0, 0))
    fd = ImageDraw.Draw(feature)
    face = render_face("night", 1).resize((400, 400), Image.LANCZOS)
    feature.paste(face, (580, 50), face)
    title_font = ImageFont.truetype(FONT_BOLD, 64)
    sub_font = ImageFont.truetype(FONT_MED, 28)
    shadow = Image.new("RGBA", feature.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.text((60, 150), "NEON", font=title_font, fill=(255, 61, 154, 220))
    sd.text((60, 225), "BEACH", font=title_font, fill=(0, 229, 255, 220))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
    feature = feature.convert("RGBA")
    feature.alpha_composite(shadow)
    fd = ImageDraw.Draw(feature)
    fd.text((60, 150), "NEON", font=title_font, fill=(255, 140, 200))
    fd.text((60, 225), "BEACH", font=title_font, fill=(170, 245, 255))
    fd.text((62, 315), "Mostrador retrô para Wear OS", font=sub_font, fill=(255, 255, 255))
    save(feature.convert("RGB"), os.path.join(STORE, "feature-graphic-1024x500.png"))

    shots = [
        ("01-por-do-sol-rosa", "sunset", 0, False, "10:08", "QUA", "12.11", 32),
        ("02-noite-ciano", "night", 1, False, "21:47", "SEX", "14.11", 15),
        ("03-por-do-sol-dourado", "sunset", 2, False, "07:30", "SÁB", "15.11", 48),
        ("04-noite-verde", "night", 4, False, "23:59", "DOM", "16.11", 55),
        ("05-modo-ambiente", "sunset", 0, True, "10:08", "QUA", "12.11", 0),
    ]
    for name, scene, theme, amb, t, dy, dt, s in shots:
        face = render_face(scene, theme, amb, t, dy, dt, s)
        # Play requires opaque 1:1 screenshots of at least 384x384; 900x900 here.
        canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 255))
        canvas.alpha_composite(face)
        save(canvas.resize((900, 900), Image.LANCZOS).convert("RGB"),
             os.path.join(STORE, "screenshots", f"{name}.png"))


if __name__ == "__main__":
    main()
