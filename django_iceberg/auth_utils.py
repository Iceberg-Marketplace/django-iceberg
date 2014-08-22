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
    conf = get_conf_class(user)

    if getattr(conf, "ICEBERG_API_PRIVATE_KEY", False):
        return IcebergAPI(conf = conf).auth_user(user.username, user.email, first_name = user.first_name, last_name = user.last_name, is_staff = user.is_staff, is_superuser = user.is_superuser)
    else:
        return IcebergAPI(conf = conf).sso_user(
            email = user.email,
            first_name = user.first_name or "Temp",
            last_name = user.last_name or "Temp"
        )


def init_iceberg(request):
    """
    Main function to get an api_handler for the current user
    """
    if 'iceberg_auth_data' not in request.session:
        api_handler = sync_user_with_plateform(request.user)
        request.session['iceberg_auth_data'] = {
            "username": api_handler.username,
            "access_token": api_handler.access_token
        }
        if getattr(api_handler, '_sso_response', None):
            request.session['iceberg_auth_data']['sso_response'] = api_handler._sso_response

    else:
        api_handler = IcebergAPI(username = request.session['iceberg_auth_data']['username'], access_token = request.session['iceberg_auth_data']['access_token'], conf = get_conf_class(request.user))
        if "sso_response" in request.session['iceberg_auth_data']:
            api_handler._sso_response = request.session['iceberg_auth_data']['sso_response']
    
    return api_handler


