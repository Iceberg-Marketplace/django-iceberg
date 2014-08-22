# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

class UserIcebergEnvironment(models.Model):
    ICEBERG_PROD, ICEBERG_SANDBOX, ICEBERG_STAGE = range(1, 4)
    ENVIRONMENT_CHOICES = (
        (ICEBERG_PROD, _('Iceberg Prod')),
        (ICEBERG_SANDBOX, _('Iceberg Sandbox')),
        (ICEBERG_STAGE, _('Iceberg Stage')), # Use for migration
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    environment = models.PositiveSmallIntegerField(choices=ENVIRONMENT_CHOICES, default=1)
    last_updated = models.DateTimeField(auto_now = True) # 




