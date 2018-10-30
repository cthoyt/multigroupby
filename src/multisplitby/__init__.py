# -*- coding: utf-8 -*-

"""Split an iterable into multiple using arbitrary predicates."""

from typing import Callable, Iterable, Tuple, TypeVar

__all__ = [
    'split_by',
    'multi_split_by',
]

F = TypeVar('F')

_LAST_OBJECT_SENTINEL = object()


def split_by(values: Iterable[F], predicate: Callable[[F], bool]) -> Tuple[Iterable[F], Iterable[F]]:
    """Split the iterator after the predicate becomes true."""
    last_value = _LAST_OBJECT_SENTINEL
    values = iter(values)

    def generator_first() -> Iterable[F]:
        """Yields values until the predicate is satisfied, and saves the final value."""
        nonlocal last_value

        for value in values:
            if predicate(value):
                last_value = value
                return
            yield value

    def generator_last() -> Iterable[F]:
        """Yield the final value from before and the remaining values."""
        if last_value is not _LAST_OBJECT_SENTINEL:
            yield last_value

        yield from values

    return generator_first(), generator_last()


def multi_split_by(values: Iterable[F], predicates: Iterable[Callable[[F], bool]]) -> Iterable[Iterable[F]]:
    """Split the iterator after the predicate becomes true, then repeat for every remaining iterable.

    If no values are given, will result in |predicates| + 1 generators, all yielding empty lists.

    If no predicates are given, will result in a single generator that yields the original list:

    >>> values = [1, 2, 3, 4]
    >>> [list(sub_values) for sub_values in multi_split_by(values, [])]
    >>> [[1, 2, 3, 4]]
    """
    last_value = _LAST_OBJECT_SENTINEL
    values = iter(values)

    def generator(p: Callable[[F], bool]) -> Iterable[F]:
        """Yield values until the given predicate is met, keeping the last value saved each time."""
        nonlocal last_value

        if last_value is not _LAST_OBJECT_SENTINEL:
            yield last_value

        for value in values:
            if p(value):
                last_value = value
                return

            yield value

    for predicate in predicates:
        yield generator(predicate)

    def generator_last() -> Iterable[F]:
        """Yield the remaining value on which the last predicate stopped, then the remainder of the iterable."""
        if last_value is not _LAST_OBJECT_SENTINEL:
            yield last_value

        yield from values

    yield generator_last()
