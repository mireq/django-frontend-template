# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template


register = template.Library()


@register.filter
def get_sequence(value):
	"""
	Return sequence of defined length. Usage:

	{% for x in 3|get_sequence %}
		<li>{{ x }}</li>
	{% endfor %}
	"""
	return range(int(value))
