# -*- coding: utf-8 -*-

from argparse import Namespace
from unittest import TestCase, main

from generalize_config.namespace.join import left_join, right_join


class JoinTestCase(TestCase):
    def test_join_default(self):
        a = Namespace()
        b = Namespace(value=1)
        c = Namespace()
        d = Namespace(value=2)
        e = Namespace()
        nss = [a, b, c, d, e]

        left = left_join(*nss)
        self.assertEqual(1, left.value)

        right = right_join(*nss)
        self.assertEqual(2, right.value)

    def test_join_default_with_none(self):
        a = None
        b = Namespace(value=1)
        c = None
        d = Namespace(value=None)
        e = None
        nss = [a, b, c, d, e]

        left = left_join(*nss)
        self.assertEqual(1, left.value)

        right = right_join(*nss)
        self.assertEqual(1, right.value)


if __name__ == "__main__":
    main()
