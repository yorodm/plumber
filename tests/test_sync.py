# coding: utf-8
import plumber


def test_pipe(extractor, transformer, writer):
    pipe = plumber.pipe.Pipe(extractor, transformer, writer)
    pipe.run()
    assert len(writer._data) == 10
    assert pipe.finished


def test_iterable_extractor(transformer, writer):
    data = plumber.pipe.extractor(range(2))
    pipe = plumber.pipe.Pipe(data, transformer, writer)
    pipe.run()
    assert writer._data == [0, 1]


def test_extractor_decorator(transformer, writer):
    @plumber.pipe.extractor
    def data():
        for x in range(10):
            yield {'a': x}
    pipe = plumber.pipe.Pipe(data, transformer, writer)
    pipe.run()
    assert writer._data[0] == {'a': 0}


def test_combine_extractors(extractor, transformer, writer):
    data = plumber.pipe.extractor(range(2))
    pipe = plumber.pipe.Pipe(extractor + data, transformer, writer)
    pipe.run()
    assert writer._data[0] == ({"a": 0}, 0)
    assert writer._data[3] == ({"a": 3}, None)


def test_transformer_decorator(extractor, writer):
    @plumber.pipe.transformer
    def dupe(a):
        return (a, a)

    pipe = plumber.pipe.Pipe(extractor, dupe, writer)
    pipe.run()
    assert writer._data[0] == ({"a": 0}, {"a": 0})


def test_chaining(extractor, transformer, writer):
    @plumber.pipe.transformer
    def dupe(a):
        return (a, a)

    pipe = plumber.pipe.Pipe(extractor, transformer + dupe + transformer, writer)
    pipe.run()
    assert writer._data[0] == ({"a": 0}, {"a": 0})
