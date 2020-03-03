#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse
from convert import convert, convert_all


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('json_name', action='store', nargs="?")
    parser.add_argument('excel_name', action='store', nargs="?")
    args = parser.parse_args()

    if args.json_name is not None:
        excel_name = args.excel_name
        if excel_name is None:
            excel_name = os.path.splitext(args.json_name)[0] + '.xlsx'
        convert(args.json_name, excel_name)
    else:
        convert_all('.json', '.xlsx')
