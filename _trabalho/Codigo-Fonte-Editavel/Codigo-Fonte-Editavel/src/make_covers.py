#!/usr/bin/env python3
"""Variantes de enquadramento da capa (mesma cena, câmera própria para cada formato).
Uso: make_covers.py preview|final letter|mobile"""
import sys, os, time
from PIL import Image
import make_cover as M

VARIANTS = {
    # tz maior = corrente menor; ty desloca para cima; tx para a direita
    "letter": dict(ratio=(8.5, 11.0), pose=dict(M.POSE, tz=120.0, ty=4.8, tx=0.4), final=(2400, 3105)),
    "mobile": dict(ratio=(4.2, 7.47), pose=dict(M.POSE, tz=132.0, ty=8.3, tx=0.6), final=(1440, 2560)),
}
mode, name = sys.argv[1], sys.argv[2]
v = VARIANTS[name]
if mode == "preview":
    W = 420; H = round(W * v["ratio"][1] / v["ratio"][0])
    SS = 2
else:
    W, H = v["final"]; SS = 2
t = time.time()
raw = M.render(W, H, SS, os.path.join(M.BUILD, f"chain_{name}_{mode}.raw"), v["pose"])
im = M.compose(raw, (W, H))
if mode == "preview":
    im.save(os.path.join(M.BUILD, f"cover_{name}_preview.png"))
else:
    im.save(os.path.join(M.ASSETS, f"capa-{name}.png"), optimize=True)
    im.save(os.path.join(M.ASSETS, f"capa-{name}.jpg"), quality=92, subsampling=0, optimize=True)
    try: os.remove(os.path.join(M.BUILD, f"chain_{name}_{mode}.raw"))
    except OSError: pass
print(name, mode, (W, H), f"{time.time()-t:.1f}s")
