# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.views.static import serve

from .views import ShowTemplate


IMG_DIR = os.path.join(os.path.dirname(__file__), os.pardir, 'static', 'img')


urlpatterns = []

if settings.DEBUG:
	urlpatterns.append(path('style/', TemplateView.as_view(template_name='partials/style.html')))
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
	path('admin/', admin.site.urls),
	path('', ShowTemplate.as_view(), kwargs={'template': 'index.html'}),
	re_path(r'(?P<path>favicon\.ico)', serve, {'document_root': IMG_DIR}),
	path('<path:template>', ShowTemplate.as_view()),
]
