# coding: utf-8

from plumber.classes import Extractor, Writer, Transformer
from pytest import fixture


class FixedExtractor(Extractor):
    def setup(self):
        pass

    def cleanup(self):
        pass

    def read(self):
        for x in range(10):
            print("Generado %s" % x)
            yield {"a": x}


class FixedWriter(Writer):
    def setup(self):
        self._data = list()

    def cleanup(self):
        pass

    def write(self, data: list):
        self._data.append(data)


class FixedTransformer(Transformer):

    def transform(self, data):
        print("Procesando %s" % data)
        return data


@fixture
def extractor():
    return FixedExtractor()


@fixture
def writer():
    return FixedWriter()


@fixture
def transformer():
    return FixedTransformer()
