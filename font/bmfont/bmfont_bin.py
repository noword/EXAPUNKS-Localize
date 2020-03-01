#! /usr/bin/env python
# coding=utf-8
from .bmfont_base import *
from io import StringIO
from struct import unpack, pack


def _get_str(io):
    s = ""
    t = io.read(1)
    while t != "" and t != "\x00":
        s += t
        t = io.read(1)
    return s


class InfoBin(InfoBase):
    def load(self, io):
        self.size, bit_field, charset, self.stretchH, self.aa, \
            self.padding[0], self.padding[1], self.padding[2], self.padding[3], \
            self.spacing[0], self.spacing[1], self.outline \
            = unpack("<h BB H 8B", io.read(0xe))

        self.smooth = bit_field >> 7
        self.unicode = (bit_field >> 6) & 1
        self.italic = (bit_field >> 5) & 1
        self.bold = (bit_field >> 4) & 1

        self.face = _get_str(io)

    def save(self, io):
        bit_field = (self.smooth << 7) | (self.unicode << 6) | (self.italic << 5) | (self.bold << 4)
        io.write(pack("<h BB H 8B", self.size, bit_field, 0, self.stretchH, self.aa,
                      self.padding[0], self.padding[1], self.padding[2], self.padding[3],
                      self.spacing[0], self.spacing[1], self.outline))

        io.write(self.face + "\x00")


class CommonBin(CommonBase):
    def load(self, io):
        self.lineHeight, self.base, self.scaleW, self.scaleH, self.pages, self.packed, \
            self.alphaChnl, self.redChnl, self.greenChnl, self.blueChnl \
            = unpack("<5H 5B", io.read(0xf))
        self.tail = io.read()

    def save(self, io):
        io.write(pack("<5H 5B", self.lineHeight, self.base, self.scaleW, self.scaleH, self.pages, self.packed,
                      self.alphaChnl, self.redChnl, self.greenChnl, self.blueChnl))
        io.write(self.tail)


class CommonBinV1(CommonBase):
    def load(self, io):
        self.lineHeight, self.base, self.scaleW, self.scaleH, self.pages, self.packed = \
            unpack("<5HB", io.read(0xb))

    def save(self, io):
        io.write(pack("<5HB", self.lineHeight, self.base, self.scaleW, self.scaleH, self.pages, self.packed))


class PagesBin(PagesBase):
    def load(self, io):
        while True:
            name = _get_str(io)
            if len(name) == 0:
                break
            self.append(name)

    def save(self, io):
        for name in self:
            io.write(name + "\x00")


class CharsBin(CharsBase):
    def load(self, io):
        while True:
            tmp = io.read(0x14)
            if len(tmp) != 0x14:
                break
            self.append(dict(zip(("id", "x", "y", "width", "height", "xoffset",
                                  "yoffset", "xadvance", "page", "chnl"), unpack("<I 7h 2B", tmp))))

    def save(self, io):
        self.sort(key=lambda x: int(x["id"]))
        for c in self:
            io.write(
                pack(
                    "<I 7h 2B",
                    c["id"],
                    c["x"],
                    c["y"],
                    c["width"],
                    c["height"],
                    c["xoffset"],
                    c["yoffset"],
                    c["xadvance"],
                    c["page"],
                    c["chnl"]))


class KerningsBin(KerningsBase):
    def load(self, io):
        while True:
            tmp = io.read(0xa)
            if len(tmp) != 0xa:
                break
            self.append(dict(zip(("first", "second", "amount"), unpack("<IIh", tmp))))

    def save(self, io):
        for p in self:
            io.write(pack("<IIh", p["first"], p["second"], p["amount"]))


class FntBin(FntBase):
    SIGNATURE = "BMF"

    def _load_block(self, io):
        # print "%x"%io.tell()
        index, length = unpack("<BI", io.read(5))
        if self.version == 1:
            length -= 4
        return io.read(length)

    def _save_block(self, io, index, buf):
        if self.version == 1:
            io.write(pack("<BI", index, len(buf) + 4))
        else:
            io.write(pack("<BI", index, len(buf)))
        io.write(buf)

    def load(self, io):
        if io.read(len(self.SIGNATURE)) != self.SIGNATURE:
            raise TypeError("wrong signature")

        self.version, = unpack("B", io.read(1))

        self.info = InfoBin(StringIO(self._load_block(io)))
        if self.version == 1:
            self.common = CommonBinV1(StringIO(self._load_block(io)))
        else:
            self.common = CommonBin(StringIO(self._load_block(io)))
        self.pages = PagesBin(StringIO(self._load_block(io)))
        self.chars = CharsBin(StringIO(self._load_block(io)))

        try:
            self.kernings = KerningsBin(StringIO(self._load_block(io)))
        except BaseException:
            self.kernings = None

    def save(self, io):
        io.write(self.SIGNATURE)
        io.write(pack("B", self.version))
        self._save_block(io, 1, self.info.get_data())
        self._save_block(io, 2, self.common.get_data())
        self._save_block(io, 3, self.pages.get_data())
        self._save_block(io, 4, self.chars.get_data())
        if self.kernings:
            self._save_block(io, 5, self.kernings.get_data())

    def convert(self, fnt):
        info = InfoBin()
        info.copy(fnt.info)
        self.info = info

        common = CommonBin()
        common.copy(fnt.common)
        self.common = common

        pages = PagesBin()
        pages.copy(fnt.pages)
        self.pages = pages

        chars = CharsBin()
        chars.copy(fnt.chars)
        self.chars = chars

        kernings = KerningsBin()
        kernings.copy(fnt.kernings)
        self.kernings = kernings
