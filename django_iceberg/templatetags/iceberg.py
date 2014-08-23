# -*- coding: utf-8 -*-

import json

from django import template
from django.conf import settings

register = template.Library()

from django_iceberg.auth_utils import init_iceberg 

@register.inclusion_tag('django_iceberg/javascript_sdk.html', takes_context=True)
def iceberg_javascript_sdk(context):
    """
    To Finish
    """
    if getattr(settings, 'ICEBERG_USE_LOCAL', False):
        livrary_path = 'http://connect.local.iceberg-marketplace.com:9000/script.js'
    else:
        livrary_path = 'http://connect.iceberg-marketplace.com/script.js'
    return {
        'LIBRARY_URL': livrary_path
    }


@register.inclusion_tag('django_iceberg/sso.html', takes_context=True)
def iceberg_sso(context):
    api_handler = init_iceberg(context['request'])

    if hasattr(api_handler, '_sso_response'):
        return {
            'appNamespace': api_handler.conf.ICEBERG_APPLICATION_NAMESPACE,
            "sso_data": json.dumps(api_handler._sso_response)
        }
    else:
        return {}

    
    



