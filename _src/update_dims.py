#!/usr/bin/env python3
"""Record width/height of every design image so build.py can lay them out proportionally.
Requires ImageMagick (`magick`). Run from anywhere: python3 _src/update_dims.py
"""
import json, os, subprocess
here = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(here, "..", "assets", "img", "design")
out = subprocess.run(["magick", "identify", "-format", "%f %w %h\n"] + sorted(
    os.path.join(img_dir, f) for f in os.listdir(img_dir) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))),
    capture_output=True, text=True, check=True).stdout
dims = {}
for line in out.splitlines():
    f, w, h = line.split()
    dims[f] = [int(w), int(h)]
with open(os.path.join(here, "image_dims.json"), "w") as fh:
    json.dump(dims, fh, indent=0)
print(f"saved {len(dims)} image sizes")
