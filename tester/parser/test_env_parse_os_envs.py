# -*- coding: utf-8 -*-

import os
from os import environ
from tempfile import NamedTemporaryFile
from typing import Optional
from unittest import TestCase, main

from generalize_config.parser.env_parse import read_os_envs, read_os_envs_file

TEST_ENV_PREFIX = "TEST_"
TEST_ENV_FILE_SUFFIX = "_FILE"

TEST_CONFIG = "TEST_CONFIG"
TEST_HOST_FILE = "TEST_HOST_FILE"
TEST_BIND = "TEST_BIND"
TEST_PORT = "TEST_PORT"
TEST_VERBOSE = "TEST_VERBOSE"
TEST_DEVELOPER = "TEST_DEVELOPER"
TEST_PATH = "TEST_PATH"

TEST_CONFIG_VALUE = "env.conf"
TEST_HOST_VALUE = "unknown.host"
TEST_BIND_VALUE = "local"
TEST_PORT_VALUE = "8888"
TEST_VERBOSE_VALUE = "2"
TEST_DEVELOPER_VALUE = "true"
TEST_PATH_VALUE = "/package/dir/1:/package/dir/2"


def exchange_env(key: str, exchange: Optional[str]) -> Optional[str]:
    result = environ.get(key)
    if result is not None:
        environ.pop(key)
    if exchange is not None:
        environ[key] = exchange
    return result


def get_env(key: str) -> Optional[str]:
    return environ.get(key)


class EnvParseOsEnvsTestCase(TestCase):
    def setUp(self):
        with NamedTemporaryFile("wt", delete=False) as f:
            self.http_host_file = f.name
            f.write(TEST_HOST_VALUE)
        self.assertTrue(os.path.isfile(self.http_host_file))

        self.exchanges = {
            TEST_CONFIG: TEST_CONFIG_VALUE,
            TEST_HOST_FILE: self.http_host_file,
            TEST_BIND: TEST_BIND_VALUE,
            TEST_PORT: TEST_PORT_VALUE,
            TEST_VERBOSE: TEST_VERBOSE_VALUE,
            TEST_DEVELOPER: TEST_DEVELOPER_VALUE,
            TEST_PATH: TEST_PATH_VALUE,
        }
        self.originals = dict()
        self.updates = dict()

        for key, value in self.exchanges.items():
            self.originals[key] = exchange_env(key, value)
            self.updates[key] = get_env(key)

        self.assertEqual(TEST_CONFIG_VALUE, self.updates[TEST_CONFIG])
        self.assertEqual(self.http_host_file, self.updates[TEST_HOST_FILE])
        self.assertEqual(TEST_BIND_VALUE, self.updates[TEST_BIND])
        self.assertEqual(TEST_PORT_VALUE, self.updates[TEST_PORT])
        self.assertEqual(TEST_VERBOSE_VALUE, self.updates[TEST_VERBOSE])
        self.assertEqual(TEST_DEVELOPER_VALUE, self.updates[TEST_DEVELOPER])
        self.assertEqual(TEST_PATH_VALUE, self.updates[TEST_PATH])

    def tearDown(self):
        if os.path.isfile(self.http_host_file):
            os.remove(self.http_host_file)

        for key, value in self.originals.items():
            exchange_env(key, value)

        self.assertEqual(TEST_CONFIG_VALUE, self.exchanges[TEST_CONFIG])
        self.assertEqual(self.http_host_file, self.exchanges[TEST_HOST_FILE])
        self.assertEqual(TEST_BIND_VALUE, self.exchanges[TEST_BIND])
        self.assertEqual(TEST_PORT_VALUE, self.exchanges[TEST_PORT])
        self.assertEqual(TEST_VERBOSE_VALUE, self.exchanges[TEST_VERBOSE])
        self.assertEqual(TEST_DEVELOPER_VALUE, self.exchanges[TEST_DEVELOPER])
        self.assertEqual(TEST_PATH_VALUE, self.exchanges[TEST_PATH])

    def test_read_os_envs(self):
        config = read_os_envs(TEST_ENV_PREFIX)
        self.assertEqual(TEST_BIND_VALUE, config.bind)
        self.assertEqual(TEST_PORT_VALUE, config.port)
        self.assertEqual(TEST_VERBOSE_VALUE, config.verbose)
        self.assertEqual(TEST_DEVELOPER_VALUE, config.developer)
        self.assertEqual(TEST_PATH_VALUE, config.path)

    def test_read_os_envs_file(self):
        config = read_os_envs_file(TEST_ENV_PREFIX, TEST_ENV_FILE_SUFFIX)
        self.assertEqual(TEST_HOST_VALUE, config.host)


if __name__ == "__main__":
    main()
