# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


DEFAULT_ICEBERG_ENV = getattr(settings, 'ICEBERG_DEFAULT_ENVIRO', "prod")

class IcebergBaseModel(models.Model):
    ICEBERG_PROD, ICEBERG_SANDBOX, ICEBERG_STAGE, ICEBERG_SANDBOX_STAGE = "prod", "sandbox", "stage", "sandbox_stage"
    ENVIRONMENT_CHOICES = (
        (ICEBERG_PROD, _('Iceberg - Prod')),
        (ICEBERG_STAGE, _('Iceberg - Prod Stage')), # PreProd
        (ICEBERG_SANDBOX, _('Iceberg - Sandbox')),
        (ICEBERG_SANDBOX_STAGE, _('Iceberg - Sandbox Stage')),
    )
    environment = models.CharField(choices=ENVIRONMENT_CHOICES, default=DEFAULT_ICEBERG_ENV, max_length = 20)
    iceberg_id = models.PositiveIntegerField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now = True)

    API_RESOURCE_NAME = None

    class Meta:
        abstract = True

    def iceberg_sync(self, api_handler):
        """
        Sync the local object from Iceberg version
        """
        raise NotImplementedError