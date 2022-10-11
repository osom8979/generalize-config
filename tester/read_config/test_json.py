# -*- coding: utf-8 -*-

import os
import tempfile
from unittest import TestCase, main

from generalize_config.read_config import read_config_file

JSON_SAMPLE = """
{
  "test": {
    "main": "target"
  }
}
"""


class JsonTestCase(TestCase):
    def setUp(self):
        fp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        fp.write(JSON_SAMPLE.encode("utf-8"))
        fp.close()
        self.test_file_path = fp.name

    def tearDown(self):
        os.unlink(self.test_file_path)
        self.assertFalse(os.path.exists(self.test_file_path))

    def test_read_config_file(self):
        config = read_config_file(self.test_file_path, "test")
        self.assertEqual("target", config.main)

    def test_subsection_error(self):
        with self.assertRaises(KeyError):
            read_config_file(self.test_file_path, "test", "kk")


if __name__ == "__main__":
    main()
