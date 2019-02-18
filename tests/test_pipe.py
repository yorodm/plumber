# coding: utf-8
from plumber.classes import Pipe


def test_pipe(extractor, transformer, writer):
    print(extractor)
    print(transformer)
    print(writer)
    pipe = Pipe(extractor, transformer, writer)
    pipe.run()
    assert len(writer._data) > 9
