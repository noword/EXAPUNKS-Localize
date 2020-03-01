#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import os


def get_trans(name):
    if not os.path.exists(name):
        return {}

    ext = os.path.splitext(name)[1].lower()
    if ext in ('.xls', '.xlsx'):
        df = pd.read_excel(name)
    elif ext in ('.json'):
        df = pd.read_json(name)
    else:
        raise TypeError('not support type: "%s"' % ext)

    trans_start_index = df.columns.to_list().index('English') + 1
    df.replace(float('nan'), '', inplace=True)
    rows = filter(lambda x: sum([len(y) for y in x[trans_start_index:]]) > 0, df.itertuples(index=False))
    df = pd.DataFrame(rows)
    df = df.set_index('English')
    if '_0' in df:
        df = df.drop(columns=['_0', ])
    trans = df.to_dict('index')
    return trans
