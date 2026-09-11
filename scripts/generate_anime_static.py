import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import math, os, random

OUT = os.path.join(os.path.dirname(__file__), "..", "src", "images", "uploads")

def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def lerp(a, b, t):
    return a + (b - a) * t

def linear_gradient(w, h, c1, c2, angle=90):
    c1 = np.array(hex2rgb(c1), dtype=float)
    c2 = np.array(hex2rgb(c2), dtype=float)
    ang = math.radians(angle)
    xx, yy = np.meshgrid(np.linspace(0, 1, w), np.linspace(0, 1, h))
    t = xx * math.cos(ang) + yy * math.sin(ang)
    t = (t - t.min()) / (t.max() - t.min())
    img = np.zeros((h, w, 3))
    for i in range(3):
        img[:, :, i] = lerp(c1[i], c2[i], t)
    return Image.fromarray(img.astype('uint8'))

def soft_blob(img, cx, cy, r, color, blur, opacity=180):
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*hex2rgb(color), opacity))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    img.paste(Image.alpha_composite(img.convert('RGBA'), layer).convert('RGB'), (0, 0))
    return img

def style_sky(w, h, seed, palette):
    random.seed(seed)
    img = linear_gradient(w, h, palette[0], palette[1], angle=95).convert('RGB')
    # soft, flat cloud bands (generic, painterly -- no characters/IP)
    d = ImageDraw.Draw(img, 'RGBA')
    for i in range(6):
        y = int(h * (0.15 + i * 0.11))
        band_h = int(h * random.uniform(0.03, 0.07))
        x_off = random.randint(int(-w*0.1), int(w*0.1))
        d.ellipse([x_off - w*0.3, y, x_off + w*1.1, y + band_h], fill=(*hex2rgb(palette[2]), 70))
    img = img.filter(ImageFilter.GaussianBlur(w * 0.01))
    img = soft_blob(img, int(w*0.75), int(h*0.22), int(min(w,h)*0.16), "#fff3d6", blur=min(w,h)*0.08, opacity=150)
    return img

WALLPAPERS = [
    dict(slug="cloud-field", w=1080, h=1920, kind="phone"),
    dict(slug="cloud-field", w=1920, h=1080, kind="laptop"),
]
palette = ["#8fbfe0", "#f6d9c4", "#ffffff"]
for wp in WALLPAPERS:
    img = style_sky(wp["w"], wp["h"], 42, palette)
    img.save(os.path.join(OUT, f"{wp['slug']}-{wp['kind']}.jpg"), quality=88)

thumb = style_sky(700, 780, 43, palette)
thumb.save(os.path.join(OUT, "cloud-field-thumb.jpg"), quality=85)
print("done")
