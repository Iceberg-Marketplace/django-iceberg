# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from django_iceberg.auth_utils import init_iceberg, get_conf_class

def iceberg_settings(request):
    """
    Defines some template variables in context
    """
    conf = get_conf_class(request.user)

    if not conf:
        ICEBERG_API_URL_FULL = "https://api.iceberg.technology"
        ICEBERG_CORS = "https://api.iceberg.technology/cors/"
    else:
        iceberg_env = getattr(conf, 'ICEBERG_ENV', 'prod')
        ICEBERG_API_URL_FULL = conf.ICEBERG_API_URL_FULL
        ICEBERG_CORS = conf.ICEBERG_CORS

    res = {
        "ICEBERG_ENV": iceberg_env,
        "ICEBERG_API_URL": ICEBERG_API_URL_FULL,
        "ICEBERG_CORS": ICEBERG_CORS,
    }

    if request.user.is_authenticated():
        res['access_token'] = init_iceberg(request).access_token
    else:
        res['access_token'] = "anonymous"
    return res
