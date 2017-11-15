# -*- coding: utf-8 -*-
from __future__ import unicode_literals



ASSETS = {
}

SPRITES = (
	{
		'name': 'sprites',
		'output': 'img/sprites_generated.png',
		'scss_output': 'css/_sprites_generated.scss',
		'extra_sizes': ((2, '@2x'),),
		'width': 256,
		'height': 512,
		'images': (
			# place larger first
			{ 'name': 'check', 'src': 'img/sprites/check.png' },
			{ 'name': 'radio', 'src': 'img/sprites/radio.png' },
		),
	},
)
