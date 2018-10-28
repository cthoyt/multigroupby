# -*- coding: utf-8 -*-

"""Tests for multigroupby."""

import unittest
from typing import Iterable

from multisplitby import multi_split_by, split_by


def _consume(iterable: Iterable):
    def yield_all():
        yield from iterable

    return list(yield_all())


def predicate_1(x: int) -> bool:
    """Return true if the integer is 3."""
    return x == 3


def predicate_2(x: int) -> bool:
    """Return true if the integer is 6."""
    return x == 6


def predicate_3(x: int) -> bool:
    """Return true if the integer is 8."""
    return x == 8


class TestIter(unittest.TestCase):
    """Test :mod:`multisplitby`."""

    def test_split_by(self):
        """Test the :func:`multisplitby.split_by` function."""
        my_iterable = [1, 2, 3, 4, 5, 6, 7]

        a, b = split_by(my_iterable, predicate_1)

        self.assertIsNotNone(a)
        self.assertIsNotNone(b)

        a = _consume(a)
        b = _consume(b)

        self.assertEqual([1, 2], a)
        self.assertEqual([3, 4, 5, 6, 7], b)

    def test_split_by_two(self):
        """Test the :func:`multisplitby.multi_split_by` function with two predicates."""
        integers = [1, 2, 3, 4, 5, 6, 7]

        # expected = [[1, 2], [3, 4, 5], [6, 7]]

        a, b, c = multi_split_by(integers, [predicate_1, predicate_2])

        self.assertIsNotNone(a)
        self.assertIsNotNone(b)
        self.assertIsNotNone(c)

        a = list(_consume(a))
        b = list(_consume(b))
        c = list(_consume(c))

        self.assertEqual([1, 2], a)
        self.assertEqual([3, 4, 5], b)
        self.assertEqual([6, 7], c)

    def test_split_by_three(self):
        """Test the :func:`multisplitby.multi_split_by` function with three predicates."""
        integers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # expected = [[1, 2], [3, 4, 5], [6, 7], [8, 9, 10]]

        a, b, c, d = multi_split_by(integers, [predicate_1, predicate_2, predicate_3])

        self.assertIsNotNone(a)
        self.assertIsNotNone(b)
        self.assertIsNotNone(c)
        self.assertIsNotNone(d)

        a = list(_consume(a))
        b = list(_consume(b))
        c = list(_consume(c))
        d = list(_consume(d))

        self.assertEqual([1, 2], a)
        self.assertEqual([3, 4, 5], b)
        self.assertEqual([6, 7], c)
        self.assertEqual([8, 9, 10], d)
