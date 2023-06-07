#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

# fonts used:
# 江城斜黑体
# 文泉驿微米黑
# 青鸟华光简淡古印
# 字心坊鸿潮榜书
# 造字工房哲黑（非商用）常规体 (removed)
# 造字工房羽逸(非商用）常规体
# 思源黑体
# 隶书
# MBitmapRoundHK-Light
# mplus_hzk_12


def need_update(xcf_name, jpg_name):
    if os.path.exists(jpg_name):
        xcf_time = os.path.getmtime(xcf_name)
        jpg_time = os.path.getmtime(jpg_name)
        return xcf_time > jpg_time
    return True


def gen_pdf(name):
    count = 0 if os.path.exists(f'{name}/{name}_00.xcf') else 1
    jpgs = []
    update = False
    while True:
        page_name = f'{name}/{name}_{count:02d}'
        count += 1
        xcf_name = f'{page_name}.xcf'
        if os.path.exists(xcf_name):
            jpg_name = f'{page_name}.jpg'
            if need_update(xcf_name, jpg_name):
                update = True
                print(f'{xcf_name} ==> {jpg_name}')
                quality = '-quality 80' if count > 2 else ''
                os.system(f'convert.exe {xcf_name} -flatten {quality} {jpg_name}')
            jpgs.append(jpg_name)
        else:
            break

    if update:
        print(f'generating {name}.pdf')
        os.system(f'convert.exe {" ".join(jpgs)} {name}.pdf')


if __name__ == '__main__':
    gen_pdf('digital_en_1')
    gen_pdf('digital_en_2')
