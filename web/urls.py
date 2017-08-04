# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.conf.urls import url
from django.views.static import serve

from .views import ShowTemplate


IMG_DIR = os.path.join(os.path.dirname(__file__), os.pardir, 'static', 'img')


urlpatterns = [
	url(r'^$', ShowTemplate.as_view(), kwargs={'template': 'index.html'}),
	url(r'^(?P<path>favicon\.ico)$', serve, {'document_root': IMG_DIR}),
	url(r'^(?P<template>.*)$', ShowTemplate.as_view()),
]
