import abc
from typing import Optional, Generator, Iterable, Any
from types import TracebackType

# Fix for Python lower than 3.6
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    BaseExceptionType = Type[BaseException]
else:
    BaseExceptionType = bool  # don't care, as long is it doesn't error


class Cleanable(abc.ABC):

    @abc.abstractmethod
    def setup(self) -> None:
        pass

    @abc.abstractmethod
    def cleanup(self) -> None:
        pass

    def __enter__(self) -> 'Cleanable':
        self.setup()
        return self

    def __exit__(self, exc_type: Optional[BaseExceptionType],
                 exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> bool:
        self.cleanup()


class Extractor(Cleanable):

    @abc.abstractmethod
    def read(self) -> Generator:
        yield None

    def __iter__(self):
        for x in self.read():
            yield x

    def __call__(self):
        return self

    @classmethod
    def from_iterable(cls, it: Iterable) -> 'Extractor':
        pass


class Writer(Cleanable):

    @abc.abstractmethod
    def write(self, data: dict) -> None:
        pass

    def __call__(self, tr: 'Transformer') -> None:
        for x in tr:
            self.write(x)


class Transformer:

    @abc.abstractmethod
    def transform(self, data: dict) -> dict:
        pass

    def __iter__(self) -> Generator:
        with self._extractor as ext:
            for data in ext:
                yield self.transform(data)

    def __call__(self, ext: Extractor) -> Iterable:
        self._extractor = ext
        return self


class Pipe:

    def __init__(self, e: Extractor, t: Transformer, l: Writer):
        self._extractor = e
        self._transformer = t
        self._loader = l

    def run(self):
        with self._loader as loader:
            loader(self._transformer(self._extractor()))


class AsyncReader(abc.ABC):
    pass


class AsyncWriter(abc.ABC):
    pass
