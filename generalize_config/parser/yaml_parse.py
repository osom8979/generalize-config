# -*- coding: utf-8 -*-

from argparse import Namespace

from yaml import full_load as loads

from generalize_config.parser.dict_parse import parse_dict


def read_yaml_text(content: str, *subsection: str) -> Namespace:
    return parse_dict(loads(content), *subsection)


def read_yaml_file(path: str, *subsection: str, encoding="utf-8") -> Namespace:
    with open(path, encoding=encoding) as f:
        content = f.read()
    return read_yaml_text(content, *subsection)
