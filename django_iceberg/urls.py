# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from django.conf import settings

from django_iceberg.views import switch_env, UpdateShoppingPreference, webhook_endpoint

urlpatterns = patterns('',
    url(r"^switch_env$", switch_env, name="django_iceberg_switch_env"),
    url(r"^update_shopping_prefs/$", UpdateShoppingPreference.as_view(), name="django_iceberg_update_shopping_prefs"),
)

if getattr(settings, "ICEBERG_ACTIVATE_WEBHOOK_ENDPOINT", False):
    urlpatterns += patterns('',
        url(r"^webhook_endpoint$", webhook_endpoint, name="django_iceberg_webhook_endpoint"),
    )