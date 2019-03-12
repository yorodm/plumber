# coding: utf-8

import abc
import typing
from types import TracebackType
from contextlib import contextmanager
from itertools import zip_longest
import copy

# Fix for Python lower than 3.6

if typing.TYPE_CHECKING:
    BaseExceptionType = typing.Type[BaseException]
else:
    BaseExceptionType = bool  # don't care, as long is it doesn't error


T = typing.TypeVar("T")
R = typing.TypeVar("R")


class Cleanable(abc.ABC):

    _exited = False

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


def transformer(fn: typing.Callable[[T], R]):
    class __FnTransformer(Transformer):
        def transform(self, data: T) -> R:
            return fn(data)

    return __FnTransformer()


@contextmanager
def _iterable_extractor(it: typing.Iterable[T]):
    def wrapper():
        for x in it:
            yield x
    try:
        yield wrapper()
    finally:
        pass


@contextmanager
def _fn_extractor(fn: typing.Callable[[T], R]) -> R:
    def wrapper():
        for x in fn():
            yield x
    try:
        yield wrapper()
    finally:
        pass


def extractor(data: typing.Union[typing.Callable[[], T], typing.Iterable[T]]):
    try:
        data = iter(data)
        return _iterable_extractor(data)
    except TypeError:
        return _fn_extractor(data)


class Extractor(Cleanable, typing.Generic[T]):
    @abc.abstractmethod
    def read(self) -> typing.Generator:
        yield None

    def __iter__(self) -> typing.Iterable[T]:
        for x in self.read():
            yield x

    def __add__(self, other: "Extractor[T]") -> "Extractor[T]":
        with self as left, other as right:
            data = zip_longest(iter(left), iter(right))
        return _iterable_extractor(data)


@contextmanager
def writer(fn: typing.Callable[[T], R]):
    def wrapper(trans: typing.Callable[[T], R]):
        for x in trans:
            fn(x)
    try:
        yield wrapper
    finally:
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
                for trans in self._transformations:
                    data = trans(data)
                yield data

    def __call__(self, ext: Extractor[T]) -> "Transformer[T,R]":
        self._extractor = ext
        return self

    def __add__(self, other: "Transformer[R]"):
        result = copy.deepcopy(self)
        result._transformations.extend(other._transformations)
        return result


class Pipe:
    def __init__(self, e: Extractor[T], t: Transformer[T, R], l: Writer[R]) -> None:
        self._extractor = e
        self._transformer = t
        self._writer = l

    def __or__(self, other: 'Pipe') -> 'Pipe':
        pass

    def __add__(self, other: 'Pipe') -> 'Pipe':
        pass

    def __mul__(self, other: 'Pipe') -> 'Pipe':
        pass

    def finished(self):
        return self._writer._exited

    def run(self) -> None:
        with self._writer as writer:
            writer(self._transformer(self._extractor))


class _SafetyPipe(Pipe):

    def __init__(left: Pipe, right: Pipe):
        pass


class _JointPipe(Pipe):

    def __init__(left: Pipe, right: Pipe) -> None:
        pass


class _MultiPipe(Pipe):

    def __init__(left: Pipe, right: Pipe) -> None:
        pass
