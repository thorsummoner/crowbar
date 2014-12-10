#!/usr/bin/env python3

import os

from pprint import pprint

CONFIG_STOCK = './configurations/'
CONFIG_USER = '~/.config/crowbar/compiler/'
CONFIG_EXT = '.csh'

def read_configs():
	config_dirs = (os.path.expanduser(static) for static in [CONFIG_STOCK, CONFIG_USER])
	configs_paths = []
	for config_dir in config_dirs:
		try:
			abspath, _, config_files = next(os.walk(config_dir))
		except StopIteration:
			print('Notice: Could not load from config dir `%s`.' % config_dir)
			continue

		for config_file in config_files:
			if not config_file.endswith(CONFIG_EXT):
				continue
			configs_paths.append(os.path.realpath(os.path.join(abspath, config_file)))

	config_bodys = {}
	for config_path in configs_paths:
		name = os.path.splitext(os.path.basename(config_path))[0]
		with open(config_path, 'r') as fh:
			# The order of loading should allow a user to define and override
			# presets
			config_bodys[name] = fh.read()

	return config_bodys

if __name__ == '__main__':
	configs = read_configs()
	pprint(configs)
