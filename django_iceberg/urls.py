# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from django.conf import settings

from django_iceberg import views

urlpatterns = patterns('',
    url(r"^switch_env$", views.switch_env, name="django_iceberg_switch_env"),
    url(r"^update_shopping_prefs/$", views.UpdateShoppingPreference.as_view(), name="django_iceberg_update_shopping_prefs"),
)

ICEBERG_ACTIVATE_WEBHOOK_ENDPOINT = getattr(settings, "ICEBERG_ACTIVATE_WEBHOOK_ENDPOINT", False)
ICEBERG_WEBHOOK_ENDPOINT = getattr(settings, "ICEBERG_WEBHOOK_ENDPOINT", "webhook_endpoint/")

if ICEBERG_ACTIVATE_WEBHOOK_ENDPOINT:
    urlpatterns += patterns('',
        url(r"^%s$" % ICEBERG_WEBHOOK_ENDPOINT, views.webhook_endpoint, name="django_iceberg_webhook_endpoint"),
    )