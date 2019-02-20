import abc
import functools
import typing
from types import TracebackType
from operator import or_
import copy

# Fix for Python lower than 3.6

if typing.TYPE_CHECKING:
    BaseExceptionType = typing.Type[BaseException]
else:
    BaseExceptionType = bool  # don't care, as long is it doesn't error


T = typing.TypeVar("T")
R = typing.TypeVar("R")


def transformify(*callables: typing.List["Transformer"]) -> "Transformer":
    return functools.reduce(or_, callables)


class Cleanable(abc.ABC):
    @abc.abstractmethod
    def setup(self) -> None:
        pass

    @abc.abstractmethod
    def cleanup(self) -> None:
        pass

    def __enter__(self) -> "Cleanable":
        self.setup()
        return self

    def __exit__(
        self,
        exc_type: typing.Optional[BaseExceptionType],
        exc_value: typing.Optional[BaseException],
        traceback: typing.Optional[TracebackType],
    ) -> bool:
        self.cleanup()


class Extractor(Cleanable, typing.Generic[T]):
    @abc.abstractmethod
    def read(self) -> typing.Generator:
        yield None

    def __iter__(self) -> typing.Iterable[T]:
        for x in self.read():
            yield x

    def __call__(self) -> "Extractor[T]":
        return self

    @classmethod
    def from_iterable(cls, it: typing.Iterable[T]) -> "Extractor[T]":
        pass


class Writer(Cleanable, typing.Generic[T]):
    @abc.abstractmethod
    def write(self, data: T) -> None:
        pass

    def __call__(self, tr: "Transformer") -> None:
        for x in tr:
            self.write(x)


class Transformer(abc.ABC, typing.Generic[T, R]):
    def __init__(self):
        self._transformations = [self.transform]

    @abc.abstractmethod
    def transform(self, data: T) -> R:
        pass

    def __iter__(self) -> typing.Iterable[R]:
        with self._extractor as ext:
            for data in ext:
                print(self._transformations)
                for trans in self._transformations:
                    data = trans(data)
                yield data

    def __call__(self, ext: Extractor[T]) -> "Transformer[T,R]":
        self._extractor = ext
        return self

    @classmethod
    def from_function(cls, func: typing.Callable[[T], R]) -> "Transformer":
        class __FnTransformer(cls):
            def __init__(self, func: typing.Callable[[T], R]) -> None:
                super().__init__()
                self._func = func

            def transform(self, data: T) -> R:
                print(data)
                return self._func(data)

        return __FnTransformer(func)

    def __add__(self, other: "Transformer[R]"):
        result = copy.deepcopy(self)
        result._transformations.extend(other._transformations)
        return result


class Pipe:

    def __init__(self, e: Extractor[T], t: Transformer[T, R], l: Writer[R]) -> None:
        self._extractor = e
        self._transformer = t
        self._writer = l

    def run(self) -> None:
        with self._writer as writer:
            writer(self._transformer(self._extractor()))
