#! /usr/bin/env python
# coding=utf-8
from .bmfont_base import *
import re


def _get_str(s, tag):
    return re.search(r'%s="?(.*?)[" ]' % tag, s).group(1)


def _get_int(s, tag):
    m = re.search(r"%s=(-?\d+)" % tag, s)
    if m:
        return int(m.group(1))
    else:
        return 0


def _get_list(s, tag, num):
    p = r"%s=" % tag + ",".join([r"(\d+)" for i in range(num)])
    m = re.search(p, s)
    return [int(x) for x in m.groups()]


class InfoTxt(InfoBase):
    def load(self, io):
        line = io.readline()
        self.face = _get_str(line, "face")
        self.size = _get_int(line, "size")
        self.bold = _get_int(line, "bold")
        self.italic = _get_int(line, "italic")
        self.charset = _get_str(line, "charset")
        self.unicode = _get_int(line, "unicode")
        self.stretchH = _get_int(line, "stretchH")
        self.smooth = _get_int(line, "smooth")
        self.aa = _get_int(line, "aa")
        self.padding = _get_list(line, "padding", 4)
        self.spacing = _get_list(line, "spacing", 2)
        self.outline = _get_int(line, "outline")

    def save(self, io):
        io.write('info face="%s" size=%d bold=%d italic=%d charset="%s" unicode=%d stretchH=%d smooth=%d aa=%d padding=%d,%d,%d,%d spacing=%d,%d outline=%d\r\n' % (
            self.face,
            self.size,
            self.bold,
            self.italic,
            self.charset,
            self.unicode,
            self.stretchH,
            self.smooth,
            self.aa,
            self.padding[0],
            self.padding[1],
            self.padding[2],
            self.padding[3],
            self.spacing[0],
            self.spacing[1],
            self.outline,
        ))


class CommonTxt(CommonBase):
    def load(self, io):
        line = io.readline()
        self.lineHeight = _get_int(line, "lineHeight")
        self.base = _get_int(line, "base")
        self.scaleW = _get_int(line, "scaleW")
        self.scaleH = _get_int(line, "scaleH")
        self.pages = _get_int(line, "pages")
        self.packed = _get_int(line, "packed")
        self.alphaChnl = _get_int(line, "alphaChnl")
        self.redChnl = _get_int(line, "redChnl")
        self.greenChnl = _get_int(line, "greenChnl")
        self.blueChnl = _get_int(line, "blueChnl")

    def save(self, io):
        io.write('common lineHeight=%d base=%d scaleW=%d scaleH=%d pages=%d packed=%d alphaChnl=%d redChnl=%d greenChnl=%d blueChnl=%d\r\n' % (
            self.lineHeight,
            self.base,
            self.scaleW,
            self.scaleH,
            self.pages,
            self.packed,
            self.alphaChnl,
            self.redChnl,
            self.greenChnl,
            self.blueChnl,
        ))


class PagesTxt(PagesBase):
    def __init__(self, io=None, num=1):
        if io:
            self.load(io, num)

    def load(self, io, num):
        for i in range(num):
            line = io.readline()
            id = _get_int(line, "id")
            name = _get_str(line, "file")
            if id != i:
                raise
            self.append(name)

    def save(self, io):
        for i, name in enumerate(self):
            io.write('page id=%d file="%s"\r\n' % (i, name))


class CharsTxt(CharsBase):
    def load(self, io):
        count = _get_int(io.readline(), "count")
        for i in range(count):
            line = io.readline()
            char = {}
            char["id"] = _get_int(line, "id")
            char["x"] = _get_int(line, "x")
            char["y"] = _get_int(line, "y")
            char["width"] = _get_int(line, "width")
            char["height"] = _get_int(line, "height")
            char["xoffset"] = _get_int(line, "xoffset")
            char["yoffset"] = _get_int(line, "yoffset")
            char["xadvance"] = _get_int(line, "xadvance")
            char["page"] = _get_int(line, "page")
            char["chnl"] = _get_int(line, "chnl")
            self.append(char)

    def save(self, io):
        io.write("chars count=%d\r\n" % len(self))
        for char in self:
            io.write("char id=%-4d x=%-5d y=%-5d width=%-5d height=%-5d xoffset=%-5d yoffset=%-5d xadvance=%-5d page=%-2d chnl=%-2d\r\n" % (
                char["id"],
                char["x"],
                char["y"],
                char["width"],
                char["height"],
                char["xoffset"],
                char["yoffset"],
                char["xadvance"],
                char["page"],
                char["chnl"],
            ))


class KerningsTxt(KerningsBase):
    def load(self, io):
        try:
            count = _get_int(io.readline(), "count")
        except StopIteration:
            count = 0
        for i in range(count):
            line = io.next()
            kerning = {}
            kerning["first"] = _get_int(line, "first")
            kerning["second"] = _get_int(line, "second")
            kerning["amount"] = _get_int(line, "amount")
            self.append(kerning)

    def save(self, io):
        io.write("kernings count=%d\r\n" % len(self))
        for kerning in self:
            io.write("kerning first=%-3d  second=%-3d  amount=%-4d\r\n" % (
                kerning["first"],
                kerning["second"],
                kerning["amount"],
            ))


class FntTxt(FntBase):
    def load(self, io):
        self.info = InfoTxt(io)
        self.common = CommonTxt(io)
        self.pages = PagesTxt(io, self.common.pages)
        self.chars = CharsTxt(io)
        self.kernings = KerningsTxt(io)

    def save(self, io):
        self.info.save(io)
        self.common.save(io)
        self.pages.save(io)
        self.chars.save(io)
        self.kernings.save(io)

    def convert(self, fnt):
        info = InfoTxt()
        info.copy(fnt.info)
        self.info = info

        common = CommonTxt()
        common.copy(fnt.common)
        self.common = common

        pages = PagesTxt()
        pages.copy(fnt.pages)
        self.pages = pages

        chars = CharsTxt()
        chars.copy(fnt.chars)
        self.chars = chars

        kernings = KerningsTxt()
        kernings.copy(fnt.kernings)
        self.kernings = kernings
