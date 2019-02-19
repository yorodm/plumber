import abc
import functools
import contextlib
from typing import Optional, Generator, Iterable, Any, List, Callable
from types import TracebackType

# Fix for Python lower than 3.6
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    BaseExceptionType = Type[BaseException]
else:
    BaseExceptionType = bool  # don't care, as long is it doesn't error


def compose(*callables: List[Callable[[Any], Any]]) -> Callable:
    return functools.reduce(
        lambda f, g: lambda x: f(g(x)), callables
    )


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
        exc_type: Optional[BaseExceptionType],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
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
    def from_iterable(cls, it: Iterable) -> "Extractor":
        pass


class Writer(Cleanable):
    @abc.abstractmethod
    def write(self, data: Any) -> None:
        pass

    def __call__(self, tr: "Transformer") -> None:
        for x in tr:
            self.write(x)


class Transformer(Cleanable):

    @abc.abstractmethod
    def transform(self, data: Any) -> Any:
        pass

    def __iter__(self) -> Iterable[Any]:
        with self._extractor as ext:
            for data in ext:
                yield self.transform(data)

    def __call__(self, ext: Extractor) -> Iterable:
        self._extractor = ext
        return self

    @classmethod
    def from_function(cls, func: Callable[[Any], Any]) -> 'Transformer':
        class __FnTransformer(cls):
            def __init__(self, func: Callable[[Any], Any]) -> None:
                self._func = func

            def transform(self, data: Any) -> Any:
                return self._func(data)
        return __FnTransformer(func)


class Pipe:

    def __init__(self, e: Extractor, t: List[Transformer], l: Writer):
        self._extractor = e
        self._transformers = compose(*t)
        print(self._transformers)
        self._writer = l

    def run(self):
        with self._writer as writer:
            writer(self._transformers(self._extractor()))


class AsyncReader(abc.ABC):
    pass


class AsyncWriter(abc.ABC):
    pass
