# -*- coding: utf-8 -*-

from argparse import ArgumentParser, Namespace
from typing import Optional, Sequence

from generalize_config.namespace.merge import merge_left_first
from generalize_config.parser.env_parse import read_os_envs, read_os_envs_file
from generalize_config.read_config import read_config_file


def read_generalize_configs(
    parser: ArgumentParser,
    subsection: str,
    env_prefix: str,
    env_suffix="_FILE",
    config_key="config",
    force: Optional[Namespace] = None,
    default: Optional[Namespace] = None,
    commandline: Optional[Sequence[str]] = None,
) -> Namespace:
    init = Namespace()
    cmds = parser.parse_known_args(commandline)[0]
    cmds_config = getattr(cmds, config_key, None)
    cfg1 = read_config_file(cmds_config, subsection) if cmds_config else None
    envs = read_os_envs(prefix=env_prefix)
    envs_config = getattr(envs, config_key, None)
    cfg2 = read_config_file(envs_config, subsection) if envs_config else None
    envfiles = read_os_envs_file(prefix=env_prefix, suffix=env_suffix)
    return merge_left_first(init, force, cmds, cfg1, envs, cfg2, envfiles, default)
