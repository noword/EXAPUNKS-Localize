#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import os
import argparse


def convert(json_name, excel_name):
    if os.path.exists(excel_name) and input('file "%s" exists, overwrite? [Y/N]' % excel_name).lower() != 'y':
        return
    print('%s ==> %s' % (json_name, excel_name))
    df = pd.read_json(json_name, encoding='utf-8')
    df.replace(float('nan'), '', inplace=True)
    english_index = df.columns.to_list().index('English') + 2
    df.to_excel(excel_name, freeze_panes=(1, english_index))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('json_name', action='store', nargs="?")
    parser.add_argument('excel_name', action='store', nargs="?")
    args = parser.parse_args()

    if args.json_name is not None and args.excel_name is not None:
        convert(args.json_name, args.excel_name)
    else:
        for root, dirs, files in os.walk(os.path.dirname(os.path.realpath(__file__))):
            for f in files:
                json_name = os.path.join(root, f)
                name, ext = os.path.splitext(json_name)
                if ext.lower() == '.json':
                    excel_name = name + '.xlsx'
                    convert(json_name, excel_name)
