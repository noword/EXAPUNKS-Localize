#! /usr/bin/env python
# coding=utf-8
from struct import unpack, pack
import os
from PIL import Image


class PackedFont:
    def __init__(self, io=None):
        if io:
            self.load(io)

    def load(self, io):
        self.f0, self.f1, self.f2, num = unpack("3fI", io.read(0x10))
        self.codes = []
        for i in range(num):
            self.codes.append(unpack("II", io.read(8)))

        num, = unpack("I", io.read(4))
        self.glyphs = []
        for i in range(num):
            self.glyphs.append(dict(zip(("index", "x", "y", "w", "h", "offsetx",
                                         "offsety", "adv"), unpack("I7f", io.read(0x20)))))

        num, = unpack("I", io.read(4))
        self.textures = []
        for i in range(num):
            w, h = unpack("II", io.read(8))
            buf = io.read(w * h)
            im = Image.new("L", (w, h))
            im.frombytes(buf)
            im = im.transpose(Image.FLIP_TOP_BOTTOM)
            self.textures.append(im)

    def save(self, io):
        io.write(pack("3fI", self.f0, self.f1, self.f2, len(self.codes)))
        for c in self.codes:
            io.write(pack("II", *c))

        io.write(pack("I", len(self.glyphs)))
        for g in self.glyphs:
            io.write(pack("I7f", g["index"], g["x"], g["y"], g["w"], g["h"], g["offsetx"], g["offsety"], g["adv"]))

        io.write(pack("I", len(self.textures)))
        for t in self.textures:
            io.write(pack("II", *(t.size)))
            io.write(t.tobytes())

    def get_chars(self):
        chars = u""
        for c in self.codes:
            chars += u"".join([chr(c) for c in range(c[0], c[1] + 1)])
        return chars

    def set_chars(self, chars):
        chars = [ord(c) for c in chars]
        self.codes = [[chars[0], chars[0]], ]
        for c in chars[1:]:
            if self.codes[-1][1] + 1 == c:
                self.codes[-1][1] += 1
            else:
                self.codes.append([c, c])


if __name__ == "__main__":
    import sys
    pf = PackedFont(open(sys.argv[1], "rb"))
    print(pf.f0, pf.f1, pf.f2)
    w, h = pf.textures[0].size
    chars = pf.get_chars()
    for i, g in enumerate(pf.glyphs):
        print('%x' % ord(chars[i]), g["index"], g["x"], g["y"], g["w"], g["h"], g["offsetx"], g["offsety"], g["adv"])
    for i, t in enumerate(pf.textures):
        pf.textures[i].save("%d.png" % i)
