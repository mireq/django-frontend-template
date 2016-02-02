# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template


@register.filter
def get_sequence(value):
	"""
	Return sequence of defined length. Usage:

	{% for x in 3|get_range %}
		<li>{{ x }}</li>
	{% endfor %}
	"""
	return range(int(value))
