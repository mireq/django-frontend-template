# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from compressor.filters import CompilerFilter
from django.conf import settings


class PostcssFilter(CompilerFilter):
	command = "{binary} {args}"
	options = (
		("binary", settings.COMPRESS_POSTCSS_BINARY),
		("args", settings.COMPRESS_POSTCSS_ARGS),
	)
