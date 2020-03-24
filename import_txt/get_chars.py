#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

if __name__ == '__main__':
    chars = set('·’')
    chars |= set([chr(i) for i in range(0x20, 0x100)])
    for root, dirs, files in os.walk('./'):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext == '.json':
                chars |= set(open(os.path.join(root, f), 'r', encoding='utf-8').read())

    chars_list = sorted(filter(lambda x: ord(x) >= 0x20, chars))
    open('../font/chars.txt', 'w', encoding='utf-8').write(''.join(chars_list))
