#! /usr/bin/env python
# coding=utf-8
from PIL import Image
import os
from bmfont import FontGenerator
from collections import OrderedDict
from bmfont import Fnt
from packedfont import PackedFont
import threading
import queue
import multiprocessing

'''
free fonts:
https://sourceforge.net/projects/wqy/files/wqy-microhei/0.2.0-beta/
https://www.google.com/get/noto/help/cjk/
https://github.com/adobe-fonts/source-han-sans
https://github.com/be5invis/Sarasa-Gothic
https://github.com/adobe-fonts/source-han-mono
'''

MONO_FONT = 'Source Han Mono'
REGULAR_FONT = 'Source Han Sans'
LIGHT_FONT = 'Source Han Sans Light'

FONT_MAP = {
    'mono': (MONO_FONT, 1.2, False),
    'pixel': (MONO_FONT, 1.3, False),
    'karnivore': (REGULAR_FONT, 1.3, True),
    'impact': (REGULAR_FONT, 1.3, True),
    'archivo': (REGULAR_FONT, 1.3, True),
    'devalencia': (REGULAR_FONT, 1.3, False),
    'michroma': (LIGHT_FONT, 1.4, False),
    'roboto': (REGULAR_FONT, 1.3, False),
}


def do(name, width=512, height=512):
    print(name)
    pf = PackedFont(open(name, "rb"))
    size = int(pf.f2)
    if size < 13:
        size = 13
    print(pf.f0, pf.f1, pf.f2, size)
    font_gen = FontGenerator()

    font_gen.set_font_name(REGULAR_FONT)
    font_gen.set_font_size(size)
    for oname, (mname, scale, bold) in FONT_MAP.items():
        if oname in name:
            font_gen.set_font_name(mname)
            font_gen.set_font_size(int(size * scale))
            font_gen.set_font_bold(bold)
            break

    font_gen.set_texture_format("png")
    font_gen.set_chars(TEXTS)
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
            "offsety": c["yoffset"] - 3 - (fnt.common.lineHeight - fnt.common.base),
            "adv": c["xadvance"]
        })

    pf.save(open(os.path.split(name)[1], "wb"))

    font_gen.clear()


def fontgen_thread(q):
    while True:
        name = q.get()
        do(name)
        q.task_done()


if __name__ == "__main__":
    TEXTS = open("chars.txt", "r", encoding='utf-8').read()

    codes = [[ord(TEXTS[0]), ord(TEXTS[0])], ]
    for t in TEXTS[1:]:
        t = ord(t)
        if codes[-1][1] + 1 == t:
            codes[-1][1] += 1
        else:
            codes.append([t, t])

    task_queue = queue.Queue()
    for i in range(multiprocessing.cpu_count() - 1):
        job = threading.Thread(target=fontgen_thread, args=(task_queue, ))
        job.setDaemon(True)
        job.start()

    for root, dirs, files in os.walk("fonts"):
        for f in files:
            task_queue.put(os.path.join(root, f))

    task_queue.join()
