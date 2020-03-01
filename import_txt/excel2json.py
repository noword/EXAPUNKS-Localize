#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import os
import argparse


def convert(excel_name, json_name):
    if os.path.exists(json_name) and input('file "%s" exists, overwrite? [Y/N]' % json_name).lower() != 'y':
        return
    print('%s ==> %s' % (excel_name, json_name))
    df = pd.read_excel(excel_name)
    json_str = df.to_json(force_ascii=False, indent=4)
    open(json_name, 'w', encoding='utf-8').write(json_str)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('excel_name', action='store', nargs="?")
    parser.add_argument('json_name', action='store', nargs="?")
    args = parser.parse_args()

    if args.json_name is not None and args.excel_name is not None:
        convert(args.excel_name, args.json_name)
    else:
        for root, dirs, files in os.walk(os.path.dirname(os.path.realpath(__file__))):
            for f in files:
                if '~$' in f:
                    continue
                excel_name = os.path.join(root, f)
                name, ext = os.path.splitext(excel_name)
                if ext.lower() in ('.xls', '.xlsx'):
                    json_name = name + '.json'
                    convert(excel_name, json_name)
