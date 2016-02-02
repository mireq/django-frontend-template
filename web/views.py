# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView


class ShowTemplate(TemplateView):
	def get_template_names(self):
		return (self.kwargs['template'],)
