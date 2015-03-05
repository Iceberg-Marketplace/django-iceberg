# -*- coding: utf-8 -*-

import json
import logging

from icebergsdk.api import IcebergAPI

from django.conf import settings

from django_iceberg.models import UserIcebergModel
from django_iceberg.conf import ConfigurationDebug, ConfigurationDebugSandbox, ConfigurationSandbox, ConfigurationSandboxStage, ConfigurationStage, ConfigurationProd


"""
To Do: Add birth_date
"""

logger = logging.getLogger(__name__)


def get_iceberg_model(request):
    if not hasattr(request, '_iceberg_model'):
        user_iceberg_model, created = UserIcebergModel.objects.get_or_create(user = request.user)
        setattr(request, '_iceberg_model', user_iceberg_model)

    return request._iceberg_model


def get_environment(request):
    if request.user.is_authenticated():
        iceberg_model = get_iceberg_model(request)
        return iceberg_model.environment
        
    return None


def get_conf_class(request, enviro = None):
    """
    Return the Configuration class for the given enviro
    """
    if not enviro:
        enviro = get_environment(request)

    if getattr(settings, 'ICEBERG_USE_LOCAL', False):
        if not enviro:
            enviro = getattr(settings, 'ICEBERG_DEFAULT_ENVIRO', None)

        if enviro == UserIcebergModel.ICEBERG_SANDBOX:
            conf = ConfigurationDebugSandbox
        else:
            conf = ConfigurationDebug
    else:
        if not enviro:
            enviro = getattr(settings, 'ICEBERG_DEFAULT_ENVIRO', None)

        if enviro == UserIcebergModel.ICEBERG_SANDBOX:
            conf = ConfigurationSandbox
        elif enviro == UserIcebergModel.ICEBERG_SANDBOX_STAGE:
            conf = ConfigurationSandboxStage
        elif enviro == UserIcebergModel.ICEBERG_STAGE:
            conf = ConfigurationStage
        else: # None or UserIcebergModel.ICEBERG_PROD
            conf = ConfigurationProd

    return conf


def save_api_handler_data(request, api_handler):
    user_iceberg_model = get_iceberg_model(request)

    user_iceberg_model.application_namespace = api_handler.conf.ICEBERG_APPLICATION_NAMESPACE
    user_iceberg_model.environment = getattr(api_handler.conf, 'ICEBERG_ENV', 'prod')
    user_iceberg_model.sso_data = json.dumps(api_handler._auth_response)
    user_iceberg_model.iceberg_username =  api_handler.username
    user_iceberg_model.access_token = api_handler.access_token

    if hasattr(api_handler.me(), 'language') and api_handler.me().language:
        user_iceberg_model.language = api_handler.me().language

    if hasattr(api_handler.me(), 'shopping_preference'):
        if api_handler.me().shopping_preference.country:
            user_iceberg_model.shipping_country = api_handler.me().shopping_preference.country

        if api_handler.me().shopping_preference.currency:
            user_iceberg_model.currency = api_handler.me().shopping_preference.currency

    user_iceberg_model.save()
    return user_iceberg_model

######
### IcebergAPI initialisation
######
def get_api_handler_for_user(request, force_reload = False, data = None, lang = None, conf = None):
    user = request.user

    if conf is None:
        ## default conf
        conf = get_conf_class(request)

    # # Check if we have a saved one
    # if not force_reload and ('iceberg_auth_response' in request.session):
    #     logger.debug('Found Iceberg Auth data in session')

    #     if ('username' in request.session['iceberg_auth_response']) and ('access_token' in request.session['iceberg_auth_response']):
    #         api_handler = IcebergAPI(conf = conf, lang = lang)
    #         api_handler._auth_response = request.session['iceberg_auth_response']
    #         api_handler.username = request.session['iceberg_auth_response']['username']
    #         api_handler.access_token = request.session['iceberg_auth_response']['access_token']

    #         return api_handler

    user_iceberg_model = get_iceberg_model(request)
    if user_iceberg_model.access_token:
        logger.debug('Found Iceberg Auth data in model')

        api_handler = IcebergAPI(conf = conf, lang = lang)
        api_handler._auth_response = json.loads(user_iceberg_model.sso_data)
        api_handler.username = user_iceberg_model.iceberg_username
        api_handler.access_token = user_iceberg_model.access_token
        return api_handler


    if getattr(conf, "ICEBERG_API_PRIVATE_KEY", False):  # ICEBERG_API_PRIVATE_KEY is used for Iceberg internal calls
        api_handler = IcebergAPI(conf = conf, lang = lang).auth_user(user.username, user.email, first_name = user.first_name, last_name = user.last_name, is_staff = user.is_staff, is_superuser = user.is_superuser)
    else:
        # Need to call the Iceberg API
        logger.debug('Will call Iceberg Auth SSO')

        if not data:
            data = {}

        data.update({
            "email": user.email,
            "first_name": user.first_name or "Temp",
            "last_name": user.last_name or "Temp"
        })

        api_handler = IcebergAPI(conf = conf, lang = lang).sso_user(**data)

    save_api_handler_data(request, api_handler)
    # # Keep it in session
    # request.session['iceberg_auth_response'] = api_handler._auth_response

    return api_handler


def get_api_handler_for_anonymous(request, force_reload = False, data = None, lang = None, conf=None):
    """
    Return the api_handler for an anonymous user
    """
    if conf is None:
        ## default conf
        conf = get_conf_class(request)

    if force_reload or ('iceberg_auth_response' not in request.session):
        api_handler = IcebergAPI(conf = conf, lang = lang).sso_user()

        # Keep it in session
        request.session['iceberg_auth_response'] = api_handler._auth_response

    else:
        api_handler = IcebergAPI(conf = conf, lang = lang)
        api_handler._auth_response = request.session['iceberg_auth_response']
        api_handler.username = request.session['iceberg_auth_response']['username']
        api_handler.access_token = request.session['iceberg_auth_response']['access_token']

    return api_handler


######
### django_iceberg main fonction
######
def init_iceberg(request, force_reload = False, data = None, lang = "en", conf=None):
    """
    Main function to get an api_handler for the current user
    """
    if not request.user.is_authenticated():
        api_handler = get_api_handler_for_anonymous(request, force_reload = force_reload, data = data, lang = lang, conf=conf)
    else:
        api_handler = get_api_handler_for_user(request, force_reload = force_reload, data = data, lang = lang, conf=conf)

    return api_handler






# def init_iceberg(request, force_reload = False):
#     """
#     Main function to get an api_handler for the current user
#     """
#     if force_reload or ('iceberg_auth_data' not in request.session):
#         api_handler = sync_user_with_plateform(request)
#         request.session['iceberg_auth_data'] = {
#             "username": api_handler.username,
#             "access_token": api_handler.access_token
#         }
#         if getattr(api_handler, '_auth_response', None):
#             request.session['iceberg_auth_data']['sso_response'] = api_handler._auth_response

#     else:
#         api_handler = IcebergAPI(username = request.session['iceberg_auth_data']['username'], access_token = request.session['iceberg_auth_data']['access_token'], conf = get_conf_class(request.user))
#         if "sso_response" in request.session['iceberg_auth_data']:
#             api_handler._auth_response = request.session['iceberg_auth_data']['sso_response']
    
#     return api_handler


