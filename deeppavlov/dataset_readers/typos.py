"""
Copyright 2017 Neural Networks and Deep Learning lab, MIPT

Licensed inder the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import csv
from pathlib import Path
import sys

from deeppavlov.core.common.registry import register
from deeppavlov.core.data.utils import is_done, download, mark_done
from deeppavlov.core.data.dataset_reader import DatasetReader


@register('typos_custom_reader')
class TyposCustom(DatasetReader):
    @staticmethod
    def save_vocab(data, ser_dir):
        pass

    def __init__(self):
        pass

    @staticmethod
    def build(data_path: str):
        return Path(data_path)

    @classmethod
    def read(cls, data_path: str, *args, **kwargs):
        fname = cls.build(data_path)
        with fname.open(newline='') as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            next(reader)
            res = [(mistake, correct) for mistake, correct in reader]
        return {'train': res}


@register('typos_wikipedia_reader')
class TyposWikipedia(TyposCustom):
    @staticmethod
    def build(data_path: str):
        data_path = Path(data_path) / 'typos_wiki'

        fname = data_path / 'misspelings.tsv'

        if not is_done(data_path):
            url = 'https://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/For_machines'

            download(fname, url)

            with fname.open() as f:
                data = []
                for line in f:
                    if line.strip().endswith('<pre>'):
                        break
                for line in f:
                    if line.strip().startswith('</pre>'):
                        break
                    data.append(line.strip().split('-&gt;'))

            with fname.open('w', newline='') as tsvfile:
                writer = csv.writer(tsvfile, delimiter='\t')
                for line in data:
                    writer.writerow(line)

            mark_done(data_path)

            print('Built', file=sys.stderr)
        return fname


@register('typos_kartaslov_reader')
class TyposKartaslov(DatasetReader):
    def __init__(self):
        pass

    @staticmethod
    def build(data_path: str):
        data_path = Path(data_path) / 'kartaslov'

        fname = data_path / 'orfo_and_typos.L1_5.csv'

        if not is_done(data_path):
            url = 'https://raw.githubusercontent.com/dkulagin/kartaslov/master/dataset/orfo_and_typos/orfo_and_typos.L1_5.csv'

            download(fname, url)

            mark_done(data_path)

            print('Built', file=sys.stderr)
        return fname

    @staticmethod
    def read(data_path: str, *args, **kwargs):
        fname = TyposKartaslov.build(data_path)
        with open(str(fname), newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader)
            res = [(mistake, correct) for correct, mistake, weight in reader]
        return {'train': res}
