# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import glob
import os
import subprocess


SIZES = (
	(1, ''),
	(2, '@2x'),
)


def convert_svg():
	svg_files = [os.path.splitext(filename)[0] for filename in glob.glob("*.svg")]
	for filename in svg_files:
		for size, suffix in SIZES:
			if not os.path.exists(filename + suffix + '.png'):
				cmd_args = ['inkscape', filename + '.svg', '-e', filename + suffix + '.png', '-d', '%d' % (90 * size)]
				subprocess.call(cmd_args)


def main():
	convert_svg()


if __name__ == "__main__":
	main()
