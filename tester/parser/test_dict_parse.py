# -*- coding: utf-8 -*-

from unittest import TestCase, main

from generalize_config.parser.dict_parse import parse_dict


class DictParseTestCase(TestCase):
    def test_parse_dict(self):
        data = {"aa": {"bb": {"cc": 100}}}
        config = parse_dict(data, "aa", "bb")
        self.assertEqual(100, config.cc)


if __name__ == "__main__":
    main()
