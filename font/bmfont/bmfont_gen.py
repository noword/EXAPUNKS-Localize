#! /usr/bin/env python
# coding=utf-8
from collections import OrderedDict
from io import StringIO
import os
from .bmfont import Fnt
import math
from PIL import Image
import uuid

path = os.path.dirname(os.path.realpath(__file__))
BMFONT_COM = os.path.join(path, "bmfont.com")


class FontGenerator:
    chars = u"".join([chr(x) for x in range(20, 0x7f)])
    args = OrderedDict((
        ("fileVersion", "1"),
        ("fontName", "Arial"),
        ("fontFile", ""),
        ("charSet", "134"),
        ("fontSize", 32),
        ("aa", "1"),
        ("scaleH", "100"),
        ("useSmoothing", "1"),
        ("isBold", "0"),
        ("isItalic", "0"),
        ("useUnicode", "1"),
        ("disableBoxChars", "0"),
        ("outputInvalidCharGlyph", "0"),
        ("dontIncludeKerningPairs", "1"),
        ("useHinting", "1"),
        ("renderFromOutline", "0"),
        ("useClearType", "1"),
        ("paddingDown", "0"),
        ("paddingUp", "0"),
        ("paddingRight", "0"),
        ("paddingLeft", "0"),
        ("spacingHoriz", "1"),
        ("spacingVert", "1"),
        ("useFixedHeight", "0"),
        ("forceZero", "0"),
        ("outWidth", "256"),
        ("outHeight", "256"),
        ("outBitDepth", "32"),
        ("fontDescFormat", "0"),
        ("fourChnlPacked", "0"),
        ("textureFormat", "png"),
        ("textureCompression", "0"),
        ("alphaChnl", "1"),
        ("redChnl", "0"),
        ("greenChnl", "0"),
        ("blueChnl", "0"),
        ("invA", "0"),
        ("invR", "0"),
        ("invG", "0"),
        ("invB", "0"),
        ("outlineThickness", "0"),))

    def __init__(self, name=u"Arial Unicode MS", size=20, bold=False, italic=False):
        self.uuid = str(uuid.uuid4())
        self.set_font_name(name)
        self.set_font_size(size)
        self.set_font_bold(bold)
        self.set_font_italic(italic)
        self.icons = []

    def Gen(self, texts, fix_height=True):
        self.set_chars(texts)
        self.adjust_texture_size()
        # self.set_texture_format("png")
        self.set_fixed_height(fix_height)
        fnt = self.gen()
        while len(fnt.pages) > 1:
            w, h = self.get_texture_size()
            if w > h:
                self.set_texture_size(w, h * 2)
            else:
                self.set_texture_size(w * 2, h)
            fnt = self.gen()
        for c in fnt.chars:
            c["w"] = c["width"]
            c["h"] = c["height"]
            c["x0"] = c["x"]
            c["y0"] = c["y"]
            c["x1"] = c["x0"] + c["w"]
            c["y1"] = c["y0"] + c["h"]
            c["left"] = c["xoffset"]
            c["top"] = c["yoffset"]
            c["adv"] = c["xadvance"]
        self.im = Image.open(fnt.pages[0])
        infos = dict(zip([chr(c["id"]) for c in fnt.chars], fnt.chars))
        for t in texts:
            if t not in infos:
                infos[t] = infos[" "].copy()
        return infos

    def GetRgbaImage(self):
        return self.im

    def GetImage(self):
        return self.im.split()[3]

    def __setitem__(self, key, value):
        self.args[key] = value

    def __getitem__(self, key):
        return self.args[key]

    def set_chars(self, chars):
        self.chars = chars
        self.adjust_texture_size()

    def get_bmfc(self):
        io = StringIO()
        for k, v in self.args.items():
            io.write("%s=%s\n" % (k, str(v)))

        chars = []
        for i, c in enumerate(self.chars):
            if i % 16 == 15:
                io.write("chars=%s\n" % (",".join(chars)))
                chars = []
            chars.append("%d" % (ord(c)))
        io.write("chars=%s\n\n" % (",".join(chars)))
        for icon in self.icons:
            io.write('icon="%s",%d,%d,%d,%d\n' % (icon["name"], icon["id"], icon["xoffset"], icon["yoffset"], icon["xadvance"]))
        return io.getvalue()

    def save_bmfc(self, io):
        io.write(self.get_bmfc())

    def clone(self, fnt):
        # self.set_font_size(-fnt.common.lineHeight*0.8)
        self.set_font_size(fnt.info.size)
        self.set_font_bold(fnt.info.bold)
        self.set_font_italic(fnt.info.italic)
        if fnt.info.outline > 3:
            self.set_outline(3)
        else:
            self.set_outline(fnt.info.outline)
        self["alphaChnl"] = fnt.common.alphaChnl
        self["redChnl"] = fnt.common.redChnl
        self["greenChnl"] = fnt.common.greenChnl
        self["blueChnl"] = fnt.common.blueChnl
        self.adjust_texture_size()
        self["fontDescFormat"] = {"txt": 0, "xml": 1, "bin": 2}[fnt.format]
        self["paddingDown"], self["paddingUp"], self["paddingRight"], self["paddingLeft"] = fnt.info.padding
        try:
            self.set_texture_format(os.path.splitext(fnt.pages[0])[1][1:])
        except BaseException:
            pass

    def gen(self, fnt_name=None):
        if fnt_name is None:
            name = self.uuid
            fnt_name = name + '.fnt'
            bmfc_name = name + '.bmfc'
        else:
            bmfc_name = os.path.splitext(fnt_name)[0] + '.bmfc'
        self.save_bmfc(open(bmfc_name, "w"))
        if os.path.exists(fnt_name):
            os.remove(fnt_name)
        os.system('"%s" -c %s -o %s' % (BMFONT_COM, bmfc_name, fnt_name))
        fnt = Fnt(open(fnt_name, "r"))
        return fnt

    def clear(self, fnt_name=None):
        if fnt_name is None:
            name = self.uuid
            fnt_name = name + '.fnt'
            bmfc_name = name + '.bmfc'
        else:
            bmfc_name = os.path.splitext(fnt_name)[0] + '.bmfc'

        os.remove(bmfc_name)
        fnt = Fnt(open(fnt_name, "r"))
        for page in fnt.pages:
            os.remove(page)
        os.remove(fnt_name)

    def set_font_name(self, name):
        self["fontName"] = name

    def set_font_desc_format(self, fmt):
        self["fontDescFormat"] = {"txt": 0, "xml": 1, "bin": 2}[fmt]

    def set_font_size(self, size):
        self["fontSize"] = size

    def set_font_bold(self, bold):
        if isinstance(bold, bool):
            bold = "1" if bold else "0"
        self["isBold"] = bold

    def set_font_italic(self, italic):
        if isinstance(italic, bool):
            italic = "1" if italic else "0"
        self["isItalic"] = italic

    def set_texture_format(self, format):
        valid_format = ("png", "tga", "dds")
        if format not in valid_format:
            raise TypeError("valid format: %s" % (str(valid_format)))
        self["textureFormat"] = format

    def set_texture_compression(self, compression):
        valid_compression = ("none", "dxt1", "dxt3", "dxt5")
        if compression not in valid_compression:
            raise TypeError("valid compression: %s" % (str(valid_compression)))
        self["textureCompression"] = valid_compression.index(compression)

    def set_texture_size(self, width, height):
        self["outWidth"] = width
        self["outHeight"] = height

    def get_texture_size(self):
        return self["outWidth"], self["outHeight"]

    def set_fixed_height(self, is_fixed_height):
        self["useFixedHeight"] = "%d" % is_fixed_height

    def set_force_zero(self, is_force_zero):
        self["forceZero"] = "%d" % is_force_zero

    def set_outline(self, outline):
        self["outlineThickness"] = outline
        if outline == 0:
            self["alphaChnl"] = 0
        else:
            self["alphaChnl"] = 1

    def set_enable_kernings(self, enable_kernings):
        self["dontIncludeKerningPairs"] = "%d" % (not enable_kernings)

    def adjust_texture_size(self):
        font_size = int(abs(self["fontSize"]))
        if self["fontSize"] > 0:
            font_size = int(font_size * 0.8)
        minsize = (font_size + int(self["paddingDown"]) + int(self["paddingUp"])) * \
            (font_size + int(self["paddingRight"]) + int(self["paddingLeft"])) * len(self.chars)
        minsize *= 1.1
        w = h = 2
        while w * h < minsize:
            if w > h:
                h *= 2
            else:
                w *= 2
        self.set_texture_size(w, h)

    def add_icon(self, name, id, xoffset=0, yoffset=0, xadvance=0):
        self.icons.append({"name": name, "id": id, "xoffset": xoffset, "yoffset": yoffset, "xadvance": xadvance})

    def set_spacing(self, v):
        self["spacingHoriz"] = self["spacingVert"] = v

    def set_padding(self, v):
        self["paddingDown"] = self["paddingUp"] = self["paddingRight"] = self["paddingLeft"] = v

    def set_four_chnl_packed(self):
        self["fourChnlPacked"] = 1
        self["alphaChnl"] = 1
        self["redChnl"] = 1
        self["greenChnl"] = 1
        self["blueChnl"] = 1


def FixFnt(new_fnt, old_fnt):
    new_fnt.info.face = old_fnt.info.face
    new_fnt.info.unicode = 1
    return new_fnt


if __name__ == "__main__":
    fontgen = FontGenerator()
    fontgen.set_chars(u"abc")
    print(fontgen.gen())
