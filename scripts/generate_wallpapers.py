"""
Generates placeholder wallpaper artwork so the demo site has real images to show.
These are original procedurally-generated gradients/patterns (no copyrighted material) —
meant to be REPLACED by the site owner's real wallpapers via the admin panel.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import math, os, random

OUT = os.path.join(os.path.dirname(__file__), "..", "src", "images", "uploads")
os.makedirs(OUT, exist_ok=True)

def lerp(a, b, t):
    return a + (b - a) * t

def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

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

def add_grain(img, amount=6):
    arr = np.array(img).astype(int)
    noise = np.random.randint(-amount, amount, arr.shape)
    arr = np.clip(arr + noise, 0, 255)
    return Image.fromarray(arr.astype('uint8'))

def soft_blob(img, cx, cy, r, color, blur, opacity=180):
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*hex2rgb(color), opacity))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    img.paste(Image.alpha_composite(img.convert('RGBA'), layer).convert('RGB'), (0, 0))
    return img

def style_nature(w, h, seed, palette):
    random.seed(seed)
    img = linear_gradient(w, h, palette[0], palette[1], angle=random.choice([70, 110, 160]))
    img = img.convert('RGB')
    for i in range(4):
        cx, cy = random.randint(0, w), random.randint(int(h*0.3), h)
        r = random.randint(int(w*0.25), int(w*0.55))
        img = soft_blob(img, cx, cy, r, palette[2], blur=r*0.6, opacity=110)
    img = add_grain(img, 5)
    return img

def style_abstract(w, h, seed, palette):
    random.seed(seed)
    img = linear_gradient(w, h, palette[0], palette[1], angle=random.choice([30, 200, 250]))
    for i in range(5):
        cx, cy = random.randint(0, w), random.randint(0, h)
        r = random.randint(int(min(w,h)*0.15), int(min(w,h)*0.4))
        img = soft_blob(img, cx, cy, r, random.choice(palette[2:]), blur=r*0.7, opacity=140)
    img = add_grain(img, 4)
    return img

def style_minimal(w, h, seed, palette):
    random.seed(seed)
    img = Image.new('RGB', (w, h), hex2rgb(palette[0]))
    d = ImageDraw.Draw(img, 'RGBA')
    r = int(min(w, h) * 0.28)
    cx, cy = int(w*0.7), int(h*0.35)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(*hex2rgb(palette[1]), 255))
    line_y = int(h*0.72)
    d.line([(int(w*0.1), line_y), (int(w*0.55), line_y)], fill=(*hex2rgb(palette[2]), 220), width=max(2, int(h*0.004)))
    img = add_grain(img, 3)
    return img

def style_space(w, h, seed, palette):
    random.seed(seed)
    img = linear_gradient(w, h, palette[0], palette[1], angle=100)
    img = img.filter(ImageFilter.GaussianBlur(2))
    for i in range(2):
        cx, cy = random.randint(int(w*0.2), int(w*0.8)), random.randint(int(h*0.1), int(h*0.6))
        r = random.randint(int(min(w,h)*0.2), int(min(w,h)*0.45))
        img = soft_blob(img, cx, cy, r, palette[2], blur=r*0.8, opacity=90)
    px = img.load()
    for _ in range(int(w*h/900)):
        x, y = random.randint(0, w-1), random.randint(0, h-1)
        b = random.randint(120, 255)
        px[x, y] = (b, b, min(255, b+15))
    return img

def style_dark(w, h, seed, palette):
    random.seed(seed)
    img = linear_gradient(w, h, palette[0], palette[0], angle=90)
    cx, cy = int(w*0.5), int(h*0.85)
    r = int(max(w, h) * 0.55)
    img = soft_blob(img, cx, cy, r, palette[1], blur=r*0.5, opacity=160)
    img = add_grain(img, 6)
    return ImageEnhance.Contrast(img).enhance(1.08)

def style_neon(w, h, seed, palette):
    random.seed(seed)
    img = Image.new('RGB', (w, h), hex2rgb(palette[0]))
    d = ImageDraw.Draw(img, 'RGBA')
    horizon = int(h*0.62)
    step = max(18, int(h*0.05))
    for i, y in enumerate(range(horizon, h, step)):
        fade = int(255 * (1 - i / ((h-horizon)/step + 1)))
        d.line([(0, y), (w, y)], fill=(*hex2rgb(palette[1]), max(30, fade)), width=2)
    vp = (int(w*0.5), horizon)
    for x in range(0, w+1, step*2):
        d.line([vp, (x, h)], fill=(*hex2rgb(palette[1]), 60), width=1)
    img = soft_blob(img, vp[0], vp[1], int(w*0.35), palette[2], blur=int(w*0.12), opacity=140)
    img = add_grain(img, 4)
    return img

WALLPAPERS = [
    dict(slug="fern-canopy", title="Fern Canopy", category="nature", fn=style_nature,
         palette=["#123524", "#2f6b4f", "#8fd6a0"], seed=1),
    dict(slug="blue-ridge", title="Blue Ridge", category="nature", fn=style_nature,
         palette=["#0f2d3a", "#2f6f7e", "#a8e0d1"], seed=2),
    dict(slug="molten-glass", title="Molten Glass", category="abstract", fn=style_abstract,
         palette=["#2a0f3d", "#7a1f6b", "#ff7a59", "#ffd166"], seed=3),
    dict(slug="shard", title="Shard", category="abstract", fn=style_abstract,
         palette=["#0d1b3e", "#3a2a7a", "#e64980", "#3ec6c6"], seed=4),
    dict(slug="eclipse-minimal", title="Eclipse Minimal", category="minimal", fn=style_minimal,
         palette=["#eae5db", "#1c1f26", "#c9a15a"], seed=5),
    dict(slug="quiet-line", title="Quiet Line", category="minimal", fn=style_minimal,
         palette=["#e7ded0", "#b7cfc4", "#3a3f36"], seed=6),
    dict(slug="deep-field", title="Deep Field", category="space", fn=style_space,
         palette=["#050914", "#131b3a", "#5f4b9e"], seed=7),
    dict(slug="orbit", title="Orbit", category="space", fn=style_space,
         palette=["#08060f", "#241338", "#7a3ba0"], seed=8),
    dict(slug="afterhours", title="Afterhours", category="dark", fn=style_dark,
         palette=["#0b0c0f", "#e4a94a"], seed=9),
    dict(slug="neon-grid", title="Neon Grid", category="neon", fn=style_neon,
         palette=["#0a0912", "#5fd3c4", "#e4a94a"], seed=10),
]

SIZES = {
    "phone": (1080, 1920),
    "laptop": (1920, 1080),
}
# varied thumb heights (at fixed width) to create a masonry feel
THUMB_W = 700
THUMB_HEIGHTS = [860, 560, 940, 640, 780, 520, 900, 600, 820, 700]

for i, wp in enumerate(WALLPAPERS):
    for kind, (w, h) in SIZES.items():
        img = wp["fn"](w, h, wp["seed"] * 13 + hash(kind) % 7, wp["palette"])
        img.save(os.path.join(OUT, f"{wp['slug']}-{kind}.jpg"), quality=87)
    th_h = THUMB_HEIGHTS[i % len(THUMB_HEIGHTS)]
    thumb = wp["fn"](THUMB_W, th_h, wp["seed"] * 13 + 99, wp["palette"])
    thumb.save(os.path.join(OUT, f"{wp['slug']}-thumb.jpg"), quality=85)
    print("generated", wp["slug"])

print("done ->", OUT)
