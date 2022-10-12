# -*- coding: utf-8 -*-

import os
from argparse import Namespace
from pathlib import Path
from typing import Optional, Union

from generalize_config.parser.cfg_parse import read_cfg_file
from generalize_config.parser.json_parse import read_json_file
from generalize_config.parser.yaml_parse import read_yaml_file

CFG_EXTENSIONS = ("cfg", "ini")
JSON_EXTENSIONS = ("json",)
YAML_EXTENSIONS = ("yaml", "yml")


def normalize_extension(extension: str) -> str:
    stripped_ext = extension.strip()
    if stripped_ext[0] == ".":
        return stripped_ext[1:].lower()  # Remove Dot('.').
    else:
        return stripped_ext.lower()


def read_config_file_by_extension(
    path: str,
    extension: str,
    *subsection: str,
    encoding="utf-8",
) -> Namespace:
    if not path:
        raise ValueError("Emtpy `path` argument.")

    if not extension:
        raise ValueError("Emtpy `extension` argument.")

    if not os.path.isfile(path):
        raise FileNotFoundError(f"Not found config file: {path}")

    if not os.access(path, os.R_OK):
        raise PermissionError(f"The file cannot be accessed: {path}")

    e = normalize_extension(extension)

    if e in CFG_EXTENSIONS:
        if not subsection:
            raise ValueError(
                "When reading a `cfg` or `ini` file, there must be 1 section"
            )
        if len(subsection) >= 2:
            raise IndexError(f"{e} files do not allow subsections greater than 2-depth")
        assert len(subsection) == 1
        return read_cfg_file(path, subsection[0], encoding=encoding)
    elif e in JSON_EXTENSIONS:
        return read_json_file(path, *subsection, encoding=encoding)
    elif e in YAML_EXTENSIONS:
        return read_yaml_file(path, *subsection, encoding=encoding)

    raise RuntimeError(f"Unsupported file extension: {extension}")


def read_config_file(
    path: Union[str, Path],
    *subsection: str,
    encoding="utf-8",
) -> Namespace:
    path = path if isinstance(path, str) else str(path)
    assert isinstance(path, str)
    ext = os.path.splitext(path)[1]
    return read_config_file_by_extension(path, ext, *subsection, encoding=encoding)


def read_config_file_if_readable(
    path: Union[str, Path],
    *subsection: str,
    encoding="utf-8",
) -> Optional[Namespace]:
    if not path:
        return None
    try:
        if not os.path.isfile(path):
            return None
        if not os.access(path, os.R_OK):
            return None
        return read_config_file(path, *subsection, encoding=encoding)
    except BaseException as e:  # noqa
        return None
