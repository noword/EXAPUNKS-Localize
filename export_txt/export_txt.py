#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../import_txt')
from translation import Translation, try_to_get_translation
import csv
import os


def export_vignettes():
    trans = try_to_get_translation('../import_txt/EXAPUNKS_vignettes.json')
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
                            data.append(trans[en])
                        else:
                            data.append({'FileName': f, 'Role': row[0], 'English': en})

    translation = Translation()
    translation.set_data(data, ('FileName', 'Role', 'English', 'French', 'Chinese', 'Japanese'))
    translation.save('EXAPUNKS_vignettes.json')


def export_descriptions():
    trans = try_to_get_translation('../import_txt/EXAPUNKS_descriptions.json')
    original = set()
    data = []
    for root, dirs, files in os.walk('Content/descriptions'):
        for f in files:
            for line in open(os.path.join(root, f), 'r', encoding='utf_8_sig'):
                line = line.strip()
                if line not in original:
                    original.add(line)
                    if line in trans:
                        data.append(trans[line])
                    else:
                        data.append({'FileName': f, 'English': line})

    translation = Translation()
    translation.set_data(data, ('FileName', 'English', 'German', 'French', 'Russian', 'Chinese', 'Japanese'))
    translation.save('EXAPUNKS_descriptions.json')


if __name__ == '__main__':
    export_vignettes()
    export_descriptions()
