#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from tex import Tex
from PIL import Image

if __name__ == '__main__':
    for root, dirs, files in os.walk('PackedContent'):
        for f in files:
            if os.path.splitext(f)[1].lower() == '.tex':
                name = os.path.join(root, f)
                new_name = os.path.join('new', name).replace('.tex', '.png')
                if os.path.exists(new_name):
                    print(name)
                    tex = Tex(open(name, 'rb'))
                    tex.image = Image.open(new_name)
                    patch_name = '../patch/' + name
                    try:
                        os.makedirs(os.path.split(patch_name)[0])
                    except BaseException:
                        pass
                    tex.save(patch_name)
