# -*- coding: utf-8 -*-

from argparse import Namespace
from os import environ
from re import Pattern
from re import compile as re_compile
from typing import Dict, Final, Optional

ILLEGAL_KEY_PATTERN: Final[Pattern] = re_compile(r"[^a-zA-Z0-9_]")
NORMALIZE_ILLEGAL_CHAR: Final[str] = "_"


def _normalize_illegal_key(text: str) -> str:
    return ILLEGAL_KEY_PATTERN.sub(NORMALIZE_ILLEGAL_CHAR, text)


def normalize_config_key(
    key: str,
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
) -> str:
    if prefix:
        if not key.startswith(prefix):
            raise KeyError(f"The prefix '{prefix}' does not match")
        begin = len(prefix)
    else:
        begin = None

    if suffix:
        if not key.endswith(suffix):
            raise KeyError(f"The suffix '{suffix}' does not match")
        end = -len(suffix)
    else:
        end = None

    middle = key[begin:end]
    if not middle:
        raise KeyError("The key is empty")

    return _normalize_illegal_key(middle).lower()


def filter_dict(
    data: Dict[str, str],
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
) -> Dict[str, str]:
    if not prefix and not suffix:
        return data

    result = dict()
    for k, v in data.items():
        if prefix and not k.startswith(prefix):
            continue
        if suffix and not k.endswith(suffix):
            continue
        result[k] = v
    return result


def normalize_filter_dict(
    data: Dict[str, str],
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
) -> Dict[str, str]:
    result = dict()
    for k, v in filter_dict(data, prefix, suffix).items():
        result[normalize_config_key(k, prefix, suffix)] = v
    return result


def read_dict(
    data: Dict[str, str],
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
) -> Namespace:
    return Namespace(**normalize_filter_dict(data, prefix, suffix))


def os_envs() -> Dict[str, str]:
    return {k: str(environ.get(k)) for k in environ if environ}


def read_os_envs(
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
) -> Namespace:
    return read_dict(os_envs(), prefix, suffix)


def read_os_envs_file(
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
    encoding: Optional[str] = None,
) -> Namespace:
    result = Namespace()
    envs = normalize_filter_dict(os_envs(), prefix, suffix)
    for key, value in envs.items():
        with open(value, "r", encoding=encoding) as f:
            setattr(result, key, f.read())
    return result
