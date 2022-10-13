# -*- coding: utf-8 -*-

from generalize_config.generalize import read_generalize_configs
from generalize_config.namespace.merge import merge_left_first, merge_right_first
from generalize_config.namespace.strip import strip_none_attributes
from generalize_config.parser.cfg_parse import read_cfg_file
from generalize_config.parser.env_parse import read_os_envs, read_os_envs_file
from generalize_config.parser.json_parse import read_json_file
from generalize_config.parser.yaml_parse import read_yaml_file
from generalize_config.read_config import read_config_file, read_config_file_if_readable

__version__ = "1.3.0"

__all__ = (
    "__version__",
    "merge_left_first",
    "merge_right_first",
    "read_cfg_file",
    "read_config_file",
    "read_config_file_if_readable",
    "read_generalize_configs",
    "read_json_file",
    "read_os_envs",
    "read_os_envs_file",
    "read_yaml_file",
    "strip_none_attributes",
)
