# -*- coding: utf-8 -*-

import os
import tempfile
from unittest import TestCase, main

from generalize_config.config_file import read_config_file

INI_SAMPLE = """
[test]
flag=Hello
"""


class ConfigFileIniTestCase(TestCase):
    def setUp(self):
        fp = tempfile.NamedTemporaryFile(suffix=".ini", delete=False)
        fp.write(INI_SAMPLE.encode("utf-8"))
        fp.close()
        self.test_file_path = fp.name

    def tearDown(self):
        os.unlink(self.test_file_path)
        self.assertFalse(os.path.exists(self.test_file_path))

    def test_read_config_file(self):
        config = read_config_file(self.test_file_path, "test")
        self.assertEqual("Hello", config.flag)

    def test_subsection_error(self):
        with self.assertRaises(IndexError):
            read_config_file(self.test_file_path, "test", "kk")


if __name__ == "__main__":
    main()
