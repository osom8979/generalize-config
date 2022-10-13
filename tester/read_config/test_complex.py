# -*- coding: utf-8 -*-

import os
from argparse import ArgumentParser, Namespace
from tempfile import NamedTemporaryFile
from unittest import TestCase, main

from generalize_config.namespace.merge import merge_left_first
from generalize_config.parser.env_parse import read_os_envs, read_os_envs_file
from generalize_config.read_config import read_config_file
from tester.utils.environment_context import EnvironmentContext

YAML_SAMPLE = """
test:
  verbose: 2
  developer: true
  port: 80
"""

CFG_SAMPLE = """
[test]
host=localhost
counter=100
"""

VALUE_SAMPLE = "1234"


def test_argument_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("--config")
    parser.add_argument("--verbose", action="count")
    parser.add_argument("--level", choices=["a", "b", "c"])
    parser.add_argument("--timeout", type=float)
    parser.add_argument("--allows", action="append")
    parser.add_argument("--host")
    parser.add_argument("--port", type=int)
    return parser


def write_temporary_file(content: str, suffix: str) -> str:
    fp = NamedTemporaryFile(suffix=suffix, delete=False)
    fp.write(content.encode("utf-8"))
    fp.close()
    return fp.name


class ComplexTestCase(TestCase):
    def setUp(self):
        self.yaml_file = write_temporary_file(YAML_SAMPLE, ".yaml")
        self.value_file = write_temporary_file(VALUE_SAMPLE, ".txt")
        self.cfg_file = write_temporary_file(CFG_SAMPLE, ".cfg")

        self.assertTrue(os.path.exists(self.yaml_file))
        self.assertTrue(os.path.exists(self.value_file))
        self.assertTrue(os.path.exists(self.cfg_file))

        self.prefix = "TEST_"
        self.suffix = "_FILE"
        self.context = EnvironmentContext(
            TEST_VALUE1="aaa",
            TEST_VALUE2="bbb",
            TEST_VALUE3="ccc",
            TEST_VALUE4_FILE=self.value_file,
            TEST_CONFIG=self.cfg_file,
        )
        self.context.open()

    def tearDown(self):
        self.context.close()

        os.unlink(self.yaml_file)
        os.unlink(self.value_file)
        os.unlink(self.cfg_file)

        self.assertFalse(os.path.exists(self.yaml_file))
        self.assertFalse(os.path.exists(self.value_file))
        self.assertFalse(os.path.exists(self.cfg_file))

    def test_empty_args_is_none(self):
        parser = test_argument_parser()
        empty_args = parser.parse_known_args([])[0]
        self.assertIsNone(empty_args.config)
        self.assertIsNone(empty_args.verbose)
        self.assertIsNone(empty_args.level)
        self.assertIsNone(empty_args.timeout)
        self.assertIsNone(empty_args.allows)
        self.assertIsNone(empty_args.host)
        self.assertIsNone(empty_args.port)

    def test_complex(self):
        parser = test_argument_parser()
        args = ["--config", self.yaml_file]
        cmds = parser.parse_known_args(args)[0]
        self.assertEqual(self.yaml_file, cmds.config)
        self.assertIsNone(cmds.verbose)
        self.assertIsNone(cmds.level)
        self.assertIsNone(cmds.timeout)
        self.assertIsNone(cmds.allows)
        self.assertIsNone(cmds.host)
        self.assertIsNone(cmds.port)

        cmd_config = read_config_file(cmds.config, "test")
        self.assertEqual(3, len(vars(cmd_config)))
        self.assertEqual(2, cmd_config.verbose)
        self.assertIsInstance(cmd_config.developer, bool)
        self.assertTrue(cmd_config.developer)
        self.assertEqual(80, cmd_config.port)

        envs = read_os_envs(prefix=self.prefix)
        self.assertEqual(5, len(vars(envs)))
        self.assertEqual("aaa", envs.value1)
        self.assertEqual("bbb", envs.value2)
        self.assertEqual("ccc", envs.value3)
        self.assertEqual(self.value_file, envs.value4_file)
        self.assertEqual(self.cfg_file, envs.config)

        envs_config = read_config_file(envs.config, "test")
        self.assertEqual(2, len(vars(envs_config)))
        self.assertEqual("localhost", envs_config.host)
        self.assertEqual("100", envs_config.counter)  # Warning, Not integer type.

        env_files_args = read_os_envs_file(prefix=self.prefix, suffix=self.suffix)
        self.assertEqual(1, len(vars(env_files_args)))
        self.assertEqual(VALUE_SAMPLE, env_files_args.value4)

        default_args = Namespace(port=9999, timeout=1.1)

        nss = (cmds, cmd_config, envs, envs_config, env_files_args, default_args)
        result_args = merge_left_first(Namespace(), *nss)

        self.assertEqual(14, len(vars(result_args)))
        self.assertEqual(self.yaml_file, result_args.config)
        self.assertEqual(2, cmd_config.verbose)
        self.assertIsNone(result_args.level)
        self.assertEqual(1.1, result_args.timeout)
        self.assertIsNone(result_args.allows)
        self.assertEqual(80, result_args.port)
        self.assertIsInstance(result_args.developer, bool)
        self.assertTrue(result_args.developer)
        self.assertEqual("aaa", result_args.value1)
        self.assertEqual("bbb", result_args.value2)
        self.assertEqual("ccc", result_args.value3)
        self.assertEqual(self.value_file, result_args.value4_file)
        self.assertEqual("localhost", result_args.host)
        self.assertEqual("100", result_args.counter)  # Warning, Not integer type.
        self.assertEqual(VALUE_SAMPLE, result_args.value4)


if __name__ == "__main__":
    main()
