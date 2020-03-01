#! /usr/bin/env python
# coding=utf-8
from io import StringIO


class Base:
    def __init__(self, io=None):
        if io is not None:
            self.load(io)

    def load(self, io):
        raise NotImplementedError

    def save(self, io):
        raise NotImplementedError

    def get_data(self):
        io = StringIO()
        self.save(io)
        return io.getvalue()


class InfoBase(Base):
    face = ""
    size = 32
    bold = 0
    italic = 0
    charset = ""
    unicode = 1
    stretchH = 100
    smooth = 1
    aa = 1
    padding = [0, 0, 0, 0]
    spacing = [1, 1]
    outline = 0

    def copy(self, info):
        self.face = info.face
        self.size = info.size
        self.bold = info.bold
        self.italic = info.italic
        self.charset = info.charset
        self.unicode = info.unicode
        self.stretchH = info.stretchH
        self.smooth = info.smooth
        self.aa = info.aa
        self.padding = info.padding
        self.spacing = info.spacing
        self.outline = info.outline

    def __str__(self):
        values = InfoBase.__dict__
        values.update(self.__dict__)
        return "    face:%(face)s\n"\
               "    size:%(size)s\n"\
               "    bold:%(bold)s\n"\
               "  italic:%(italic)s\n"\
               " charset:%(charset)s\n"\
               " unicode:%(unicode)s\n"\
               "stretchH:%(stretchH)s\n"\
               "  smooth:%(smooth)s\n"\
               "      aa:%(aa)s\n"\
               " padding:%(padding)s\n"\
               " spacing:%(spacing)s\n"\
               " outline:%(outline)s\n"\
               % values


class CommonBase(Base):
    lineHeight = 32
    base = 26
    scaleW = 256
    scaleH = 256
    pages = 1
    packed = 0
    alphaChnl = 1
    redChnl = 0
    greenChnl = 0
    blueChnl = 0

    def copy(self, common):
        self.lineHeight = common.lineHeight
        self.base = common.base
        self.scaleW = common.scaleW
        self.scaleH = common.scaleH
        self.pages = common.pages
        self.packed = common.packed
        self.alphaChnl = common.alphaChnl
        self.redChnl = common.redChnl
        self.greenChnl = common.greenChnl
        self.blueChnl = common.blueChnl

    def __str__(self):
        values = CommonBase.__dict__
        values.update(self.__dict__)
        return "lineHeight:%(lineHeight)s\n"\
               "      base:%(base)s\n"\
               "    scaleW:%(scaleW)s\n"\
               "    scaleH:%(scaleH)s\n"\
               "     pages:%(pages)s\n"\
               "    packed:%(packed)s\n"\
               " alphaChnl:%(alphaChnl)s\n"\
               "   redChnl:%(redChnl)s\n"\
               " greenChnl:%(greenChnl)s\n"\
               "  blueChnl:%(blueChnl)s\n" % values


class PagesBase(Base, list):
    def copy(self, obj):
        for i in range(len(self)):
            self.pop()
        for x in obj:
            self.append(x)

    def __str__(self):
        return "\n".join(self) + "\n"


class CharsBase(Base, list):
    def copy(self, obj):
        for i in range(len(self)):
            self.pop()
        for x in obj:
            self.append(x)

    def __str__(self):
        return "\n".join([str(c) for c in self]) + "\n"


class KerningsBase(Base, list):
    def copy(self, obj):
        for i in range(len(self)):
            self.pop()
        for x in obj:
            self.append(x)


class FntBase(Base):
    version = 3
