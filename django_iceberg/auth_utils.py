# -*- coding: utf-8 -*-

from icebergsdk.api import IcebergAPI

from django.conf import settings

from django_iceberg.models import UserIcebergEnvironment
from django_iceberg.conf import ConfigurationDebug, ConfigurationDebugSandbox, ConfigurationSandbox, ConfigurationStage


def get_environment(user):
    try:
        if user.is_authenticated():
            enviro = UserIcebergEnvironment.objects.get(user = user)
            return enviro.environment
    except UserIcebergEnvironment.DoesNotExist:
        pass
        
    return UserIcebergEnvironment.ICEBERG_PROD


def get_conf_class(user):
    enviro = get_environment(user)

    if getattr(settings, 'ICEBERG_USE_LOCAL', False):
        if enviro == UserIcebergEnvironment.ICEBERG_SANDBOX:
            conf = ConfigurationDebugSandbox
        else:
            conf = ConfigurationDebug
    else:
        if enviro == UserIcebergEnvironment.ICEBERG_SANDBOX:
            conf = ConfigurationSandbox
        elif enviro == UserIcebergEnvironment.ICEBERG_STAGE:
            conf = ConfigurationStage
        else:
            conf = None

    return conf

def sync_user_with_plateform(user):
    return IcebergAPI(conf = get_conf_class(user)).auth_user(user.username, user.email, first_name = user.first_name, last_name = user.last_name, is_staff = user.is_staff, is_superuser = user.is_superuser)


def init_iceberg(request):
    if not 'access_token' in request.session:
        api_handler = sync_user_with_plateform(request.user)
        request.session['access_token'] = api_handler.access_token
    else:
        api_handler = IcebergAPI(username = request.user.username, access_token = request.session['access_token'], conf = get_conf_class(request.user))
    
    return api_handler


