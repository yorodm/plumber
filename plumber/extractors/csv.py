# coding: utf-8
import csv
from plumber.pipe import Extractor


class CsvExtractor(Extractor):

    def __init__(self, filename: str, **kwargs):
        self._filename = filename
        self._csvargs = kwargs

    def read(self):
        with open(self._filename) as data:
            parser = csv.reader(data, **self._csvargs)
            for line in parser:
                yield line
