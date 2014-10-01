# -*- coding: utf-8 -*-

from django.contrib import admin

from django_iceberg.models import UserIcebergModel

class UserIcebergModelAdmin(admin.ModelAdmin):
    list_display   = ('user', 'environment', 'last_updated', 'application_namespace')
    raw_id_fields = ("user",)


admin.site.register(UserIcebergModel, UserIcebergModelAdmin)
