# coding: utf-8
import plumber


def test_pipe(extractor, transformer, writer):
    pipe = plumber.Pipe(extractor, transformer, writer)
    pipe.run()
    assert len(writer._data) == 10


def test_from_function(extractor, writer):
    def dupe(a):
        return (a, a)

    pipe = plumber.Pipe(
        extractor, plumber.Transformer.from_function(dupe), writer
    )
    pipe.run()
    assert writer._data[0] == ({"a": 0}, {"a": 0})


def test_chaining(extractor, transformer, writer):
    def dupe(a):
        return (a, a)
    dupe_transformer = plumber.Transformer.from_function(dupe)
    pipe = plumber.Pipe(
        extractor, transformer + dupe_transformer + transformer, writer
    )
    pipe.run()
    assert writer._data[0] == ({"a": 0}, {"a": 0})
