# -*- coding: utf-8 -*-

from argparse import Namespace
from unittest import TestCase, main

from generalize_config.namespace.strip import strip_none_attributes


class StripTestCase(TestCase):
    def test_strip_none_attributes(self):
        a = Namespace(value1=1, value2=None)
        self.assertEqual(1, getattr(a, "value1"))
        self.assertTrue(hasattr(a, "value2"))

        strip_none_attributes(a)
        self.assertEqual(1, getattr(a, "value1"))
        self.assertFalse(hasattr(a, "value2"))


if __name__ == "__main__":
    main()
