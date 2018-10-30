# -*- coding: utf-8 -*-

"""Split an iterable into multiple using arbitrary predicates."""

from typing import Callable, Iterable, Tuple, TypeVar

__all__ = [
    'split_by',
    'multi_split_by',
]

F = TypeVar('F')
F_predicate = Callable[[F], bool]


def split_by(iterable: Iterable[F], predicate: F_predicate) -> Tuple[Iterable[F], Iterable[F]]:
    """Split the iterator after the predicate becomes true."""
    iterable = iter(iterable)

    last_value = None

    def generator_1():
        nonlocal last_value

        for x in iterable:
            if predicate(x):
                last_value = x
                return
            yield x

    def generator_2():
        yield last_value
        yield from iterable

    return generator_1(), generator_2()


def multi_split_by(iterable: Iterable[F], predicates: Iterable[F_predicate]) -> Iterable[Iterable[F]]:
    """Split the iterator after the predicate becomes true, then repeat for every remaining iterable."""
    predicates = iter(predicates)
    iterable = iter(iterable)
    last_value = None

    def generator_first(p):
        nonlocal last_value
        for x in iterable:
            if p(x):
                last_value = x
                return
            yield x

    predicate = next(predicates)
    yield generator_first(predicate)

    def generator(p):
        nonlocal last_value
        yield last_value
        for x in iterable:
            if p(x):
                last_value = x
                return
            yield x

    for predicate in predicates:
        yield generator(predicate)

    def generator_last():
        yield last_value
        yield from iterable

    yield generator_last()
