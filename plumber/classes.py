import abc
from typing import Optional, TracebackType, Generator, Iterable

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
        return self

    def __exit__(self, exc_type: Optional[BaseExceptionType],
                 exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> bool:
        self.cleanup()


class Reader(Cleanable):

    @abc.abstractmethod
    def read(self) -> Generator:
        yield None

    def __iter__(self):
        yield self.read()

    @classmethod
    def from_iterable(cls, it: Iterable) -> 'Reader':
        pass


class Writer(Cleanable):

    @abc.abstractmethod
    def write(self, data: dict) -> None:
        pass


class Transformer:

    def transform(self, data: dict) -> dict:
        pass


class Pipe:

    def __init__(e: Reader, t: Transformer, l: Writer):
        pass


class AsyncReader(abc.ABC):
    pass


class AsyncWriter(abc.ABC):
    pass
