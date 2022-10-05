# -*- coding: utf-8 -*-

import os
from argparse import Namespace
from tempfile import NamedTemporaryFile, TemporaryDirectory
from unittest import TestCase, main

from generalize_config.parser.cfg_parse import read_cfg_file, write_cfg_file

TEST_BIND = "localhost"
TEST_PORT = 6666
TEST_VERBOSE = 2

TEST_CFG_CONTENT = f"""
[test]
bind={TEST_BIND}
port={TEST_PORT}
verbose={TEST_VERBOSE}
"""


class CfgParseTestCase(TestCase):
    def setUp(self):
        fp = NamedTemporaryFile(delete=False)
        fp.write(TEST_CFG_CONTENT.encode("utf-8"))
        fp.close()
        self.test_cfg_path = fp.name

    def tearDown(self):
        os.unlink(self.test_cfg_path)
        self.assertFalse(os.path.exists(self.test_cfg_path))

    def test_read_cfg_file(self):
        config = read_cfg_file(self.test_cfg_path, "test")
        self.assertEqual(TEST_BIND, config.bind)
        self.assertEqual(str(TEST_PORT), config.port)
        self.assertEqual(str(TEST_VERBOSE), config.verbose)


class CfgFileTestCase(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.cfg_path = os.path.join(self.temp.name, "cfg.ini")
        self.assertFalse(os.path.exists(self.cfg_path))

    def tearDown(self):
        self.temp.cleanup()

    def test_write_cfg_file(self):
        section = "test"
        value = "value"

        ns1 = Namespace(value=value)
        write_cfg_file(ns1, self.cfg_path, section)
        self.assertTrue(os.path.isfile(self.cfg_path))

        ns2 = read_cfg_file(self.cfg_path, section)
        self.assertEqual(ns1.value, ns2.value)


if __name__ == "__main__":
    main()
