# coding: utf-8
import plumber


def test_pipe(extractor, transformer, writer):
    pipe = plumber.Pipe(extractor, transformer, writer)
    pipe.run()
    assert len(writer._data) == 10


def test_iterable_extractor(transformer, writer):
    data = plumber.extractor(range(2))
    pipe = plumber.Pipe(data, transformer, writer)
    pipe.run()
    assert writer._data == [0, 1, 3]


def test_extractor_decorator(transformer, writer):
    @plumber.extractor
    def data():
        for x in range(10):
            yield {'a':x}
    pipe = plumber.Pipe(data, transformer, writer)
    pipe.run()
    assert writer._data[0] == {'a': 0}

def test_combine_extractors(extractor, transformer, writer):
    data = extractor(range(2))
    pipe = plumber.Pipe(extractor + data, transformer, writer)
    pipe.run()
    assert writer._data[0] == ({"a": 0}, 0)
    assert writer._data[3] == ({"a": 3}, None)


def test_transformer_decorator(extractor, writer):
    @plumber.transformer
    def dupe(a):
        return (a, a)

    pipe = plumber.Pipe(extractor, dupe, writer)
    pipe.run()
    assert writer._data[0] == ({"a": 0}, {"a": 0})


def test_chaining(extractor, transformer, writer):
    @plumber.transformer
    def dupe(a):
        return (a, a)

    pipe = plumber.Pipe(extractor, transformer + dupe + transformer, writer)
    pipe.run()
    assert writer._data[0] == ({"a": 0}, {"a": 0})
