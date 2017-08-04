# -*- coding: utf-8 -*-
from __future__ import unicode_literals



ASSETS = {
}

SPRITES = (
	{
		'name': 'sprites',
		'output': 'img/sprites_generated.png',
		'scss_output': 'css/_sprites_generated.scss',
		#'extra_sizes': ((2, '@2x'),),
		'extra_sizes': (),
		'width': 256,
		'height': 512,
		'images': (
			# large first
			{ 'name': 'cpu', 'src': 'img/sprites/cpu.png' },
			{ 'name': 'hdd', 'src': 'img/sprites/hdd.png' },
			{ 'name': 'vol', 'src': 'img/sprites/vol.png' },
		),
	},
)
