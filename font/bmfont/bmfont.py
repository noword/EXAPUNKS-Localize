#! /usr/bin/env python
# coding=utf-8
from .bmfont_txt import FntTxt
from .bmfont_bin import FntBin
from .bmfont_xml import FntXml
import os
from PIL import Image


class Fnt(FntTxt, FntBin, FntXml):
    _class = {
        "bin": FntBin,
        "xml": FntXml,
        "txt": FntTxt,
    }

    def load(self, io):
        sign = io.read(3)
        io.seek(0, os.SEEK_SET)

        if sign == FntBin.SIGNATURE:
            self.format = "bin"
        elif sign == FntXml.SIGNATURE:
            self.format = "xml"
        else:
            self.format = "txt"
        self._class[self.format].load(self, io)

    def save(self, io):
        self._class[self.format].save(self, io)

    def convert(self, format):
        self.format = format
        self._class[format].convert(self, self)

    def __str__(self):
        return str(self.info) + str(self.common) + str(self.pages) + str(self.chars)

    def get_chars(self):
        return u"".join([chr(c["id"]) for c in self.chars])

    def dump_chars(self):
        ims = []
        for page in self.pages:
            im = Image.open(page)
            ims.append(im)

        for c in self.chars:
            im = ims[c["page"]]
            cim = im.crop((c["x"], c["y"], c["x"] + c["width"], c["y"] + c["height"]))
            cim.save("%04x.png" % c["id"])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("name", action="store", nargs=1)
    parser.add_argument("--dump_chars", action="store_true", default=False)
    args = parser.parse_args()

    fnt = Fnt(open(args.name[0], "rb"))
    if args.dump_chars:
        fnt.dump_chars()
    else:
        print(fnt)
