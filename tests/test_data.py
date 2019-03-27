# coding: utf-8
import plumber.extractors
from pathlib import Path


def test_csv(writer, transformer):
    current_dir = Path(__file__).resolve().parent
    filename = current_dir.joinpath('test_data.csv')
    extractor = plumber.extractors.CsvExtractor(filename)
    pipe = plumber.pipe.Pipe(extractor, transformer, writer)
    pipe.run()
    print(type(writer._data[0]))
    assert writer._data[0] == ['Github', 'Super git repos', '1']
