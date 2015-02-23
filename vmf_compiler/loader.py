#!/usr/bin/env python3

"""
Tools for loading presets/configuration files.
"""

import os
from gi.repository import Gtk

from pprint import pprint

CONFIG_STOCK = './configurations/'
CONFIG_USER = '~/.config/crowbar/compiler/'
CONFIG_EXT = '.csh'
PROFILE_DEFAULT = 'Default'

def read_configs():
    """
        Open default configurations

        Returns:
            list: Configuration file bodies.

    """
    configs_paths = reload_config_files()

    configs = list()
    for config_path in configs_paths:
        name = os.path.splitext(os.path.basename(config_path))[0]
        with open(config_path, 'r') as file_handle:
            configs.append({
                'name': name,
                'path': config_path,
                'body': file_handle.read(),
            })

    return configs


def get_default_directories():
    """
        Gets the default directories.
    """
    return [os.path.expanduser(i) for i in [CONFIG_STOCK, CONFIG_USER]]


def reload_config_files(config_dirs=None, ext=None):
    """
        Locates config file configs_paths

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


def reload_profiles():
    """
        Read and parse all config files.

        Returns:
            list: of dicts, the parsed configs named by...
    """
    raw_configs = read_configs()

    config = {
        'byName': dict(),
        'byFileName': dict(),
        'byFilePath': dict(),
        'asListStore': Gtk.ListStore(str),
    }

    for raw_config in raw_configs:
        body_lines = raw_config['body'].splitlines()
        proper_name = body_lines.pop(0).lstrip('# ').rstrip()
        config_lines = {
            'file_name': raw_config['name'],
            'file_path': raw_config['path'],
            'list_raw': [],
            'ListStore': Gtk.ListStore(bool, str, str),
            'name': proper_name,
            'raw': raw_config['body'],
        }
        config['byName'][proper_name] = config_lines
        config['byFileName'][raw_config['name']] = config_lines
        config['byFilePath'][raw_config['path']] = config_lines
        for line in body_lines:
            # bool, str, str
            raw_values = [
                not line.startswith('#'),
                line.lstrip('# '),
                line,
            ]
            config_lines['list_raw'].append(raw_values)
            config_lines['ListStore'].append(raw_values)


        # TODO: Find the index of PROFILE_DEFAULT instead of
        # inserting it as zero.
        # TODO: Change list store primary key to file path
        if proper_name == PROFILE_DEFAULT:
            config['asListStore'].prepend([proper_name])
        else:
            config['asListStore'].append([proper_name])

    return config


def main():
    """
        Default Functionality
    """
    pprint(read_configs())


if __name__ == '__main__':
    main()
