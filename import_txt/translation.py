#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import os
import re
import openpyxl


class Translation:
    def __init__(self, name=None):
        if name is not None:
            self.load(name)

    def load(self, name):
        ext = os.path.splitext(name)[1].lower()
        if ext == '.xlsx':
            self._df = pd.read_excel(name)
        elif ext == '.json':
            self._df = pd.read_json(name)
        else:
            raise TypeError('not support type: "%s"' % ext)

        self.__process_dataframe()

    def save(self, name, index='English'):
        ext = os.path.splitext(name)[1].lower()
        if ext == '.xlsx':
            self.save_excel(name)
        elif ext == '.json':
            self.save_json(name)
        else:
            raise TypeError('not support type: "%s"' % ext)

    def save_excel(self, name, index='English'):
        frezze_index = self._df.columns.to_list().index(index) + 2
        self._df.to_excel(name, freeze_panes=(1, frezze_index))
        wb = openpyxl.load_workbook(name)
        for row in wb.active:
            for cell in row:
                if cell.value is None:
                    cell.value = ''
                elif not isinstance(cell.value, str):
                    cell.value = str(cell.value)
                cell.number_format = '@'
                cell.data_type = 's'
                cell.quotePrefix = True
        wb.save(name)

    def save_json(self, name):
        json_str = self._df.to_json(force_ascii=False, indent=4)
        open(name, 'w', encoding='utf-8').write(json_str)

    def __process_dataframe(self):
        self._df.replace(float('nan'), '', inplace=True)
        self._df.drop(columns=filter(lambda x: 'Unnamed' in x or re.search(r'_\d', x), self._df.columns), inplace=True)

    def get_translation(self, index='English'):
        start_index = self._df.columns.to_list().index(index) + 1
        rows = filter(lambda x: sum([len(y) for y in x[start_index:]]) > 0, self._df.itertuples(index=False))
        df = pd.DataFrame(rows)
        df.set_index(index, drop=False, inplace=True)
        return df.to_dict('index')

    def set_dataframe(self, df):
        self._df = df
        self.__process_dataframe()

    def set_data(self, data, columns):
        self.set_dataframe(pd.DataFrame(data, columns=columns, dtype=str))

    def get_percent(self, target_index):
        count = len(self._df[self._df[target_index] != ''])
        return count / len(self._df.index) * 100


def try_to_get_translation(name):
    if os.path.exists(name):
        return Translation(name).get_translation()
    else:
        return {}
