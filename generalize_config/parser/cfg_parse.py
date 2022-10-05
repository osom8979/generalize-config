# -*- coding: utf-8 -*-

from argparse import Namespace
from configparser import ConfigParser
from typing import Any, Dict, Optional

from generalize_config.parser.dict_parse import parse_dict


def read_cfg_parser_as_dict(parser: ConfigParser) -> Dict[str, Dict[str, Any]]:
    result = dict()
    for section in parser.sections():
        section_result = dict()
        for option in parser.options(section):
            value = parser.get(section, option)
            section_result[option] = value
        result[section] = section_result
    return result


def read_cfg_parser(parser: ConfigParser, section: Optional[str] = None) -> Namespace:
    return parse_dict(read_cfg_parser_as_dict(parser), section)


def read_cfg_text(content: str, section: Optional[str] = None) -> Namespace:
    parser = ConfigParser()
    parser.read_string(content)
    return read_cfg_parser(parser, section)


def read_cfg_file(
    path: str,
    section: Optional[str] = None,
    encoding="utf-8",
) -> Namespace:
    parser = ConfigParser()
    parser.read(path, encoding=encoding)
    return read_cfg_parser(parser, section)


def write_cfg_file(
    namespace: Namespace,
    path: str,
    section: str,
    encoding="utf-8",
) -> None:
    parser = ConfigParser()
    parser[section] = dict()
    for key, value in vars(namespace).items():
        if value is None:
            continue
        parser.set(section, key, str(value))
    with open(path, mode="w", encoding=encoding) as f:
        parser.write(f)
