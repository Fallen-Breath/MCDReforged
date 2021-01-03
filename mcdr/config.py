"""
MCDR config file stuffs
"""
import os

import ruamel.yaml as yaml

from mcdr.logger import DebugOption


class Config:
	def __init__(self, mcdr_server, file_name):
		self.mcdr_server = mcdr_server
		self.data = None
		self.file_name = file_name

	def read_config(self):
		if os.path.isfile(self.file_name):
			with open(self.file_name, encoding='utf8') as file:
				self.data = yaml.round_trip_load(file)
		self.check_config()

	def save(self):
		with open(self.file_name, 'w', encoding='utf8') as file:
			yaml.round_trip_dump(self.data, file)

	def touch(self, key, default):
		if self.data is None:
			self.data = {}
		if key not in self.data:
			self.data[key] = default
			self.mcdr_server.logger.warning('Option "{}" missing, use default value "{}"'.format(key, default))
			return True
		return False

	def check_config(self):
		flag = False
		flag |= self.touch('language', 'en_us')
		flag |= self.touch('working_directory', 'server')
		flag |= self.touch('plugin_folders', ['./plugins'])
		flag |= self.touch('start_command', '')
		flag |= self.touch('parser', 'vanilla_parser')
		flag |= self.touch('encoding', None)
		flag |= self.touch('decoding', None)
		flag |= self.touch('console_command_prefix', '!!')
		flag |= self.touch('enable_rcon', False)
		flag |= self.touch('rcon_address', '127.0.0.1')
		flag |= self.touch('rcon_port', 25575)
		flag |= self.touch('rcon_password', 'password')
		flag |= self.touch('disable_console_thread', False)
		flag |= self.touch('download_update', True)
		flag |= self.touch('debug', {
			DebugOption.ALL: False,
			DebugOption.PARSER: False,
			DebugOption.PLUGIN: False,
		})
		if flag:
			for line in self.mcdr_server.tr('config.missing_config').splitlines():
				self.mcdr_server.logger.warning(line)
			self.save()

	def __getitem__(self, item):
		return self.data[item]

	# -------------------------
	#   Actual data analyzers
	# -------------------------

	def is_debug_on(self):
		for value in self.data['debug']:
			if value is True:
				return True
		return False