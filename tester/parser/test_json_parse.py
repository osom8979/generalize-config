# -*- coding: utf-8 -*-

import os
import tempfile
from unittest import TestCase, main

from generalize_config.parser.json_parse import read_json_file

TEST_BIND = "localhost"
TEST_PORT = 6666
TEST_VERBOSE = 7

JSON_SAMPLE = f"""{{
  "test": {{
    "bind": "{TEST_BIND}",
    "port": {TEST_PORT},
    "verbose": {TEST_VERBOSE},
    "path": [
      "/package/dir/1",
      "/package/dir/2"
    ]
  }}
}}"""


class JsonParseTestCase(TestCase):
    def setUp(self):
        fp = tempfile.NamedTemporaryFile(delete=False)
        fp.write(JSON_SAMPLE.encode("utf-8"))
        fp.close()
        self.test_json_path = fp.name

    def tearDown(self):
        os.unlink(self.test_json_path)
        self.assertFalse(os.path.exists(self.test_json_path))

    def test_read_json_file(self):
        config = read_json_file(self.test_json_path, "test")
        self.assertEqual(TEST_BIND, config.bind)
        self.assertEqual(TEST_PORT, config.port)
        self.assertEqual(TEST_VERBOSE, config.verbose)

        self.assertIsInstance(config.path, list)
        self.assertEqual(2, len(config.path))
        self.assertEqual("/package/dir/1", config.path[0])
        self.assertEqual("/package/dir/2", config.path[1])


if __name__ == "__main__":
    main()
