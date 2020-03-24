#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pydriller import GitRepository, RepositoryMining
import argparse
from translation import Translation
import os
import pandas as pd


if __name__ == '__main__':
    parser = argparse.ArgumentParser(epilog='for example: history.py some.json English Chinese')
    parser.add_argument('json_name', action='store', nargs=1, help='the json file name')
    parser.add_argument('original', action='store', nargs=1, help='the column name for original')
    parser.add_argument('translation', action='store', nargs=1, help='the column name for translation')
    parser.add_argument('repo', action='store', default='../', nargs='?', help='the path of repository')
    args = parser.parse_args()

    df = Translation(args.json_name[0]).get_dataframe()
    start_dropping = False
    for col in df.columns:
        if start_dropping:
            if col == args.translation[0]:
                old_translation = df[args.translation[0]]
            df.drop(columns=[col], inplace=True)
        elif col == args.original[0]:
            start_dropping = True

    gr = GitRepository('./')
    commits = gr.get_commits_modified_file(args.json_name[0])
    for commit in RepositoryMining('../', only_commits=commits).traverse_commits():
        for modification in commit.modifications:
            if (modification.filename == args.json_name[0]):
                date = commit.committer_date.strftime('%m-%d')
                author = commit.author.name
                print(date, author)

                source = modification.source_code
                try:
                    _df = pd.read_json(source)
                except BaseException:
                    print("WARNING: can't load")
                    continue

                new_translation = _df[args.translation[0]]
                for i, old in enumerate(old_translation):
                    if old == new_translation[i]:
                        new_translation[i] = ''
                    else:
                        old_translation[i] = new_translation[i]
                df[f'{date} {author}'] = new_translation
                break

    df[f'Current {args.translation[0]}'] = old_translation
    xlsx_name = os.path.splitext(args.json_name[0])[0] + '_history.xlsx'
    tr = Translation()
    tr.set_dataframe(df)
    tr.save(xlsx_name)
    print(f'{xlsx_name} saved')
