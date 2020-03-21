#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


def gen_pdf(name):
    count = 1
    jpgs = []
    while True:
        page_name = f'{name}_{count:02d}'
        count += 1
        xcf_name = f'{page_name}.xcf'
        if os.path.exists(xcf_name):
            jpg_name = f'{page_name}.jpg'
            print(f'{xcf_name} ==> {jpg_name}')
            os.system(f'convert.exe {xcf_name} -flatten {jpg_name}')
            jpgs.append(jpg_name)
        else:
            break

    os.system(f'convert.exe {" ".join(jpgs)} {name}.pdf')


if __name__ == '__main__':
    gen_pdf('digital_en_1')
