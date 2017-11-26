# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from compressor.exceptions import FilterError
from compressor.filters import CompilerFilter
from django.conf import settings


logger = logging.getLogger('django.request')


class PostcssFilter(CompilerFilter):
	command = "{binary} {args}"
	options = (
		("binary", getattr(settings, 'COMPRESS_POSTCSS_BINARY', 'postcss')),
		("args", getattr(settings, 'COMPRESS_POSTCSS_ARGS', '--use autoprefixer')),
	)

	def input(self, **kwargs):
		try:
			return super(PostcssFilter, self).input(**kwargs)
		except FilterError:
			logger.exception("Compiler error")
			return self.content
