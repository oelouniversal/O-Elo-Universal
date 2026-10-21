#!/usr/bin/env python3
"""Arte de capa: corrente de sete elos de ouro (um por lei) sobre grafite.
Renderizada por raymarching (src/chain.c) + pós-processamento (profundidade de campo,
bloom, grão). Sem tipografia embutida. Uso:
  python3 make_cover.py preview|final
"""
import subprocess, sys, os, numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(ROOT, "build")
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(BUILD, exist_ok=True); os.makedirs(ASSETS, exist_ok=True)

POSE = dict(z=-20.0, x=34.0, y=14.0, tx=1.5, ty=6.5, tz=88.0, fov=30.0, spin=24.0)

def compile_c():
    exe = os.path.join(BUILD, "chain")
    src = os.path.join(HERE, "chain.c")
    if not os.path.exists(exe) or os.path.getmtime(exe) < os.path.getmtime(src):
        subprocess.check_call(["gcc", "-O3", "-ffast-math", "-fopenmp", src, "-o", exe, "-lm"])
    return exe

def render(W, H, SS, out, pose):
    exe = compile_c()
    args = [exe, str(W), str(H), str(SS), out, str(pose["z"]), str(pose["x"]), str(pose["y"]),
            str(pose["tx"]), str(pose["ty"]), str(pose["tz"]), str(pose["fov"]), str(pose["spin"])]
    subprocess.check_call(args)
    return np.fromfile(out, dtype=np.float32).reshape(H, W, 5)

def gblur(img, s):
    if s < 0.05: return img
    if img.ndim == 2: return ndi.gaussian_filter(img, s, mode="nearest")
    return np.stack([ndi.gaussian_filter(img[..., c], s, mode="nearest") for c in range(img.shape[2])], -1)

def srgb(x):
    x = np.clip(x, 0, 1)
    return np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(x, 1 / 2.4) - 0.055)

def aces(x):
    a, b, c, d, e = 2.51, 0.03, 2.43, 0.59, 0.14
    return np.clip((x * (a * x + b)) / (x * (c * x + d) + e), 0, 1)

def compose(raw, out_size, seed=7):
    H, W = raw.shape[:2]
    rng = np.random.default_rng(seed)
    rgb = raw[..., :3].copy(); alpha = np.clip(raw[..., 3], 0, 1); depth = raw[..., 4].copy()
    valid = alpha > 1e-3
    # profundidade preenchida para o fundo (vizinho mais próximo)
    idx = ndi.distance_transform_edt(~valid, return_distances=False, return_indices=True)
    dfill = depth[idx[0], idx[1]]
    # foco: elo mais próximo do terço inferior
    dv = depth[valid]
    near, far = np.percentile(dv, 2), np.percentile(dv, 98)
    focus = near + 0.30 * (far - near)
    span = max(far - near, 1e-3)
    coc = np.abs(dfill - focus) / span          # 0..~1
    sig_max = 0.0075 * W                        # px
    sig = np.clip(coc * 1.15, 0, 1) ** 1.2 * sig_max
    levels = [0, 0.18, 0.4, 0.7, 1.0]
    levels = [l * sig_max for l in levels]
    pm = np.concatenate([rgb, alpha[..., None]], -1)
    stack = [gblur(pm, s) for s in levels]
    out = np.zeros_like(pm)
    for i in range(len(levels) - 1):
        lo, hi = levels[i], levels[i + 1]
        w = np.clip((sig - lo) / (hi - lo), 0, 1)
        sel = (sig >= lo) & (sig <= hi + 1e-6) if i < len(levels) - 2 else (sig >= lo)
        mix = stack[i] * (1 - w[..., None]) + stack[i + 1] * w[..., None]
        out = np.where(sel[..., None], mix, out)
    out = np.where((sig < 1e-3)[..., None], pm, out)
    crgb, ca = out[..., :3], np.clip(out[..., 3], 0, 1)
    # neblina de profundidade: elos distantes mergulham no escuro
    fog = 1.0 - 0.62 * np.clip((dfill - near) / span, 0, 1) ** 1.35
    crgb = crgb * fog[..., None]
    # fundo grafite
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx, ny = (xx / W - 0.5), (yy / H - 0.46)
    r2 = nx * nx * 1.5 + ny * ny
    bg_l = 0.0075 + 0.026 * np.exp(-r2 * 5.6)       # luminância linear
    bg = np.stack([bg_l * 0.97, bg_l * 0.99, bg_l * 1.05], -1)
    # brilho âmbar sutil atrás da corrente
    halo = gblur(alpha, 0.05 * W)[..., None]
    bg = bg + halo * np.array([0.040, 0.024, 0.008])[None, None, :]
    lin = crgb + (1 - ca[..., None]) * bg
    # bloom
    lum = lin @ np.array([0.2126, 0.7152, 0.0722])
    hl = np.clip(lum - 0.9, 0, None)[..., None] * lin / np.maximum(lum[..., None], 1e-4)
    bloom = gblur(hl, 0.012 * W) * 0.55 + gblur(hl, 0.035 * W) * 0.45
    lin = lin + bloom
    # tone map + vignette + grão
    img = srgb(aces(lin * 1.22))
    vig = 1.0 - 0.42 * np.clip((np.sqrt(nx * nx * 1.2 + ny * ny * 0.9) - 0.25) / 0.6, 0, 1) ** 1.6
    img = img * vig[..., None]
    grain = rng.normal(0, 0.011, (H, W, 1)).astype(np.float32)
    grain = gblur(grain[..., 0], 0.6)[..., None] * 1.6
    img = np.clip(img + grain, 0, 1)
    im = Image.fromarray((img * 255 + 0.5).astype(np.uint8))
    if im.size != out_size:
        im = im.resize(out_size, Image.LANCZOS)
    return im

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    if mode == "preview":
        W, H = 437, 620
        raw = render(W, H, 2, os.path.join(BUILD, "chain_preview.raw"), POSE)
        im = compose(raw, (W, H))
        im.save(os.path.join(BUILD, "cover_preview.png"))
        print("preview ok")
    else:
        W, H, SS = 1748, 2480, 2
        raw = render(W, H, SS, os.path.join(BUILD, "chain_final.raw"), POSE)
        im = compose(raw, (W, H))
        im.save(os.path.join(ASSETS, "capa-elos.png"), optimize=True)
        im.save(os.path.join(ASSETS, "capa-elos.jpg"), quality=92, subsampling=0, optimize=True)
        print("final ok", im.size)
