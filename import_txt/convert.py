#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from translation import Translation


def convert(input_name, output_name):
    if os.path.exists(output_name) and input('file "%s" exists, overwrite? [Y/N]' % output_name).lower() == 'y':
        print('%s ==> %s' % (input_name, output_name))
        Translation(input_name).save(output_name)


def convert_all(input_ext, output_ext):
    input_ext = input_ext.lower()
    output_ext = output_ext.lower()
    for root, dirs, files in os.walk(os.path.dirname(os.path.realpath(__file__))):
        for f in files:
            if '~$' in f:  # excel temp file
                continue
            input_name = os.path.join(root, f)
            name, ext = os.path.splitext(input_name)
            if ext.lower() == input_ext:
                output_name = name + output_ext
                convert(input_name, output_name)
