# -*- coding: utf-8 -*-

import os
from tempfile import NamedTemporaryFile
from unittest import TestCase, main

from generalize_config.parser.env_parse import read_os_envs, read_os_envs_file
from tester.utils.environment_context import EnvironmentContext

TEST_CONFIG_VALUE = "env.conf"
TEST_HOST_VALUE = "unknown.host"
TEST_BIND_VALUE = "local"
TEST_PORT_VALUE = "8888"
TEST_VERBOSE_VALUE = "2"
TEST_DEVELOPER_VALUE = "true"
TEST_PATH_VALUE = "/package/dir/1:/package/dir/2"


class EnvParseOsEnvsTestCase(TestCase):
    def setUp(self):
        with NamedTemporaryFile("wt", delete=False) as f:
            self.http_host_file = f.name
            f.write(TEST_HOST_VALUE)
        self.assertTrue(os.path.isfile(self.http_host_file))

        self.context = EnvironmentContext(
            TEST_CONFIG=TEST_CONFIG_VALUE,
            TEST_HOST_FILE=self.http_host_file,
            TEST_BIND=TEST_BIND_VALUE,
            TEST_PORT=TEST_PORT_VALUE,
            TEST_VERBOSE=TEST_VERBOSE_VALUE,
            TEST_DEVELOPER=TEST_DEVELOPER_VALUE,
            TEST_PATH=TEST_PATH_VALUE,
        )
        self.context.open()

    def tearDown(self):
        if os.path.isfile(self.http_host_file):
            os.remove(self.http_host_file)
        self.context.close()

    def test_read_os_envs(self):
        config = read_os_envs("TEST_")
        self.assertEqual(TEST_BIND_VALUE, config.bind)
        self.assertEqual(TEST_PORT_VALUE, config.port)
        self.assertEqual(TEST_VERBOSE_VALUE, config.verbose)
        self.assertEqual(TEST_DEVELOPER_VALUE, config.developer)
        self.assertEqual(TEST_PATH_VALUE, config.path)

    def test_read_os_envs_file(self):
        config = read_os_envs_file("TEST_", "_FILE")
        self.assertEqual(TEST_HOST_VALUE, config.host)


if __name__ == "__main__":
    main()
