#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse
from convert import convert, convert_all


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('excel_name', action='store', nargs="?")
    parser.add_argument('json_name', action='store', nargs="?")
    parser.add_argument('--auto', action='store_true')
    args = parser.parse_args()

    if args.excel_name is not None:
        json_name = args.json_name
        if json_name is None:
            json_name = os.path.splitext(args.excel_name)[0] + '.json'
        convert(args.excel_name, json_name, args.auto)
    else:
        convert_all('.xlsx', '.json', args.auto)
