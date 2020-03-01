#!/usr/bin/env python
# -*- coding: utf-8 -*-
from struct import unpack, pack
from io import BytesIO
from PIL import Image
import lz4.block
import sys
import os


class Tex:
    SIGN = b'\xea\x03\x00\x00'

    def __init__(self, read_io=None):
        if read_io is not None:
            self.load(read_io)

    def load(self, read_io):
        if read_io.read(len(self.SIGN)) != self.SIGN:
            raise TypeError('wrong file type')

        self.width, self.height, self.type = unpack("<3I", read_io.read(0xc))
        self.dummy = read_io.read(0x28)
        zsize, = unpack('<I', read_io.read(4))
        self.zbuf = read_io.read(zsize)

    def save(self, write_io):
        write_io.write(self.SIGN)
        write_io.write(pack("<3I", self.width, self.height, self.type))
        write_io.write(self.dummy)
        write_io.write(pack('<I', len(self.zbuf)))
        write_io.write(self.zbuf)

    @property
    def image(self):
        size = self.width * self.height
        if self.type == 1:
            image_type = 'L'
        elif self.type == 2:
            image_type = 'RGBA'
            size *= 4
        else:
            raise TypeError('unknown type %x' % self.type)

        buf = lz4.block.decompress(self.zbuf, uncompressed_size=size)
        im = Image.new(image_type, (self.width, self.height))
        im.frombytes(buf)
        return im.transpose(Image.FLIP_TOP_BOTTOM)

    @image.setter
    def image(self, im):
        assert(im.size == (self.width, self.height))
        buf = im.tobytes()
        self.zbuf = lz4.block.compress(buf, store_size=False)


if __name__ == '__main__':
    tex = Tex(open(sys.argv[1], 'rb'))
    tex.image.save(os.path.splitext(sys.argv[1])[0] + '.png')
