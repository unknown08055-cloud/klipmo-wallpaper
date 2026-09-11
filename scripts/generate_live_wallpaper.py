"""
Generates a short, seamless, looping animation (original abstract art, no characters/IP)
to demo the "live wallpaper" feature. Encodes to mp4 for both phone and laptop sizes,
plus a poster frame (thumbnail) used before the video loads.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import math, os, subprocess, shutil

BASE = os.path.dirname(__file__)
TMP = os.path.join(BASE, "_frames")
OUT = os.path.join(BASE, "..", "src", "images", "uploads")
os.makedirs(OUT, exist_ok=True)

def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def lerp(a, b, t):
    return a + (b - a) * t

def frame(w, h, t, palette):
    # t in [0, 1), loops seamlessly
    c1 = np.array(hex2rgb(palette[0]), dtype=float)
    c2 = np.array(hex2rgb(palette[1]), dtype=float)
    xx, yy = np.meshgrid(np.linspace(0, 1, w), np.linspace(0, 1, h))
    wave = 0.5 + 0.5 * np.sin(2 * math.pi * (yy * 0.6 + t))
    img_arr = np.zeros((h, w, 3))
    for i in range(3):
        img_arr[:, :, i] = lerp(c1[i], c2[i], wave)
    img = Image.fromarray(img_arr.astype('uint8')).convert('RGBA')

    # drifting soft "petal" blobs -- generic circles, not any character/IP
    layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    n = 10
    for i in range(n):
        phase = (t + i / n) % 1.0
        cx = (0.15 + 0.7 * ((i * 0.37) % 1.0)) * w
        cy = (phase * 1.3 - 0.15) * h
        r = w * (0.05 + 0.02 * (i % 3))
        alpha = int(120 * math.sin(math.pi * phase) ** 0.5 + 20)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*hex2rgb(palette[2]), max(0, alpha)))
    layer = layer.filter(ImageFilter.GaussianBlur(r * 0.4))
    img = Image.alpha_composite(img, layer).convert('RGB')
    return img

def build(slug, w, h, palette, frames=48, fps=24):
    d = os.path.join(TMP, f"{slug}-{w}x{h}")
    os.makedirs(d, exist_ok=True)
    for i in range(frames):
        t = i / frames
        im = frame(w, h, t, palette)
        im.save(os.path.join(d, f"f{i:04d}.jpg"), quality=90)
        if i == 0:
            im.save(os.path.join(OUT, f"{slug}-poster.jpg"), quality=88)
    out_mp4 = os.path.join(OUT, f"{slug}-{'phone' if h > w else 'laptop'}.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(fps), "-i", os.path.join(d, "f%04d.jpg"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-vf", f"scale={w}:{h}", out_mp4
    ], check=True, capture_output=True)
    print("built", out_mp4)

palette = ["#3a1f3d", "#8a5a8f", "#f7c8d6"]  # soft dusk / sakura tones, fully original
build("sakura-drift", 1080, 1920, palette)
build("sakura-drift", 1920, 1080, palette)

shutil.rmtree(TMP, ignore_errors=True)
print("done")
