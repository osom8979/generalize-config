# -*- coding: utf-8 -*-

from unittest import TestCase, main

from generalize_config.parser.env_parse import normalize_config_key, read_dict


class EnvParseApiTestCase(TestCase):
    def test_normalize_config_key(self):
        sample = "TEST_TEMP_FILE"

        self.assertEqual("temp_file", normalize_config_key(sample, prefix="TEST_"))
        self.assertEqual("test_temp", normalize_config_key(sample, suffix="_FILE"))
        self.assertEqual("temp", normalize_config_key(sample, "TEST_", "_FILE"))

        with self.assertRaises(KeyError):
            normalize_config_key(sample, "ECC_")
        with self.assertRaises(KeyError):
            normalize_config_key(sample, "_FIL")

        with self.assertRaises(KeyError):
            normalize_config_key("", prefix="A")
        with self.assertRaises(KeyError):
            normalize_config_key("", suffix="B")

        with self.assertRaises(KeyError):
            normalize_config_key(sample, prefix=sample)
        with self.assertRaises(KeyError):
            normalize_config_key(sample, suffix=sample)
        with self.assertRaises(KeyError):
            normalize_config_key(sample, sample, sample)

    def test_read_dict(self):
        sample = {
            "TEST_CONFIG": "test.conf",
            "TEST_BIND": "localhost",
            "TEST_PORT": 7777,
            "TEST_VERBOSE": 3,
            "TEST_DEVELOPER": True,
            "CONFIG": "unknown",
        }

        ns1 = read_dict(sample)
        self.assertEqual(6, len(vars(ns1)))
        self.assertEqual(sample["TEST_CONFIG"], ns1.test_config)
        self.assertEqual(sample["TEST_BIND"], ns1.test_bind)
        self.assertEqual(sample["TEST_PORT"], ns1.test_port)
        self.assertEqual(sample["TEST_VERBOSE"], ns1.test_verbose)
        self.assertEqual(sample["TEST_DEVELOPER"], ns1.test_developer)
        self.assertEqual(sample["CONFIG"], ns1.config)

        ns2 = read_dict(sample, prefix="TEST_")
        self.assertEqual(5, len(vars(ns2)))
        self.assertEqual(sample["TEST_CONFIG"], ns2.config)
        self.assertEqual(sample["TEST_BIND"], ns2.bind)
        self.assertEqual(sample["TEST_PORT"], ns2.port)
        self.assertEqual(sample["TEST_VERBOSE"], ns2.verbose)
        self.assertEqual(sample["TEST_DEVELOPER"], ns2.developer)

        ns3 = read_dict(sample, suffix="BOSE")
        self.assertEqual(1, len(vars(ns3)))
        self.assertEqual(sample["TEST_VERBOSE"], ns3.test_ver)

        ns4 = read_dict(sample, prefix="TEST_", suffix="BOSE")
        self.assertEqual(1, len(vars(ns4)))
        self.assertEqual(sample["TEST_VERBOSE"], ns4.ver)


if __name__ == "__main__":
    main()
