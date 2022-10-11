# -*- coding: utf-8 -*-

from argparse import Namespace
from unittest import TestCase, main

from generalize_config.namespace.merge import merge_left_first, merge_right_first


class MergeTestCase(TestCase):
    def test_merge_default(self):
        a = Namespace()
        b = Namespace(value=1)
        c = Namespace()
        d = Namespace(value=2)
        e = None

        left = Namespace()
        self.assertEqual(left, merge_left_first(left, a, b, c, d, e))
        self.assertEqual(1, left.value)

        right = Namespace()
        self.assertEqual(right, merge_right_first(a, b, c, d, e, right))
        self.assertEqual(2, right.value)

    def test_merge_with_none_attr(self):
        a = Namespace(value=1)
        b = Namespace(value=None)

        left1 = Namespace()
        merge_left_first(left1, a, b)
        self.assertEqual(1, left1.value)

        left2 = Namespace()
        merge_left_first(left2, a, b, left_none_is_exist=True)
        self.assertEqual(1, left2.value)

        right1 = Namespace()
        merge_right_first(a, b, right1)
        self.assertEqual(1, right1.value)

        right2 = Namespace()
        merge_right_first(a, b, right2, right_none_is_exist=True)
        self.assertEqual(None, right2.value)


if __name__ == "__main__":
    main()
