# -*- coding: utf-8 -*-

from django.contrib import admin

from django_iceberg.models import UserIcebergEnvironment

class UserIcebergEnvironmentAdmin(admin.ModelAdmin):
    list_display   = ('user', 'environment', 'last_updated')
    raw_id_fields = ("user",)


admin.site.register(UserIcebergEnvironment, UserIcebergEnvironmentAdmin)
