# -*- coding: utf-8 -*-

"""Split an iterable into multiple using arbitrary predicates."""

from typing import Callable, Iterable, Tuple, TypeVar

__all__ = [
    'split_by',
    'multi_split_by',
]

F = TypeVar('F')


def split_by(iterable: Iterable[F], predicate: Callable[[F], bool]) -> Tuple[Iterable[F], Iterable[F]]:
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


def multi_split_by(values: Iterable[F], predicates: Iterable[Callable[[F], bool]]) -> Iterable[Iterable[F]]:
    """Split the iterator after the predicate becomes true, then repeat for every remaining iterable."""
    predicates = iter(predicates)
    values = iter(values)
    last_value = None

    def generator_first(p):
        nonlocal last_value
        for value in values:
            if p(value):
                last_value = value
                return
            yield value

    predicate = next(predicates)
    yield generator_first(predicate)

    def generator_middle(p):
        nonlocal last_value
        yield last_value
        for value in values:
            if p(value):
                last_value = value
                return
            yield value

    for predicate in predicates:
        yield generator_middle(predicate)

    def generator_last():
        yield last_value
        yield from values

    yield generator_last()
