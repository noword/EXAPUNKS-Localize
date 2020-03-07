#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from io import StringIO
import csv
import re
from translation import Translation


def import_strings():
    print('EXAPUNKS_exe.json\t\t%.2f%%' % Translation('EXAPUNKS_exe.json').get_percent('Chinese'))
    trans = Translation('EXAPUNKS_exe.json').get_translation()
    csv_writer = csv.writer(open('strings.csv', 'w', encoding='utf-8'), lineterminator='\n', escapechar='\\')
    for key, value in trans.items():
        row = [key, '']
        row.extend([value[lang] for lang in ('German', 'French', 'Russian', 'Chinese', 'Japanese')])
        csv_writer.writerow(row)


def import_vignettes():
    print('EXAPUNKS_vignettes.json\t\t%.2f%%' % Translation('EXAPUNKS_vignettes.json').get_percent('Chinese'))
    trans = Translation('EXAPUNKS_vignettes.json').get_translation()
    for root, dirs, files in os.walk('../export_txt/Content/vignettes'):
        for f in files:
            name = os.path.join(root, f)
            out = StringIO()
            csv_reader = csv.reader(open(name, 'r', encoding='utf_8_sig'))
            csv_writer = csv.writer(out, lineterminator='\n', escapechar='\\')
            need_save = False
            for row in csv_reader:
                if len(row) > 1:
                    en = row[1]
                    if en in trans and len(trans[en]) > 0:
                        need_save = True
                        row.extend([trans[en][lang] for lang in ('French', 'Chinese', 'Japanese')])
                csv_writer.writerow(row)
            if need_save:
                name = name.replace('../export_txt', '../patch')
                try:
                    os.makedirs(os.path.split(name)[0])
                except BaseException:
                    pass
                open(name, 'w', encoding='utf_8_sig').write(out.getvalue())


def import_descriptions():
    LANGS = {'German': 'de',
             'French': 'fr',
             'Russian': 'ru',
             'Chinese': 'zh',
             'Japanese': 'ja'
             }

    print('EXAPUNKS_descriptions.json\t%.2f%%' % Translation('EXAPUNKS_descriptions.json').get_percent('Chinese'))
    trans = Translation('EXAPUNKS_descriptions.json').get_translation()
    for root, dirs, files in os.walk('../export_txt/Content/descriptions/en'):
        for f in files:
            name = os.path.join(root, f)
            lines = open(name, 'r', encoding='utf_8_sig').readlines()
            for country, abbr in LANGS.items():
                out = StringIO()
                need_save = True
                for line in lines:
                    line = line.strip()
                    if len(line) > 0 \
                            and line in trans \
                            and len(trans[line][country]) > 0:
                        line = trans[line][country]
                        # need_save = True
                    out.write(line + '\n')
                if need_save:
                    new_name = name.replace('../export_txt', '../patch').replace('/en', '/' + abbr, 1)
                    try:
                        os.makedirs(os.path.split(new_name)[0])
                    except BaseException:
                        pass
                    open(new_name, 'w', encoding='utf').write(out.getvalue())


if __name__ == '__main__':
    import_strings()
    import_vignettes()
    import_descriptions()
