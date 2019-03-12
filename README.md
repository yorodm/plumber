# Plumber

[![Build Status](https://travis-ci.org/yorodm/plumber.svg?branch=develop)](https://travis-ci.org/yorodm/plumber)

Plumber is a simple Python ETL framework for Python3

**TL;DR:** Here's some code samples

```python
from plumber import pipe # API síncrona.

@pipe.extractor
def read_file():
    file_name = os.environ['FILENAME']
    with open(file_name) as f:
        for x in f.readlines():
            yield process_line(x)

@pipe.transformer
def csvfy(element):
    yield ','.join(map(str,element))


class SaveData(pipe.Writer):

    def __init__(self, filename):
        self.filename = filename

    def setup(self):
        self._file = open(f,'w')

    def cleanup(self):
        self._file.close()

    def write(x):
        self._file.write(x)

tuberia = pipe.Pipe(
    read_file,
    csvfy,
    SaveData("prueba.csv")
)
tuberia.run()
```
