# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns

urlpatterns = patterns('django_iceberg.views',
    url(r"^switch_env$", 'switch_env', name="django_iceberg_switch_env"),
)