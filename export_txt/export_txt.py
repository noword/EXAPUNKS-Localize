#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import re
import os
import csv
import sys
sys.path.append('../import_txt')
from misc import get_trans


def export_vignettes():
    trans = get_trans('../import_txt/EXAPUNKS_vignettes.xlsx')
    original = set()
    data = []
    for root, dirs, files in os.walk('Content/vignettes'):
        for f in files:
            csv_reader = csv.reader(open(os.path.join(root, f), 'r', encoding='utf_8_sig'))
            for row in csv_reader:
                if len(row) > 1:
                    en = row[1]
                    if en not in original:
                        original.add(en)
                        if en in trans:
                            trans[en]["English"] = en
                            data.append(trans[en])
                        else:
                            data.append({'FileName': f, 'Role': row[0], 'English': en})

    df = pd.DataFrame(data, columns=('FileName', 'Role', 'English', 'French', 'Chinese', 'Japanese'), dtype=str)
    json_str = df.to_json(force_ascii=False, indent=4)
    open('EXAPUNKS_vignettes.json', 'w', encoding='utf-8').write(json_str)
    df.to_excel('EXAPUNKS_vignettes.xlsx', freeze_panes=(1, 0))


def export_descriptions():
    trans = get_trans('../import_txt/EXAPUNKS_descriptions.xlsx')
    original = set()
    data = []
    for root, dirs, files in os.walk('Content/descriptions'):
        for f in files:
            for line in open(os.path.join(root, f), 'r', encoding='utf_8_sig'):
                line = line.strip()
                if line not in original:
                    original.add(line)
                    if line in trans:
                        trans[line]["English"] = line
                        data.append(trans[line])
                    else:
                        data.append({'FileName': f, 'English': line})

    df = pd.DataFrame(data, columns=('FileName', 'English', 'German', 'French', 'Russian', 'Chinese', 'Japanese'), dtype=str)
    json_str = df.to_json(force_ascii=False, indent=4)
    open('EXAPUNKS_descriptions.json', 'w', encoding='utf-8').write(json_str)
    df.to_excel('EXAPUNKS_descriptions.xlsx')


if __name__ == '__main__':
    export_vignettes()
    export_descriptions()
