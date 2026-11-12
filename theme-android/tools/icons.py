"""Gera os ícones neon do pacote Neon Shore (arte 100% original, desenhada por código).

Uso: python3 tools/icons.py  (a partir de theme-android/)
"""
import math
import os
from PIL import Image, ImageDraw, ImageFilter

S = 4            # supersampling
SIZE = 192       # tamanho final de cada ícone
W = SIZE * S
U = W / 100.0    # unidade da grade 0..100

PINK = (255, 46, 160)
CYAN = (34, 230, 255)
ORANGE = (255, 150, 60)
YELLOW = (255, 214, 64)
PURPLE = (190, 110, 255)
GREEN = (80, 255, 170)

OUT = os.path.join(os.path.dirname(__file__), "..", "app", "src", "main", "res", "drawable-nodpi")


def p(x, y):
    return (x * U, y * U)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def squircle_mask(size, radius_frac=0.24):
    m = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(m)
    r = int(size * radius_frac)
    pad = int(size * 0.04)
    d.rounded_rectangle([pad, pad, size - pad, size - pad], r, fill=255)
    return m


def backdrop(accent):
    """Fundo: gradiente roxo-noite com faixa de pôr do sol e borda neon."""
    img = Image.new("RGB", (W, W))
    top, bottom = (40, 8, 64), (10, 14, 44)
    px = img.load()
    for y in range(W):
        c = lerp(top, bottom, y / W)
        for x in range(W):
            px[x, y] = c
    # brilho inferior de pôr do sol
    glow = Image.new("RGB", (W, W), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([-W * 0.3, W * 0.70, W * 1.3, W * 1.5], fill=(150, 30, 110))
    glow = glow.filter(ImageFilter.GaussianBlur(W * 0.08))
    img = Image.blend(img, Image.composite(glow, img, Image.new("L", (W, W), 255)), 0.0)
    img = Image.fromarray(__import__("numpy").clip(
        __import__("numpy").asarray(img, dtype="int16") + __import__("numpy").asarray(glow, dtype="int16") // 2, 0, 255
    ).astype("uint8"))
    out = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    out.paste(img, (0, 0), squircle_mask(W))
    # borda neon
    border = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    bd = ImageDraw.Draw(border)
    pad = int(W * 0.04)
    bd.rounded_rectangle([pad + 6, pad + 6, W - pad - 6, W - pad - 6], int(W * 0.22),
                         outline=accent + (150,), width=int(1.6 * U))
    out = Image.alpha_composite(out, border)
    return out


class G:
    """Desenha um glifo em traço neon numa camada."""

    def __init__(self):
        self.img = Image.new("L", (W, W), 0)
        self.d = ImageDraw.Draw(self.img)
        self.w = int(5.5 * U)

    def line(self, *pts, w=None):
        pts = [p(*q) for q in pts]
        self.d.line(pts, fill=255, width=int((w or 5.5) * U), joint="curve")
        r = (w or 5.5) * U / 2
        for (x, y) in (pts[0], pts[-1]):
            self.d.ellipse([x - r, y - r, x + r, y + r], fill=255)

    def rect(self, x0, y0, x1, y1, r=4, w=None, fill=False):
        if fill:
            self.d.rounded_rectangle([*p(x0, y0), *p(x1, y1)], r * U, fill=255)
        else:
            self.d.rounded_rectangle([*p(x0, y0), *p(x1, y1)], r * U, outline=255, width=int((w or 5.5) * U))

    def circle(self, cx, cy, r, w=None, fill=False):
        box = [*p(cx - r, cy - r), *p(cx + r, cy + r)]
        if fill:
            self.d.ellipse(box, fill=255)
        else:
            self.d.ellipse(box, outline=255, width=int((w or 5.5) * U))

    def arc(self, cx, cy, r, a0, a1, w=None):
        box = [*p(cx - r, cy - r), *p(cx + r, cy + r)]
        self.d.arc(box, a0, a1, fill=255, width=int((w or 5.5) * U))

    def poly(self, *pts, fill=True, w=None):
        pts = [p(*q) for q in pts]
        if fill:
            self.d.polygon(pts, fill=255)
        else:
            self.d.line(pts + [pts[0]], fill=255, width=int((w or 5.5) * U), joint="curve")

    def erase_circle(self, cx, cy, r):
        self.d.ellipse([*p(cx - r, cy - r), *p(cx + r, cy + r)], fill=0)


def neon(glyph_mask, color):
    """Transforma a máscara em letreiro neon: halo colorido + núcleo claro."""
    out = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    halo_big = glyph_mask.filter(ImageFilter.GaussianBlur(5 * U))
    halo = glyph_mask.filter(ImageFilter.GaussianBlur(2 * U))
    col = Image.new("RGBA", (W, W), color + (255,))
    out = Image.composite(col, out, halo_big.point(lambda v: min(255, int(v * 1.6))))
    tmp = Image.new("RGBA", (W, W), color + (255,))
    out = Image.alpha_composite(out, Image.composite(tmp, Image.new("RGBA", (W, W), (0, 0, 0, 0)), halo))
    core_col = lerp(color, (255, 255, 255), 0.55)
    core = Image.new("RGBA", (W, W), core_col + (255,))
    out = Image.alpha_composite(out, Image.composite(core, Image.new("RGBA", (W, W), (0, 0, 0, 0)), glyph_mask))
    return out


# ---------------------------------------------------------------- glifos
def g_phone(g):
    g.line((30, 24), (40, 24), (44, 38), (37, 44))
    g.line((37, 44), (44, 56), (56, 63))
    g.line((56, 63), (62, 56), (76, 60), (76, 70), (70, 76))
    g.line((30, 24), (25, 30), (24, 40), (30, 55), (45, 70), (60, 76), (70, 76))


def g_chat(g):
    g.rect(20, 24, 80, 66, r=14)
    g.line((34, 64), (28, 80), (48, 66))
    for x in (36, 50, 64):
        g.circle(x, 45, 3.2, fill=True)


def g_whats(g):
    # dois balões de conversa sobrepostos (genérico, sem logotipo)
    g.rect(14, 20, 62, 54, r=12)
    g.line((26, 52), (22, 64), (36, 54))
    g.rect(40, 42, 86, 74, r=12, w=4.5)
    g.line((74, 72), (78, 84), (66, 74), w=4.5)


def g_camera(g):
    g.rect(16, 32, 84, 76, r=10)
    g.line((36, 32), (40, 24), (60, 24), (64, 32))
    g.circle(50, 54, 13)
    g.circle(73, 42, 2.5, fill=True)


def g_insta(g):
    # coração sobre moldura de foto (genérico, sem logotipo)
    g.rect(18, 18, 82, 82, r=6, w=4)
    g.arc(40, 42, 10, 135, 360)
    g.arc(60, 42, 10, 180, 405)
    g.line((32.9, 49.1), (50, 66), (67.1, 49.1))


def g_gallery(g):
    g.rect(18, 22, 82, 78, r=8)
    g.line((24, 70), (42, 48), (54, 62), (62, 54), (76, 70))
    g.circle(64, 38, 6)


def g_music(g):
    g.line((40, 70), (40, 26), (72, 20), (72, 62))
    g.line((40, 36), (72, 30))
    g.circle(32, 70, 8, fill=True)
    g.circle(64, 62, 8, fill=True)


def g_disc(g):
    g.circle(50, 50, 30)
    g.circle(50, 50, 8)
    g.arc(50, 50, 20, 200, 260, w=3.5)


def g_waves(g):
    # equalizador (genérico, sem logotipo)
    for x, h in ((24, 22), (37, 40), (50, 28), (63, 46), (76, 18)):
        g.line((x, 72), (x, 72 - h), w=7)
    g.line((16, 80), (84, 80), w=3.5)


def g_play(g):
    # claquete de cinema (genérico, sem logotipo)
    g.rect(18, 38, 82, 80, r=6)
    g.line((18, 30), (78, 18), w=5)
    g.line((34, 27), (40, 36), w=4)
    g.line((52, 23), (58, 32), w=4)
    g.poly((44, 50), (44, 70), (60, 60))


def g_store(g):
    g.poly((28, 20), (28, 80), (78, 50), fill=False)
    g.line((28, 20), (56, 50), (28, 80), w=4)


def g_globe(g):
    g.circle(50, 50, 30)
    g.d.ellipse([*p(38, 20), *p(62, 80)], outline=255, width=int(4 * U))
    g.line((20, 50), (80, 50), w=4)
    g.arc(50, 4, 40, 55, 125, w=4)
    g.arc(50, 96, 40, 235, 305, w=4)


def g_mail(g):
    g.rect(16, 28, 84, 72, r=8)
    g.line((18, 32), (50, 54), (82, 32))


def g_pin(g):
    g.arc(50, 40, 20, 150, 390)
    g.line((32.7, 50), (50, 80), (67.3, 50))
    g.circle(50, 40, 7)


def g_gear(g):
    g.circle(50, 50, 12)
    for i in range(8):
        a = math.radians(i * 45)
        g.line((50 + 22 * math.cos(a), 50 + 22 * math.sin(a)), (50 + 32 * math.cos(a), 50 + 32 * math.sin(a)), w=8)
    g.circle(50, 50, 24)


def g_clock(g):
    g.circle(50, 50, 30)
    g.line((50, 32), (50, 50), (63, 58))


def g_calc(g):
    g.rect(24, 16, 76, 84, r=8)
    g.rect(32, 24, 68, 38, r=3, w=4)
    for yy in (52, 66):
        for xx in (36, 50, 64):
            g.circle(xx, yy, 3.4, fill=True)
    g.circle(36, 77, 3.4, fill=True)
    g.circle(50, 77, 3.4, fill=True)
    g.circle(64, 77, 3.4, fill=True)


def g_calendar(g):
    g.rect(18, 24, 82, 80, r=8)
    g.line((18, 40), (82, 40), w=4)
    g.line((34, 16), (34, 30))
    g.line((66, 16), (66, 30))
    for yy in (52, 66):
        for xx in (34, 50, 66):
            g.rect(xx - 4, yy - 4, xx + 4, yy + 4, r=1.5, fill=True)


def g_contacts(g):
    g.circle(50, 38, 13)
    g.arc(50, 82, 28, 200, 340)


def g_people(g):
    g.circle(40, 40, 11)
    g.arc(40, 80, 24, 200, 340)
    g.circle(66, 36, 8, w=4)
    g.arc(68, 70, 18, 225, 330, w=4)


def g_hash(g):
    g.line((40, 20), (34, 80))
    g.line((66, 20), (60, 80))
    g.line((22, 40), (80, 40))
    g.line((20, 62), (78, 62))


def g_note(g):
    g.line((40, 74), (40, 22), (66, 30))
    g.circle(32, 74, 9, fill=True)
    g.arc(56, 22, 16, 30, 110, w=4)


def g_tv(g):
    g.rect(16, 28, 84, 74, r=8)
    g.line((36, 16), (50, 28), (64, 16))
    g.line((44, 40), (44, 62), (60, 51), (44, 40), w=4.5)


def g_plane(g):
    g.poly((16, 48), (84, 20), (64, 80), (48, 58), fill=False)
    g.line((48, 58), (84, 20), w=4)
    g.line((48, 58), (46, 74), (56, 66), w=4)


def g_folder(g):
    g.line((16, 74), (16, 26), (40, 26), (46, 34), (84, 34), (84, 74), (16, 74))
    g.line((16, 44), (84, 44), w=4)


def g_notes(g):
    g.rect(24, 16, 76, 84, r=8)
    g.line((34, 34), (66, 34), w=4)
    g.line((34, 48), (66, 48), w=4)
    g.line((34, 62), (54, 62), w=4)


def g_search(g):
    g.circle(44, 44, 20)
    g.line((59, 59), (78, 78), w=8)


def g_cloud(g):
    g.arc(36, 56, 14, 90, 270)
    g.arc(54, 46, 20, 185, 340)
    g.arc(68, 58, 12, 270, 450)
    g.line((36, 70), (68, 70))


def g_card(g):
    g.rect(14, 26, 86, 74, r=8)
    g.line((14, 40), (86, 40), w=7)
    g.line((26, 60), (44, 60), w=4)


def g_car(g):
    g.line((18, 62), (18, 50), (30, 46), (38, 34), (64, 34), (74, 46), (84, 50), (84, 62), (18, 62))
    g.circle(32, 64, 7, fill=True)
    g.circle(70, 64, 7, fill=True)
    g.erase_circle(32, 64, 3)
    g.erase_circle(70, 64, 3)


def g_gamepad(g):
    g.rect(14, 34, 86, 70, r=17)
    g.line((32, 46), (32, 58), w=4)
    g.line((26, 52), (38, 52), w=4)
    g.circle(64, 48, 3.4, fill=True)
    g.circle(72, 56, 3.4, fill=True)


def g_sun(g):
    g.circle(50, 50, 15)
    for i in range(8):
        a = math.radians(i * 45 + 22.5)
        g.line((50 + 23 * math.cos(a), 50 + 23 * math.sin(a)), (50 + 32 * math.cos(a), 50 + 32 * math.sin(a)))


def g_mic(g):
    g.rect(40, 16, 60, 56, r=10)
    g.arc(50, 46, 20, 0, 180)
    g.line((50, 66), (50, 82))
    g.line((40, 82), (60, 82))


def g_video(g):
    g.rect(14, 30, 64, 70, r=8)
    g.poly((68, 44), (86, 34), (86, 66), (68, 56), fill=False, w=5)


def g_bag(g):
    g.line((22, 36), (78, 36), (74, 82), (26, 82), (22, 36))
    g.arc(50, 36, 14, 180, 360)


def g_palm(g):
    """Ícone do próprio app: palmeira neon com sol no horizonte."""
    def curve(p0, c, p1, w):
        pts = []
        for i in range(25):
            t = i / 24
            pts.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t ** 2 * p1[0],
                        (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t ** 2 * p1[1]))
        g.line(*pts, w=w)
    crown = (44, 34)
    g.arc(50, 84, 22, 180, 360, w=4)              # sol no horizonte
    g.line((14, 84), (86, 84), w=4)
    curve((56, 84), (58, 58), crown, 6)           # tronco
    curve(crown, (26, 24), (14, 46), 5)
    curve(crown, (34, 18), (22, 20), 4.5)
    curve(crown, (54, 16), (68, 22), 4.5)
    curve(crown, (68, 26), (84, 46), 5)
    curve(crown, (58, 36), (66, 54), 4.5)
    curve(crown, (32, 38), (28, 56), 4.5)

def g_wallet(g):
    g.rect(16, 28, 84, 76, r=10)
    g.line((60, 46), (84, 46), (84, 60), (60, 60), (60, 46), w=4)
    g.line((24, 28), (64, 16), (70, 28), w=4)


def g_bank(g):
    g.poly((16, 40), (50, 18), (84, 40), fill=False, w=5)
    for x in (28, 44, 56, 72):
        g.line((x, 48), (x, 72), w=4.5)
    g.line((16, 80), (84, 80))


def g_drive(g):
    g.poly((36, 20), (64, 20), (84, 56), (70, 80), (30, 80), (16, 56), fill=False, w=5)


def g_bolt(g):
    g.poly((56, 14), (26, 56), (48, 56), (42, 86), (74, 42), (52, 42), fill=False, w=5)


# nome do drawable -> (função, cor, [componentes])
ICONS = {
    "phone": (g_phone, GREEN, [
        "com.google.android.dialer/com.google.android.dialer.extensions.GoogleDialtactsActivity",
        "com.samsung.android.dialer/com.samsung.android.dialer.DialtactsActivity",
        "com.android.dialer/com.android.dialer.main.impl.MainActivity",
        "com.android.dialer/com.android.dialer.DialtactsActivity",
    ]),
    "messages": (g_chat, CYAN, [
        "com.google.android.apps.messaging/com.google.android.apps.messaging.ui.ConversationListActivity",
        "com.samsung.android.messaging/com.android.mms.ui.ConversationComposer",
        "com.android.mms/com.android.mms.ui.ConversationList",
    ]),
    "whatsapp": (g_whats, GREEN, [
        "com.whatsapp/com.whatsapp.Main",
        "com.whatsapp/com.whatsapp.home.ui.HomeActivity",
        "com.whatsapp.w4b/com.whatsapp.Main",
    ]),
    "camera": (g_camera, PINK, [
        "com.google.android.GoogleCamera/com.android.camera.CameraLauncher",
        "com.sec.android.app.camera/com.sec.android.app.camera.Camera",
        "com.android.camera2/com.android.camera.CameraLauncher",
        "com.motorola.camera3/com.motorola.camera.Camera",
    ]),
    "instagram": (g_insta, PINK, [
        "com.instagram.android/com.instagram.mainactivity.LauncherActivity",
        "com.instagram.android/com.instagram.mainactivity.MainActivity",
    ]),
    "gallery": (g_gallery, ORANGE, [
        "com.google.android.apps.photos/com.google.android.apps.photos.home.HomeActivity",
        "com.sec.android.gallery3d/com.samsung.android.gallery.app.activity.GalleryActivity",
        "com.sec.android.gallery3d/com.sec.android.gallery3d.app.GalleryActivity",
        "com.android.gallery3d/com.android.gallery3d.app.GalleryActivity",
    ]),
    "spotify": (g_waves, GREEN, ["com.spotify.music/com.spotify.music.MainActivity"]),
    "music": (g_music, PURPLE, [
        "com.google.android.apps.youtube.music/com.google.android.apps.youtube.music.activities.MusicActivity",
        "com.sec.android.app.music/com.sec.android.app.music.MusicMainActivity",
        "com.deezer.android.app/com.deezer.android.ui.activity.LauncherActivity",
    ]),
    "youtube": (g_play, PINK, [
        "com.google.android.youtube/com.google.android.youtube.app.honeycomb.Shell$HomeActivity",
        "com.google.android.youtube/com.google.android.apps.youtube.app.watchwhile.WatchWhileActivity",
    ]),
    "playstore": (g_store, CYAN, ["com.android.vending/com.android.vending.AssetBrowserActivity"]),
    "browser": (g_globe, CYAN, [
        "com.android.chrome/com.google.android.apps.chrome.Main",
        "com.sec.android.app.sbrowser/com.sec.android.app.sbrowser.SBrowserMainActivity",
        "org.mozilla.firefox/org.mozilla.fenix.HomeActivity",
        "com.brave.browser/com.google.android.apps.chrome.Main",
        "com.opera.browser/com.opera.Opera",
    ]),
    "mail": (g_mail, ORANGE, [
        "com.google.android.gm/com.google.android.gm.ConversationListActivityGmail",
        "com.samsung.android.email.provider/com.samsung.android.email.ui.messagelist.EmailMessageListActivity",
        "com.microsoft.office.outlook/com.microsoft.office.outlook.MainActivity",
    ]),
    "maps": (g_pin, PINK, [
        "com.google.android.apps.maps/com.google.android.maps.MapsActivity",
        "com.waze/com.waze.FreeMapAppActivity",
    ]),
    "settings": (g_gear, PURPLE, [
        "com.android.settings/com.android.settings.Settings",
        "com.android.settings/com.android.settings.homepage.SettingsHomepageActivity",
    ]),
    "clock": (g_clock, YELLOW, [
        "com.google.android.deskclock/com.android.deskclock.DeskClock",
        "com.sec.android.app.clockpackage/com.sec.android.app.clockpackage.ClockPackage",
        "com.android.deskclock/com.android.deskclock.DeskClock",
    ]),
    "calculator": (g_calc, ORANGE, [
        "com.google.android.calculator/com.android.calculator2.Calculator",
        "com.sec.android.app.popupcalculator/com.sec.android.app.popupcalculator.Calculator",
        "com.android.calculator2/com.android.calculator2.Calculator",
    ]),
    "calendar": (g_calendar, CYAN, [
        "com.google.android.calendar/com.android.calendar.AllInOneActivity",
        "com.samsung.android.calendar/com.samsung.android.app.calendar.activity.MainActivity",
    ]),
    "contacts": (g_contacts, YELLOW, [
        "com.google.android.contacts/com.android.contacts.activities.PeopleActivity",
        "com.samsung.android.app.contacts/com.samsung.android.contacts.contactslist.PeopleActivity",
        "com.android.contacts/com.android.contacts.activities.PeopleActivity",
    ]),
    "facebook": (g_people, CYAN, [
        "com.facebook.katana/com.facebook.katana.LoginActivity",
        "com.facebook.lite/com.facebook.lite.MainActivity",
    ]),
    "x": (g_hash, CYAN, ["com.twitter.android/com.twitter.android.StartActivity"]),
    "tiktok": (g_note, PINK, [
        "com.zhiliaoapp.musically/com.ss.android.ugc.aweme.splash.SplashActivity",
        "com.ss.android.ugc.trill/com.ss.android.ugc.aweme.splash.SplashActivity",
    ]),
    "netflix": (g_tv, PINK, ["com.netflix.mediaclient/com.netflix.mediaclient.ui.launch.UIWebViewActivity"]),
    "telegram": (g_plane, CYAN, ["org.telegram.messenger/org.telegram.ui.LaunchActivity"]),
    "files": (g_folder, YELLOW, [
        "com.google.android.apps.nbu.files/com.google.android.apps.nbu.files.home.HomeActivity",
        "com.sec.android.app.myfiles/com.sec.android.app.myfiles.external.ui.MainActivity",
        "com.google.android.documentsui/com.android.documentsui.LauncherActivity",
    ]),
    "notes": (g_notes, YELLOW, [
        "com.google.android.keep/com.google.android.keep.activities.BrowseActivity",
        "com.samsung.android.app.notes/com.samsung.android.app.notes.memolist.MemoListActivity",
    ]),
    "google": (g_search, CYAN, [
        "com.google.android.googlequicksearchbox/com.google.android.googlequicksearchbox.SearchActivity",
    ]),
    "drive": (g_drive, YELLOW, ["com.google.android.apps.docs/com.google.android.apps.docs.app.NewMainProxyActivity"]),
    "cloud": (g_cloud, CYAN, [
        "com.dropbox.android/com.dropbox.android.activity.DropboxBrowser",
        "com.microsoft.skydrive/com.microsoft.skydrive.MainActivity",
    ]),
    "wallet": (g_wallet, GREEN, [
        "com.google.android.apps.walletnfcrel/com.google.commerce.tapandpay.android.wallet.WalletActivity",
        "com.samsung.android.spay/com.samsung.android.spay.ui.SpayMainActivity",
    ]),
    "bank": (g_bank, PURPLE, [
        "com.nu.production/com.nu.production.MainActivity",
        "br.com.intermedium/br.com.intermedium.MainActivity",
        "com.itau/com.itau.MainActivity",
    ]),
    "car": (g_car, ORANGE, [
        "com.ubercab/com.ubercab.presidio.app.core.root.RootActivity",
        "com.taxis99/com.taxis99.app.ui.splash.SplashActivity",
    ]),
    "games": (g_gamepad, PURPLE, [
        "com.google.android.play.games/com.google.android.gms.games.ui.destination.main.MainActivity",
        "com.discord/com.discord.main.MainActivity",
        "com.samsung.android.game.gamehome/com.samsung.android.game.gamehome.main.MainActivity",
    ]),
    "weather": (g_sun, YELLOW, [
        "com.sec.android.daemonapp/com.sec.android.daemonapp.app.MainActivity",
        "com.google.android.apps.weather/com.google.android.apps.weather.WeatherActivity",
    ]),
    "recorder": (g_mic, PINK, [
        "com.sec.android.app.voicenote/com.sec.android.app.voicenote.main.VNMainActivity",
        "com.google.android.apps.recorder/com.google.android.apps.recorder.ui.RecorderActivity",
    ]),
    "meet": (g_video, GREEN, [
        "com.google.android.apps.tachyon/com.google.android.apps.tachyon.MainActivity",
        "us.zoom.videomeetings/com.zipow.videobox.LauncherActivity",
    ]),
    "shop": (g_bag, ORANGE, [
        "com.mercadolibre/com.mercadolibre.splash.SplashActivity",
        "com.amazon.mShop.android.shopping/com.amazon.mShop.home.HomeActivity",
        "com.shopee.br/com.shopee.app.ui.home.HomeActivity_",
    ]),
    "food": (g_bolt, YELLOW, [
        "br.com.brainweb.ifood/br.com.brainweb.ifood.presentation.splash.SplashActivity",
    ]),
    "disc": (g_disc, PURPLE, ["com.amazon.mp3/com.amazon.mp3.activity.MusicHomeActivity"]),
}


def render_icon(fn, color):
    g = G()
    fn(g)
    base = backdrop(color)
    glyph = neon(g.img, color)
    base = Image.alpha_composite(base, glyph)
    return base.resize((SIZE, SIZE), Image.LANCZOS)


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, (fn, color, _) in ICONS.items():
        render_icon(fn, color).save(os.path.join(OUT, f"ic_{name}.png"), optimize=True)
    # fundo genérico para apps não temáticos (iconback)
    backdrop(PINK).resize((SIZE, SIZE), Image.LANCZOS).save(os.path.join(OUT, "iconback.png"), optimize=True)
    print(f"{len(ICONS)} ícones gerados em {os.path.abspath(OUT)}")


if __name__ == "__main__":
    main()
