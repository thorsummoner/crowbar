#!/usr/bin/env python3

"""
Tools for loading presets/configuration files.
"""

import os
import warnings

from pprint import pprint

CONFIG_STOCK = './configurations/'
CONFIG_USER = '~/.config/crowbar/compiler/'
CONFIG_EXT = '.csh'


def main():
    """Default Functionality """
    pprint(read_configs())


def read_configs():
    """Open default configurations

    Returns:
        list: Configuration file bodies.

    """
    configs_paths = reload_config_files()

    config_bodys = {}
    for config_path in configs_paths:
        name = os.path.splitext(os.path.basename(config_path))[0]
        with open(config_path, 'r') as file_handle:
            # The order of loading should allow a user to define and
            # override the preset versions
            config_bodys[name] = file_handle.read()

    return config_bodys


def get_default_directories():
    """Gets the default directories."""
    return [os.path.expanduser(i) for i in [CONFIG_STOCK, CONFIG_USER]]


def reload_config_files(config_dirs=None, ext=None):
    """Locates config file configs_paths

    Args:
        config_dirs (list): Directories to look in.

    Returns:
        list: File paths found in directories.
    """

    if config_dirs is None:
        config_dirs = get_default_directories()

    if ext is None:
        ext = CONFIG_EXT

    configs_paths = []
    for config_dir in config_dirs:
        try:
            abspath, _, config_files = next(os.walk(config_dir))
        except StopIteration:
            warn_msg = 'Notice: Could not load from config dir `%s`.'
            warnings.warn(warn_msg % config_dir)
            continue

        for config_file in config_files:
            if not config_file.endswith(ext):
                # Skip files of unknown extensions.
                continue
            # Append to the list of config files.
            configs_paths.append(
                os.path.realpath(os.path.join(abspath, config_file))
            )
    return configs_paths

if __name__ == '__main__':
    main()
