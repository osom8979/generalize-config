# -*- coding: utf-8 -*-

import os
import tempfile
from unittest import TestCase, main

from generalize_config.config_file import read_config_file

YAML_SAMPLE = """
test:
  verbose: 2
  developer: true
  port: 80
"""


class ConfigFileYamlTestCase(TestCase):
    def setUp(self):
        fp = tempfile.NamedTemporaryFile(suffix=".yaml", delete=False)
        fp.write(YAML_SAMPLE.encode("utf-8"))
        fp.close()
        self.test_file_path = fp.name

    def tearDown(self):
        os.unlink(self.test_file_path)
        self.assertFalse(os.path.exists(self.test_file_path))

    def test_read_config_file(self):
        config = read_config_file(self.test_file_path, "test")
        self.assertEqual(2, config.verbose)
        self.assertIsInstance(config.developer, bool)
        self.assertTrue(config.developer)
        self.assertEqual(80, config.port)

    def test_subsection_error(self):
        with self.assertRaises(KeyError):
            read_config_file(self.test_file_path, "test", "kk")


if __name__ == "__main__":
    main()
