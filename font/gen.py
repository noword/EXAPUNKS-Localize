#! /usr/bin/env python
# coding=utf-8
from PIL import Image
import os
from bmfont import FontGenerator
from collections import OrderedDict
from bmfont import Fnt
from packedfont import PackedFont
import sys


def do(name, width=512, height=512):
    print(name)
    pf = PackedFont(open(name, "rb"))
    size = int(pf.f0)
    if size < 13:
        size = 13
    print(pf.f0, pf.f1, pf.f2, size)
    font_gen = FontGenerator()

    texts = TEXTS
    pf.f2 *= 1.5

    font_gen.set_font_name("Arial Unicode MS")
    font_gen.set_font_size(-size)
    font_gen.set_texture_format("png")
    font_gen.set_chars(texts)
    font_gen.set_texture_size(width, height)
    font_gen.set_fixed_height(True)
    font_gen.set_enable_kernings(False)
    font_gen.set_spacing(3)

    if "bold" in name:
        font_gen.set_font_bold(True)

    if 'italic' in name:
        font_gen.set_font_italic(True)

    fnt = font_gen.gen()

    pf.set_chars(u"".join([chr(c["id"]) for c in fnt.chars]))
    pf.textures = []
    for page in fnt.pages:
        im = Image.open(page).transpose(Image.FLIP_TOP_BOTTOM)
        _, _, _, im = im.split()
        pf.textures.append(im)

    pf.glyphs = []
    for c in fnt.chars:
        pf.glyphs.append({
            "index": c["page"],
            "x": c["x"],
            "y": height - c["y"] - c["height"],
            "w": c["width"],
            "h": c["height"],
            "offsetx": c["xoffset"],
            "offsety": size - fnt.common.base - 3,
            "adv": c["xadvance"]
        })

    pf.save(open(os.path.split(name)[1], "wb"))


if __name__ == "__main__":
    TEXTS = open("chars.txt", "r", encoding='utf-8').read()

    codes = [[ord(TEXTS[0]), ord(TEXTS[0])], ]
    for t in TEXTS[1:]:
        t = ord(t)
        if codes[-1][1] + 1 == t:
            codes[-1][1] += 1
        else:
            codes.append([t, t])

    # for i, c in enumerate(codes):
        # print i, c

    for root, dirs, files in os.walk("fonts"):
        for f in files:
            if 'mono' not in f:
                do(os.path.join(root, f))
