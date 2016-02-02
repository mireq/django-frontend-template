# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import ShowTemplate


urlpatterns = [
	url('^$', ShowTemplate.as_view(), kwargs={'template': 'index.html'}),
	url('^(?P<template>.*)$', ShowTemplate.as_view()),
]
