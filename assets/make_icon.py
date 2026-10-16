"""Builds the Galactic Macro app icon: the spiral galaxy from galaxy.py with a robot face in the
bottom-right corner. galaxy.py is copied from the Internet Downloader project's store assets.

Needs Pillow and NumPy:  python make_icon.py
Writes icon.png (1024 x 1024), icon.ico (16-256 px) and the installer's wizard-*.bmp images next to
this script, and the GitHub social preview to ../docs/social-preview.png. The galaxy is seeded,
so the output is the same every time."""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import galaxy

HERE = Path(__file__).parent
SIZE = 1024
SS = 4  # supersampling for the robot's vector shapes

OUTLINE = (12, 16, 40, 255)
METAL_TOP = np.array([236, 242, 252])
METAL_BOTTOM = np.array([140, 156, 184])
VISOR = (18, 26, 58, 255)
GLOW = (90, 230, 255)
BULB = (255, 92, 120)


def box(x0, y0, x1, y1):
    return [v * SS for v in (x0, y0, x1, y1)]


def gradient_fill(layer, shape_mask, top_y, bottom_y):
    """Paints a vertical metal gradient into `layer` wherever `shape_mask` is set."""
    S = layer.size[0]
    t = np.clip((np.arange(S) - top_y * SS) / ((bottom_y - top_y) * SS), 0, 1)[:, None, None]
    rgb = METAL_TOP * (1 - t) + METAL_BOTTOM * t
    grad = np.broadcast_to(rgb, (S, S, 3)).astype(np.uint8)
    layer.paste(Image.fromarray(grad, 'RGB'), (0, 0), shape_mask)


def robot():
    """Returns the robot as a SIZE x SIZE RGBA layer (transparent elsewhere)."""
    S = SIZE * SS
    layer = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    ol = 16 * SS  # outline width

    # Head geometry (in 1024 px units).
    hx0, hy0, hx1, hy1 = 548, 600, 948, 924
    cx = (hx0 + hx1) / 2

    # Antenna: stalk and glowing bulb.
    d.rounded_rectangle(box(cx - 13, 510, cx + 13, hy0 + 10), radius=13 * SS, fill=OUTLINE)
    d.rounded_rectangle(box(cx - 5, 518, cx + 5, hy0 + 10), radius=5 * SS, fill=tuple(METAL_BOTTOM) + (255,))
    d.ellipse(box(cx - 40, 468, cx + 40, 548), fill=OUTLINE)
    d.ellipse(box(cx - 26, 482, cx + 26, 534), fill=BULB + (255,))

    # Ears.
    for ex0, ex1 in ((hx0 - 42, hx0 + 10), (hx1 - 10, hx1 + 42)):
        d.rounded_rectangle(box(ex0, 700, ex1, 824), radius=22 * SS, fill=OUTLINE)
        m = Image.new('L', (S, S), 0)
        ImageDraw.Draw(m).rounded_rectangle(box(ex0 + 14, 714, ex1 - 14, 810), radius=12 * SS, fill=255)
        gradient_fill(layer, m, 700, 824)

    # Head: dark outline, then a metal gradient body.
    d.rounded_rectangle(box(hx0, hy0, hx1, hy1), radius=78 * SS, fill=OUTLINE)
    body = Image.new('L', (S, S), 0)
    ImageDraw.Draw(body).rounded_rectangle(
        [hx0 * SS + ol, hy0 * SS + ol, hx1 * SS - ol, hy1 * SS - ol], radius=64 * SS, fill=255)
    gradient_fill(layer, body, hy0, hy1)
    d = ImageDraw.Draw(layer)

    # Visor (face plate).
    vx0, vy0, vx1, vy1 = hx0 + 46, hy0 + 72, hx1 - 46, hy1 - 46
    d.rounded_rectangle(box(vx0, vy0, vx1, vy1), radius=46 * SS, fill=VISOR)

    # Eyes and mouth on their own layer so they can glow.
    face = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    f = ImageDraw.Draw(face)
    ey = vy0 + 72
    for ex in (cx - 78, cx + 78):
        f.ellipse(box(ex - 40, ey - 40, ex + 40, ey + 40), fill=GLOW + (255,))
    my = vy1 - 52
    f.rounded_rectangle(box(cx - 92, my - 13, cx + 92, my + 13), radius=13 * SS, fill=GLOW + (255,))
    for gx in (cx - 46, cx, cx + 46):  # grille gaps
        f.rectangle(box(gx - 5, my - 13, gx + 5, my + 13), fill=VISOR)

    glow = face.filter(ImageFilter.GaussianBlur(18 * SS))
    layer = Image.alpha_composite(layer, glow)
    layer = Image.alpha_composite(layer, face)
    # Pupils: small bright highlights.
    d = ImageDraw.Draw(layer)
    for ex in (cx - 78, cx + 78):
        d.ellipse(box(ex - 4, ey - 26, ex + 22, ey), fill=(235, 255, 255, 255))

    return layer.resize((SIZE, SIZE), Image.LANCZOS)


def compose():
    base = galaxy.icon(SIZE)
    bot = robot()
    # Drop shadow so the robot stands off the galaxy.
    a = np.asarray(bot)[..., 3].astype(float) / 255
    shadow = Image.fromarray((a * 200).astype(np.uint8), 'L').filter(ImageFilter.GaussianBlur(14))
    shadow_rgba = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    shadow_rgba.paste((0, 0, 0, 255), (8, 14), shadow)
    out = Image.alpha_composite(base, shadow_rgba)
    out = Image.alpha_composite(out, bot)
    # Keep the robot and its shadow inside the icon's rounded square.
    out.putalpha(Image.fromarray(np.minimum(np.asarray(out)[..., 3], np.asarray(base)[..., 3])))
    return out


def scaled(img, px):
    small = img.resize((px, px), Image.LANCZOS)
    if px <= 48:
        small = small.filter(ImageFilter.UnsharpMask(radius=1, percent=60, threshold=0))
    return small


def wizard_images(icon_img):
    """Installer artwork: the tall welcome-page panel and the small header image, each at 100% and 200%."""
    w, h = 328, 628
    light = galaxy.galaxy(h, 0.45 * h, h / 2, h * 0.40, rot=np.deg2rad(-28))
    g = galaxy.tonemap(light, 2.2)[:, (h - w) // 2:(h + w) // 2]
    panel = galaxy.to_image(galaxy.screen(galaxy.background(w, h, seed=11), g)).convert('RGBA')
    bot = robot()
    bot = bot.crop(bot.getbbox())
    bw = 200
    bot = bot.resize((bw, round(bot.height * bw / bot.width)), Image.LANCZOS)
    panel.alpha_composite(bot, ((w - bw) // 2, h - bot.height - 40))
    panel = panel.convert('RGB')
    panel.save(HERE / 'wizard-large-200.bmp')
    panel.resize((w // 2, h // 2), Image.LANCZOS).save(HERE / 'wizard-large-100.bmp')
    for px, name in ((55, 'wizard-small-100.bmp'), (110, 'wizard-small-200.bmp')):
        small = Image.new('RGBA', (px, px), (255, 255, 255, 255))
        small.alpha_composite(scaled(icon_img, px))
        small.convert('RGB').save(HERE / name)



def social_preview(icon_img):
    """1280 x 640 card for link previews: starfield, a large faint galaxy, the icon, name and tagline."""
    w, h = 1280, 640
    gs = 1100
    light = galaxy.galaxy(gs, 0.45 * gs, gs / 2, gs / 2, rot=np.deg2rad(-28))
    g = galaxy.tonemap(light, 2.2) * 0.55
    big = np.zeros((h, w, 3))
    x0, y0 = w - gs // 2 - 230, h // 2 - gs // 2  # galaxy centred right of the text, bleeding off the edges
    sx0, sy0 = max(0, -x0), max(0, -y0)
    dx0, dy0 = max(0, x0), max(0, y0)
    cw, ch = min(w - dx0, gs - sx0), min(h - dy0, gs - sy0)
    big[dy0:dy0 + ch, dx0:dx0 + cw] = g[sy0:sy0 + ch, sx0:sx0 + cw]
    card = galaxy.to_image(galaxy.screen(galaxy.background(w, h, seed=5), big)).convert('RGBA')

    ic = 300
    card.alpha_composite(icon_img.resize((ic, ic), Image.LANCZOS), (90, (h - ic) // 2))

    d = ImageDraw.Draw(card)
    fonts = Path('C:/Windows/Fonts')
    title = ImageFont.truetype(str(fonts / 'segoeuib.ttf'), 96)
    tag = ImageFont.truetype(str(fonts / 'segoeui.ttf'), 38)
    small = ImageFont.truetype(str(fonts / 'seguisb.ttf'), 28)
    tx = 90 + ic + 60
    d.text((tx, 190), 'Galactic Macro', font=title, fill=(255, 255, 255))
    d.text((tx, 318), 'Record and play back mouse and', font=tag, fill=(205, 220, 255))
    d.text((tx, 364), 'keyboard macros on Windows', font=tag, fill=(205, 220, 255))
    d.text((tx, 440), 'Custom hotkeys  ·  Countdown  ·  Free & open source', font=small, fill=tuple(GLOW))
    card.convert('RGB').save(HERE.parent / 'docs' / 'social-preview.png', optimize=True)


if __name__ == '__main__':
    img = compose()
    img.save(HERE / 'icon.png')
    sizes = [256, 128, 64, 48, 40, 32, 24, 20, 16]
    frames = [scaled(img, s) for s in sizes]
    frames[0].save(HERE / 'icon.ico', sizes=[(s, s) for s in sizes], append_images=frames[1:])
    wizard_images(img)
    social_preview(img)
