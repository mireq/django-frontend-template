# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import glob
import json
import os
import re
import subprocess


SIZES = (
	(1, ''),
	(2, '@2x'),
)


IGNORE_PATTERNS = [
	re.compile(r'^original/.*$'),
	re.compile(r'^placeholder/.*$'),
	re.compile(r'^favicon/.*$'),
]


def process_pngquant(filename, settings):
	settings = {item.split('=', 1)[0]: item.split('=', 1)[1] for item in settings.split(':')}
	settings.setdefault('quality', '100')
	cmd_args = ['pngquant', '--nofs', '--quality', settings['quality'], '-f', '--ext', '.png', filename]
	subprocess.call(cmd_args)


def convert_svg(force_convert=None):
	svg_files = [os.path.splitext(filename)[0] for filename in glob.glob(os.path.join(os.path.dirname(__file__), "**/*.svg"), recursive=True)]
	svg_files = [f[len(os.path.dirname(__file__)):].lstrip("/") for f in svg_files]
	images_settings = {}
	if force_convert is None:
		force_convert = set()
	try:
		with open('images.json', 'r') as fp:
			images_settings = json.load(fp)
	except FileNotFoundError:
		pass
	for filename in svg_files:
		ignore = False
		for pattern in IGNORE_PATTERNS:
			if pattern.match(filename):
				ignore = True
				break
		if ignore:
			continue
		settings = images_settings.get(filename, {})
		for size, suffix in SIZES:
			out_filename = os.path.abspath(os.path.join(os.path.dirname(__file__), filename + suffix + '.png'))
			if not os.path.exists(out_filename) or (filename + '.svg') in force_convert:
				cmd_args = ['inkscape', os.path.abspath(os.path.join(os.path.dirname(__file__), filename + '.svg')), '-e', out_filename, '-d', str(96 * size)]
				subprocess.call(cmd_args)
				if 'pngquant' in settings:
					process_pngquant(out_filename, settings['pngquant'])
				cmd_args = ['optipng', '-o7', out_filename]
				subprocess.call(cmd_args)
				cmd_args = ['advpng', '-z', '-4', out_filename]
				subprocess.call(cmd_args)
				cmd_args = ['pngout-static', '-k0', out_filename]
				subprocess.call(cmd_args)

def main():
	convert_svg()


if __name__ == "__main__":
	main()
