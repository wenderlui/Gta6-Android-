"""Ícone do app (adaptativo) e artes da Play Store.

Uso: python3 tools/branding.py  (rode depois de icons.py e wallpapers.py)
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import icons
from icons import G, neon, backdrop, g_palm, PINK, CYAN, W

ROOT = os.path.join(os.path.dirname(__file__), "..")
RES = os.path.join(ROOT, "app", "src", "main", "res")
STORE = os.path.join(ROOT, "store", "graphics")
NODPI = os.path.join(RES, "drawable-nodpi")
FONT_BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FONT_SEMI = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"


def palm_layer(size, color=PINK, safe=0.62):
    """Glifo da palmeira neon centralizado numa camada transparente."""
    g = G()
    g_palm(g)
    glyph = neon(g.img, color)
    inner = int(size * safe)
    glyph = glyph.resize((inner, inner), Image.LANCZOS)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(glyph, ((size - inner) // 2, (size - inner) // 2), glyph)
    return out


def launcher_icons():
    d = os.path.join(RES, "mipmap-xxxhdpi")
    os.makedirs(d, exist_ok=True)
    # camadas adaptativas: 108dp -> 432px em xxxhdpi; zona segura = 66dp (~61%)
    bg = full_bleed_bg(432)
    bg.save(os.path.join(d, "ic_launcher_background.png"), optimize=True)
    palm_layer(432).save(os.path.join(d, "ic_launcher_foreground.png"), optimize=True)
    g = G()
    g_palm(g)
    mono = Image.new("RGBA", (W, W), (255, 255, 255, 0))
    mono.putalpha(g.img)
    inner = int(432 * 0.58)
    mono = mono.resize((inner, inner), Image.LANCZOS)
    m = Image.new("RGBA", (432, 432), (0, 0, 0, 0))
    m.paste(mono, ((432 - inner) // 2, (432 - inner) // 2), mono)
    m.save(os.path.join(d, "ic_launcher_monochrome.png"), optimize=True)


def full_bleed_bg(size):
    """Fundo quadrado sem cantos transparentes (Play Store e camada adaptativa)."""
    import numpy as np
    ys = np.linspace(0, 1, size)[:, None]
    xs = np.linspace(-1, 1, size)[None, :]
    top, bottom = np.array([40, 8, 64]), np.array([10, 14, 44])
    img = top[None, None, :] * (1 - ys[..., None]) + bottom[None, None, :] * ys[..., None]
    glow = np.clip(1 - ((xs * 0.8) ** 2 + ((ys - 1.05) * 2.2) ** 2), 0, 1)[..., None]
    img = img + glow * np.array([150, 30, 110]) * 0.7
    return Image.fromarray(np.clip(img, 0, 255).astype("uint8"))


def store_icon():
    os.makedirs(STORE, exist_ok=True)
    g = G()
    g_palm(g)
    full = full_bleed_bg(W).convert("RGBA")
    glyph = neon(g.img, PINK)
    inner = int(W * 0.8)
    glyph = glyph.resize((inner, inner), Image.LANCZOS)
    full.alpha_composite(glyph, ((W - inner) // 2, (W - inner) // 2))
    full = full.convert("RGB")
    full.resize((512, 512), Image.LANCZOS).save(os.path.join(STORE, "icon-512.png"))


def text_center(d, text, y, font, fill, width):
    b = d.textbbox((0, 0), text, font=font)
    d.text(((width - (b[2] - b[0])) / 2, y), text, font=font, fill=fill)


def feature_graphic():
    wall = Image.open(os.path.join(NODPI, "wall_neon_grid.jpg"))
    # recorte horizontal: sol listrado + grade neon
    crop = wall.crop((0, 1080, 1440, 1080 + 703)).resize((1024, 500), Image.LANCZOS)
    overlay = Image.new("RGBA", crop.size, (10, 4, 30, 0))
    img = Image.alpha_composite(crop.convert("RGBA"), overlay)
    d = ImageDraw.Draw(img)
    title = ImageFont.truetype(FONT_BLACK, 96)
    sub = ImageFont.truetype(FONT_SEMI, 34)
    # título com brilho
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    text_center(gd, "NEON SHORE", 120, title, (40, 0, 40, 255), 1024)
    text_center(gd, "Ícones neon + wallpapers retrô", 250, sub, (20, 0, 30, 255), 1024)
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(img)
    text_center(d, "NEON SHORE", 120, title, (255, 235, 250), 1024)
    text_center(d, "Ícones neon + wallpapers retrô", 250, sub, (255, 255, 255), 1024)
    img.convert("RGB").save(os.path.join(STORE, "feature-graphic-1024x500.png"))


def phone_frame(screen, w=1080, h=2400):
    screen = screen.resize((w, h), Image.LANCZOS)
    return screen


def screenshot_home(wall_name, caption, icon_names, out_name):
    """Simula a tela inicial com o wallpaper e os ícones do pacote (Play exige telas que representem o app)."""
    w, h = 1080, 2400
    wall = Image.open(os.path.join(NODPI, wall_name + ".jpg")).resize((w, h), Image.LANCZOS).convert("RGBA")
    d = ImageDraw.Draw(wall)
    # relógio
    big = ImageFont.truetype(FONT_BLACK, 170)
    small = ImageFont.truetype(FONT_SEMI, 44)
    text_center(d, "21:45", 260, big, (255, 255, 255, 235), w)
    text_center(d, "sexta, 13 de novembro", 460, small, (255, 255, 255, 220), w)
    # grade de ícones
    size, cols = 168, 4
    gap = (w - cols * size) // (cols + 1)
    y0 = h - 300 - ((len(icon_names) + cols - 1) // cols) * (size + 90)
    lab = ImageFont.truetype(FONT_SEMI, 30)
    labels = {"phone": "Telefone", "messages": "Mensagens", "camera": "Câmera", "gallery": "Galeria",
              "browser": "Navegador", "music": "Música", "maps": "Mapas", "settings": "Ajustes",
              "clock": "Relógio", "calculator": "Calculadora", "calendar": "Agenda", "mail": "E-mail",
              "whatsapp": "Chat", "instagram": "Fotos", "spotify": "Player", "youtube": "Vídeos",
              "games": "Jogos", "weather": "Clima", "notes": "Notas", "files": "Arquivos"}
    for i, n in enumerate(icon_names):
        ic = Image.open(os.path.join(NODPI, f"ic_{n}.png")).resize((size, size), Image.LANCZOS)
        x = gap + (i % cols) * (size + gap)
        y = y0 + (i // cols) * (size + 90)
        wall.paste(ic, (x, y), ic)
        b = d.textbbox((0, 0), labels.get(n, n), font=lab)
        d.text((x + (size - (b[2] - b[0])) / 2, y + size + 12), labels.get(n, n), font=lab, fill=(255, 255, 255, 240))
    return add_caption(wall, caption, out_name)


def add_caption(img, caption, out_name):
    w, h = img.size
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    canvas.paste(img, (0, 0))
    band = Image.new("RGBA", (w, 150), (12, 4, 30, 200))
    canvas.alpha_composite(band, (0, 40))
    d = ImageDraw.Draw(canvas)
    f = ImageFont.truetype(FONT_BLACK, 58)
    text_center(d, caption, 82, f, (255, 225, 245, 255), w)
    canvas.convert("RGB").save(os.path.join(STORE, out_name))


def screenshot_icons():
    w, h = 1080, 2400
    bg = Image.open(os.path.join(NODPI, "wall_neon_grid.jpg")).resize((w, h), Image.LANCZOS).convert("RGBA")
    bg.alpha_composite(Image.new("RGBA", (w, h), (8, 2, 24, 150)))
    names = list(icons.ICONS.keys())[:28]
    size, cols = 200, 4
    gap = (w - cols * size) // (cols + 1)
    for i, n in enumerate(names):
        ic = Image.open(os.path.join(NODPI, f"ic_{n}.png")).resize((size, size), Image.LANCZOS)
        bg.paste(ic, (gap + (i % cols) * (size + gap), 300 + (i // cols) * (size + 60)), ic)
    add_caption(bg, f"{len(icons.ICONS)}+ ícones neon", "screenshot-2-icones.png")


def screenshot_walls():
    w, h = 1080, 2400
    bg = Image.new("RGBA", (w, h), (14, 6, 34, 255))
    names = ["wall_sunset_shore", "wall_neon_grid", "wall_skyline", "wall_palm_night", "wall_highway", "wall_waves"]
    tw, th = 470, 1000
    for i, n in enumerate(names):
        t = Image.open(os.path.join(NODPI, n + "_thumb.jpg")).resize((tw, th), Image.LANCZOS)
        m = Image.new("L", (tw, th), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, tw - 1, th - 1], 36, fill=255)
        x = 47 + (i % 2) * (tw + 46)
        y = 250 + (i // 2) * (th + 40)
        if y + th > h:
            break
        bg.paste(t, (x, y), m)
    add_caption(bg, "Wallpapers em alta resolução", "screenshot-3-wallpapers.png")


def main():
    launcher_icons()
    store_icon()
    feature_graphic()
    screenshot_home("wall_sunset_shore", "Seu Android no clima retrô",
                    ["phone", "messages", "camera", "gallery", "browser", "music", "maps", "settings",
                     "clock", "calculator", "calendar", "mail"], "screenshot-1-home.png")
    screenshot_icons()
    screenshot_walls()
    screenshot_home("wall_skyline", "Fácil de aplicar no seu launcher",
                    ["whatsapp", "instagram", "spotify", "youtube", "games", "weather", "notes", "files"],
                    "screenshot-4-launcher.png")
    print("ok")


if __name__ == "__main__":
    main()
