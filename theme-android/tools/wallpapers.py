"""Gera os wallpapers do Neon Shore (arte original, procedural).

Uso: python3 tools/wallpapers.py  (a partir de theme-android/)
"""
import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

WIDTH, HEIGHT = 1440, 3200
OUT = os.path.join(os.path.dirname(__file__), "..", "app", "src", "main", "res", "drawable-nodpi")
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"


def vgrad(w, h, stops):
    """Gradiente vertical com várias paradas [(pos, (r,g,b)), ...]."""
    ys = np.linspace(0, 1, h)
    out = np.zeros((h, w, 3), dtype=np.float32)
    for c in range(3):
        col = np.interp(ys, [s[0] for s in stops], [s[1][c] for s in stops])
        out[:, :, c] = col[:, None]
    return Image.fromarray(out.astype(np.uint8))


def add(img, layer, amount=1.0):
    a = np.asarray(img, dtype=np.float32)
    b = np.asarray(layer.convert("RGB"), dtype=np.float32)
    return Image.fromarray(np.clip(a + b * amount, 0, 255).astype(np.uint8))


def glow_shape(size, draw_fn, color, blur):
    m = Image.new("L", size, 0)
    draw_fn(ImageDraw.Draw(m))
    m = m.filter(ImageFilter.GaussianBlur(blur))
    col = Image.new("RGB", size, color)
    black = Image.new("RGB", size, (0, 0, 0))
    return Image.composite(col, black, m)


def stars(img, n, seed, top=0.0, bottom=0.5):
    rnd = random.Random(seed)
    d = ImageDraw.Draw(img)
    w, h = img.size
    for _ in range(n):
        x, y = rnd.uniform(0, w), rnd.uniform(top * h, bottom * h)
        r = rnd.choice([1.2, 1.6, 2.2, 3.0])
        b = rnd.randint(150, 255)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(b, b, min(255, b + 20)))
    return img


def striped_sun(img, cx, cy, r, top=(255, 230, 90), bottom=(255, 40, 140), gaps=7):
    w, h = img.size
    sun = vgrad(int(2 * r), int(2 * r), [(0, top), (1, bottom)])
    mask = Image.new("L", sun.size, 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=255)
    # faixas horizontais recortadas na metade inferior (estética retrô)
    for i in range(gaps):
        t = 0.52 + i * 0.07
        y = t * 2 * r
        th = 6 + i * 5
        md.rectangle([0, y, 2 * r, y + th], fill=0)
    halo = glow_shape(img.size, lambda d: d.ellipse([cx - r * 1.05, cy - r * 1.05, cx + r * 1.05, cy + r * 1.05], fill=255),
                      bottom, r * 0.35)
    img = add(img, halo, 0.8)
    img.paste(sun, (int(cx - r), int(cy - r)), mask)
    return img


def palm(d, base, height, lean, scale, color, seed=0):
    """Silhueta de palmeira: tronco curvo + folhas pendentes."""
    rnd = random.Random(seed)
    bx, by = base
    tx, ty = bx + lean, by - height
    # tronco: bezier quadrática afinando
    pts = []
    for i in range(41):
        t = i / 40
        cx, cy = bx + lean * 0.15, by - height * 0.5
        x = (1 - t) ** 2 * bx + 2 * (1 - t) * t * cx + t ** 2 * tx
        y = (1 - t) ** 2 * by + 2 * (1 - t) * t * cy + t ** 2 * ty
        pts.append((x, y, (1 - t) * 26 * scale + 10 * scale))
    for i in range(len(pts) - 1):
        x0, y0, w0 = pts[i]
        x1, y1, w1 = pts[i + 1]
        d.polygon([(x0 - w0 / 2, y0), (x0 + w0 / 2, y0), (x1 + w1 / 2, y1), (x1 - w1 / 2, y1)], fill=color)
        if i % 3 == 0:  # anéis do tronco
            d.line([(x0 - w0 / 2 - 2, y0), (x0 + w0 / 2 + 2, y0 - 4)], fill=color, width=int(4 * scale))
    # folhas
    angles = [-170, -145, -120, -95, -70, -45, -18, 8, -160, -30]
    for a in angles:
        a = math.radians(a + rnd.uniform(-6, 6))
        length = rnd.uniform(260, 360) * scale
        droop = rnd.uniform(0.45, 0.8)
        leaf_pts_top, leaf_pts_bot = [], []
        for i in range(31):
            t = i / 30
            x = tx + math.cos(a) * length * t
            y = ty + math.sin(a) * length * t + droop * length * t * t
            # largura da folha
            wv = math.sin(math.pi * min(1, t * 1.1)) * 34 * scale * (1 - t * 0.4)
            nx, ny = -math.sin(a), math.cos(a)
            leaf_pts_top.append((x + nx * wv * 0.5, y + ny * wv * 0.5 - wv * 0.2))
            leaf_pts_bot.append((x - nx * wv * 0.5, y - ny * wv * 0.5 + wv * 0.2))
        d.polygon(leaf_pts_top + leaf_pts_bot[::-1], fill=color)
        # recortes das folhas (folíolos)
        for i in range(4, 30, 3):
            x, y = leaf_pts_top[i]
            d.line([(x, y), (x + math.cos(a + 1.2) * 30 * scale, y + math.sin(a + 1.2) * 30 * scale)],
                   fill=color, width=int(9 * scale))
    d.ellipse([tx - 18 * scale, ty - 14 * scale, tx + 18 * scale, ty + 16 * scale], fill=color)


def perspective_grid(img, horizon, color, spacing=11, alpha=1.0, glow=True):
    w, h = img.size
    layer = Image.new("RGB", (w, h), (0, 0, 0))
    d = ImageDraw.Draw(layer)
    vx = w / 2
    for i in range(-30, 31):
        x_bottom = vx + i * w * 0.18
        d.line([(vx + i * 6, horizon), (x_bottom, h)], fill=color, width=4)
    y = horizon + 4
    step = 6
    while y < h:
        d.line([(0, y), (w, y)], fill=color, width=max(2, int(step / 10)))
        step *= 1.22
        y += step
    if glow:
        layer = add(layer.filter(ImageFilter.GaussianBlur(6)), layer, 1.0)
    return add(img, layer, alpha)


def skyline(d, base_y, w, color, seed, window=None, max_h=900):
    rnd = random.Random(seed)
    x = -20
    while x < w:
        bw = rnd.randint(70, 190)
        bh = rnd.randint(int(max_h * 0.25), max_h)
        d.rectangle([x, base_y - bh, x + bw, base_y], fill=color)
        if rnd.random() < 0.3:  # antena
            d.rectangle([x + bw / 2 - 3, base_y - bh - 80, x + bw / 2 + 3, base_y - bh], fill=color)
        if rnd.random() < 0.25:  # topo escalonado
            d.rectangle([x + bw * 0.2, base_y - bh - 60, x + bw * 0.8, base_y - bh], fill=color)
        if window:
            for wy in range(int(base_y - bh + 30), int(base_y - 20), 34):
                for wx in range(int(x + 14), int(x + bw - 14), 26):
                    if rnd.random() < 0.35:
                        d.rectangle([wx, wy, wx + 10, wy + 16], fill=rnd.choice(window))
        x += bw + rnd.randint(-10, 12)


def water_reflection(img, horizon, colors, seed):
    rnd = random.Random(seed)
    d = ImageDraw.Draw(img)
    w, h = img.size
    y = horizon + 10
    while y < h:
        span = rnd.uniform(0.1, 0.5) * w * (1 - (y - horizon) / (h - horizon) * 0.5)
        cx = w / 2 + rnd.uniform(-0.2, 0.2) * w
        d.line([(cx - span / 2, y), (cx + span / 2, y)], fill=rnd.choice(colors), width=rnd.randint(3, 8))
        y += rnd.randint(14, 34)
    return img


def neon_text(img, text, cy, size, color):
    w, h = img.size
    font = ImageFont.truetype(FONT, size)
    m = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(m)
    bbox = md.textbbox((0, 0), text, font=font)
    tx = (w - (bbox[2] - bbox[0])) / 2
    md.text((tx, cy), text, font=font, fill=0, stroke_width=10, stroke_fill=255)
    halo = m.filter(ImageFilter.GaussianBlur(28))
    col = Image.new("RGB", img.size, color)
    black = Image.new("RGB", img.size, (0, 0, 0))
    img = add(img, Image.composite(col, black, halo), 1.4)
    img = add(img, Image.composite(col, black, m.filter(ImageFilter.GaussianBlur(4))), 1.0)
    core = Image.new("RGB", img.size, tuple(min(255, c + 140) for c in color))
    img.paste(core, (0, 0), m)
    return img


# ------------------------------------------------------------ cenas
def scene_sunset_shore():
    img = vgrad(WIDTH, HEIGHT, [(0, (24, 6, 58)), (0.35, (120, 20, 120)), (0.55, (255, 90, 120)), (0.62, (255, 170, 90)),
                                (0.621, (40, 20, 90)), (1, (8, 6, 40))])
    img = stars(img, 160, 1, 0, 0.3)
    img = striped_sun(img, WIDTH / 2, HEIGHT * 0.53, 430)
    # corta o sol no horizonte
    d = ImageDraw.Draw(img)
    sea = vgrad(WIDTH, int(HEIGHT * 0.38), [(0, (70, 20, 110)), (1, (8, 6, 40))])
    img.paste(sea, (0, int(HEIGHT * 0.62)))
    img = water_reflection(img, HEIGHT * 0.62, [(255, 120, 150), (255, 200, 120), (190, 80, 200)], 3)
    d = ImageDraw.Draw(img)
    palm(d, (180, HEIGHT + 40), 1500, 160, 1.25, (14, 4, 24), 1)
    palm(d, (1330, HEIGHT + 60), 1250, -190, 1.05, (14, 4, 24), 2)
    palm(d, (1180, HEIGHT + 60), 900, -60, 0.8, (24, 8, 38), 5)
    return img


def scene_neon_grid():
    img = vgrad(WIDTH, HEIGHT, [(0, (6, 2, 22)), (0.45, (60, 10, 90)), (0.55, (200, 40, 140)), (0.551, (10, 2, 26)),
                                (1, (20, 0, 40))])
    img = stars(img, 300, 7, 0, 0.45)
    img = striped_sun(img, WIDTH / 2, HEIGHT * 0.47, 380, top=(255, 240, 120), bottom=(255, 30, 160))
    d = ImageDraw.Draw(img)
    # montanhas
    rnd = random.Random(4)
    pts = [(0, HEIGHT * 0.551)]
    x = 0
    while x < WIDTH:
        x += rnd.randint(80, 200)
        pts.append((x, HEIGHT * 0.551 - rnd.randint(40, 260) * (1.4 if abs(x - WIDTH / 2) > 400 else 0.4)))
    pts.append((WIDTH, HEIGHT * 0.551))
    d.polygon(pts, fill=(18, 4, 40))
    d.line(pts, fill=(34, 230, 255), width=4)
    img = perspective_grid(img, HEIGHT * 0.551, (255, 46, 180))
    return img


def scene_skyline():
    img = vgrad(WIDTH, HEIGHT, [(0, (20, 10, 60)), (0.3, (90, 30, 140)), (0.55, (255, 80, 130)), (0.7, (255, 180, 100)),
                                (1, (255, 200, 120))])
    img = striped_sun(img, WIDTH * 0.62, HEIGHT * 0.56, 330, gaps=5)
    d = ImageDraw.Draw(img)
    skyline(d, HEIGHT * 0.78, WIDTH, (90, 30, 110), 11, max_h=1100)
    skyline(d, HEIGHT * 0.82, WIDTH, (40, 10, 60), 12, window=[(255, 210, 120), (255, 120, 180), (120, 230, 255)], max_h=800)
    d.rectangle([0, HEIGHT * 0.82, WIDTH, HEIGHT], fill=(20, 4, 36))
    img = water_reflection(img, HEIGHT * 0.82, [(255, 120, 170), (255, 210, 120), (120, 230, 255)], 9)
    d = ImageDraw.Draw(img)
    palm(d, (120, HEIGHT + 30), 1700, 220, 1.3, (10, 2, 20), 8)
    return img


def scene_palm_night():
    img = vgrad(WIDTH, HEIGHT, [(0, (4, 10, 30)), (0.6, (16, 40, 90)), (0.75, (30, 120, 160)), (1, (6, 14, 40))])
    img = stars(img, 500, 21, 0, 0.7)
    moon = glow_shape(img.size, lambda d: d.ellipse([920, 520, 1220, 820], fill=255), (120, 220, 255), 70)
    img = add(img, moon, 1.0)
    d = ImageDraw.Draw(img)
    d.ellipse([920, 520, 1220, 820], fill=(230, 250, 255))
    d.ellipse([970, 500, 1250, 790], fill=(10, 24, 60))  # lua crescente
    palm(d, (300, HEIGHT + 50), 1900, 250, 1.4, (2, 4, 14), 31)
    palm(d, (1200, HEIGHT + 50), 1400, -220, 1.1, (2, 4, 14), 32)
    palm(d, (760, HEIGHT + 50), 1000, 60, 0.85, (6, 14, 34), 33)
    return img


def scene_highway():
    img = vgrad(WIDTH, HEIGHT, [(0, (30, 0, 50)), (0.4, (180, 40, 130)), (0.5, (255, 140, 90)), (0.501, (14, 4, 30)),
                                (1, (4, 2, 14))])
    img = stars(img, 120, 41, 0, 0.3)
    img = striped_sun(img, WIDTH / 2, HEIGHT * 0.44, 400, gaps=6)
    d = ImageDraw.Draw(img)
    hz = HEIGHT * 0.501
    skyline(d, hz, WIDTH, (40, 8, 60), 44, max_h=260)
    d.rectangle([0, hz, WIDTH, HEIGHT], fill=(14, 4, 30))
    # estrada
    d.polygon([(WIDTH / 2 - 30, hz), (WIDTH / 2 + 30, hz), (WIDTH + 400, HEIGHT), (-400, HEIGHT)], fill=(28, 10, 50))
    road = Image.new("RGB", img.size, (0, 0, 0))
    rd = ImageDraw.Draw(road)
    rd.line([(WIDTH / 2 - 30, hz), (-400, HEIGHT)], fill=(255, 46, 180), width=10)
    rd.line([(WIDTH / 2 + 30, hz), (WIDTH + 400, HEIGHT)], fill=(255, 46, 180), width=10)
    y, step = hz + 20, 20
    while y < HEIGHT:
        t = (y - hz) / (HEIGHT - hz)
        half = 3 + 18 * t
        rd.polygon([(WIDTH / 2 - half, y), (WIDTH / 2 + half, y), (WIDTH / 2 + half * 1.1, y + step * 0.6),
                    (WIDTH / 2 - half * 1.1, y + step * 0.6)], fill=(255, 220, 90))
        step *= 1.18
        y += step
    img = add(img, road.filter(ImageFilter.GaussianBlur(10)), 1.0)
    img = add(img, road, 1.0)
    d = ImageDraw.Draw(img)
    palm(d, (60, hz + 140), 700, 70, 0.55, (10, 2, 22), 51)
    palm(d, (1380, hz + 140), 640, -60, 0.5, (10, 2, 22), 52)
    return img


def scene_waves():
    img = vgrad(WIDTH, HEIGHT, [(0, (255, 170, 120)), (0.35, (255, 110, 150)), (1, (90, 30, 140))])
    d = ImageDraw.Draw(img)
    cols = [(255, 140, 160), (240, 90, 160), (200, 60, 160), (150, 40, 150), (100, 30, 130), (60, 20, 100), (30, 10, 70)]
    for i, c in enumerate(cols):
        base = HEIGHT * (0.45 + i * 0.08)
        amp = 60 + i * 12
        ph = i * 1.3
        pts = [(x, base + math.sin(x / WIDTH * 2 * math.pi * 1.4 + ph) * amp) for x in range(0, WIDTH + 20, 20)]
        d.polygon(pts + [(WIDTH, HEIGHT), (0, HEIGHT)], fill=c)
    img = striped_sun(img, WIDTH * 0.3, HEIGHT * 0.25, 220, top=(255, 250, 200), bottom=(255, 150, 120), gaps=4)
    return img


def scene_neon_sign():
    img = vgrad(WIDTH, HEIGHT, [(0, (10, 4, 24)), (1, (30, 8, 50))])
    # parede de tijolos sutil
    d = ImageDraw.Draw(img)
    for row, y in enumerate(range(0, HEIGHT, 60)):
        off = 0 if row % 2 == 0 else 70
        for x in range(-off, WIDTH, 140):
            d.rectangle([x + 3, y + 3, x + 137, y + 57], outline=(40, 16, 60), width=3)
    img = neon_text(img, "NEON", HEIGHT * 0.33, 330, (255, 46, 180))
    img = neon_text(img, "SHORE", HEIGHT * 0.45, 300, (34, 230, 255))
    # palmeira em neon
    m = Image.new("L", img.size, 0)
    palm(ImageDraw.Draw(m), (WIDTH / 2, HEIGHT * 0.86), 520, 40, 0.65, 255, 61)
    edges = m.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(5))
    col = Image.new("RGB", img.size, (80, 255, 170))
    black = Image.new("RGB", img.size, (0, 0, 0))
    img = add(img, Image.composite(col, black, edges.filter(ImageFilter.GaussianBlur(20))), 1.3)
    img = add(img, Image.composite(col, black, edges), 1.0)
    return img


def scene_flamingo_sky():
    img = vgrad(WIDTH, HEIGHT, [(0, (60, 200, 230)), (0.45, (255, 170, 200)), (0.7, (255, 120, 160)), (1, (120, 40, 140))])
    # nuvens suaves
    cloud = Image.new("L", img.size, 0)
    cd = ImageDraw.Draw(cloud)
    rnd = random.Random(71)
    for _ in range(26):
        x, y = rnd.uniform(-200, WIDTH), rnd.uniform(HEIGHT * 0.1, HEIGHT * 0.6)
        cd.ellipse([x, y, x + rnd.uniform(300, 700), y + rnd.uniform(60, 140)], fill=rnd.randint(60, 140))
    cloud = cloud.filter(ImageFilter.GaussianBlur(40))
    img = Image.composite(Image.new("RGB", img.size, (255, 235, 245)), img, cloud)
    d = ImageDraw.Draw(img)
    # orla: calçadão ondulado
    d.rectangle([0, HEIGHT * 0.84, WIDTH, HEIGHT], fill=(250, 230, 210))
    for x in range(0, WIDTH, 8):
        y = HEIGHT * 0.84 + 30 + math.sin(x / 50) * 22
        d.line([(x, y), (x, y + 18)], fill=(40, 30, 50), width=8)
        y2 = HEIGHT * 0.84 + 130 + math.sin(x / 50 + math.pi) * 22
        d.line([(x, y2), (x, y2 + 18)], fill=(40, 30, 50), width=8)
    d.rectangle([0, HEIGHT * 0.81, WIDTH, HEIGHT * 0.84], fill=(40, 170, 200))
    palm(d, (220, HEIGHT * 0.86), 1300, 120, 1.0, (60, 20, 70), 81)
    palm(d, (1220, HEIGHT * 0.86), 1650, -160, 1.2, (60, 20, 70), 82)
    return img


SCENES = [
    ("wall_sunset_shore", scene_sunset_shore),
    ("wall_neon_grid", scene_neon_grid),
    ("wall_skyline", scene_skyline),
    ("wall_palm_night", scene_palm_night),
    ("wall_highway", scene_highway),
    ("wall_waves", scene_waves),
    ("wall_neon_sign", scene_neon_sign),
    ("wall_pastel_shore", scene_flamingo_sky),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in SCENES:
        img = fn().convert("RGB")
        img.save(os.path.join(OUT, f"{name}.jpg"), quality=88, optimize=True, progressive=True)
        img.resize((360, 800), Image.LANCZOS).save(os.path.join(OUT, f"{name}_thumb.jpg"), quality=85, optimize=True)
        print("ok", name)


if __name__ == "__main__":
    main()
