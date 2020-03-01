#! /usr/bin/env python
# coding=utf-8
from .bmfont_base import *
from xml.etree import ElementTree
from xml.dom import minidom
from io import StringIO


def prettify(elem):
    s = ElementTree.tostring(elem, "utf-8")
    reparsed = minidom.parseString(s)
    return reparsed.toprettyxml(indent="  ")


class InfoXml(InfoBase):
    def load(self, node):
        self.face = node.attrib.get("face")
        self.size = int(node.attrib.get("size"))
        self.bold = int(node.attrib.get("bold"))
        self.italic = int(node.attrib.get("italic"))
        self.charset = node.attrib.get("charset")
        self.unicode = int(node.attrib.get("unicode"))
        self.stretchH = int(node.attrib.get("stretchH"))
        self.smooth = int(node.attrib.get("smooth"))
        self.aa = int(node.attrib.get("aa"))
        self.padding = [int(x) for x in node.attrib.get("padding").split(",")]
        self.spacing = [int(x) for x in node.attrib.get("spacing").split(",")]
        self.outline = int(node.attrib.get("outline"))

    def save(self, root):
        info = ElementTree.SubElement(root, "info")
        info.set("face", self.face)
        info.set("size", str(self.size))
        info.set("smooth", str(self.smooth))
        info.set("unicode", str(self.unicode))
        info.set("italic", str(self.italic))
        info.set("bold", str(self.bold))
        info.set("charset", self.charset)
        info.set("stretchH", str(self.stretchH))
        info.set("aa", str(self.aa))
        info.set("padding", ",".join([str(x) for x in self.padding]))
        info.set("spacing", ",".join([str(x) for x in self.spacing]))
        info.set("outline", str(self.outline))


class CommonXml(CommonBase):
    def load(self, node):
        self.lineHeight = int(node.attrib.get("lineHeight"))
        self.base = int(node.attrib.get("base"))
        self.scaleW = int(node.attrib.get("scaleW"))
        self.scaleH = int(node.attrib.get("scaleH"))
        self.pages = int(node.attrib.get("pages"))
        self.packed = int(node.attrib.get("packed"))
        try:
            self.alphaChnl = int(node.attrib.get("alphaChnl"))
            self.redChnl = int(node.attrib.get("redChnl"))
            self.greenChnl = int(node.attrib.get("greenChnl"))
            self.blueChnl = int(node.attrib.get("blueChnl"))
        except TypeError:
            self.alphaChnl = 1
            self.redChnl = 0
            self.greenChnl = 0
            self.blueChnl = 0

    def save(self, root):
        common = ElementTree.SubElement(root, "common")
        common.set("lineHeight", str(self.lineHeight))
        common.set("base", str(self.base))
        common.set("scaleW", str(self.scaleW))
        common.set("scaleH", str(self.scaleH))
        common.set("pages", str(self.pages))
        common.set("packed", str(self.packed))
        common.set("alphaChnl", str(self.alphaChnl))
        common.set("redChnl", str(self.redChnl))
        common.set("greenChnl", str(self.greenChnl))
        common.set("blueChnl", str(self.blueChnl))


class PagesXml(PagesBase):
    def load(self, node):
        names = {}
        for page in node.iter("page"):
            id = int(page.attrib.get("id"))
            names[id] = page.attrib.get("file")

        for i in range(len(names)):
            self.append(names[i])

    def save(self, root):
        pages = ElementTree.SubElement(root, "pages")
        for i, name in enumerate(self):
            page = ElementTree.SubElement(pages, "page")
            page.set("id", str(i))
            page.set("file", name)


class CharsXml(CharsBase):
    def load(self, node):
        for char in node.iter("char"):
            for key, value in char.attrib.items():
                char.attrib[key] = int(value)
            self.append(char.attrib)

    def save(self, root):
        chars = ElementTree.SubElement(root, "chars")
        chars.set("count", str(len(self)))

        self.sort(key=lambda x: int(x["id"]))
        for c in self:
            char = ElementTree.SubElement(chars, "char")
            char.set("id", str(c["id"]))
            char.set("x", str(c["x"]))
            char.set("y", str(c["y"]))
            char.set("width", str(c["width"]))
            char.set("height", str(c["height"]))
            char.set("xoffset", str(c["xoffset"]))
            char.set("yoffset", str(c["yoffset"]))
            char.set("xadvance", str(c["xadvance"]))
            char.set("page", str(c["page"]))
            char.set("chnl", str(c["chnl"]))


class KerningsXml(KerningsBase):
    def load(self, node):
        for kerning in node.iter("kerning"):
            for key, value in kerning.attrib.items():
                kerning.attrib[key] = int(value)
            self.append(kerning.attrib)

    def save(self, root):
        kernings = ElementTree.SubElement(root, "kernings")
        kernings.set("count", str(len(self)))
        for k in self:
            kerning = ElementTree.SubElement(kernings, "kerning")
            kerning.set("first", str(k["first"]))
            kerning.set("second", str(k["second"]))
            kerning.set("amount", str(k["amount"]))


class FntXml(FntBase):
    SIGNATURE = "<?x"

    def load(self, io):
        io = StringIO(io.read())
        tree = ElementTree.parse(io)

        self.info = InfoXml(tree.iter("info").next())
        self.common = CommonXml(tree.iter("common").next())
        self.pages = PagesXml(tree.iter("pages").next())
        self.chars = CharsXml(tree.iter("chars").next())
        try:
            self.kernings = KerningsXml(tree.iter("kernings").next())
        except BaseException:
            self.kernings = None

    def save(self, io):
        top = ElementTree.Element("font")

        self.info.save(top)
        self.common.save(top)
        self.pages.save(top)
        self.chars.save(top)
        if self.kernings:
            self.kernings.save(top)

        io.write(prettify(top))

    def convert(self, fnt):
        info = InfoXml()
        info.copy(fnt.info)
        self.info = info

        common = CommonXml()
        common.copy(fnt.common)
        self.common = common

        pages = PagesXml()
        pages.copy(fnt.pages)
        self.pages = pages

        chars = CharsXml()
        chars.copy(fnt.chars)
        self.chars = chars

        kernings = KerningsXml()
        kernings.copy(fnt.kernings)
        self.kernings = kernings
