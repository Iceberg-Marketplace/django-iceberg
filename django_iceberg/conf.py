# -*- coding: utf-8 -*-

from django.conf import settings


# Debug/Local
class ConfigurationDebug:
    ICEBERG_API_URL = "http://api.local.iceberg.technology"
    ICEBERG_API_PORT = 8000
    ICEBERG_API_PRIVATE_KEY = getattr(settings, 'ICEBERG_API_PRIVATE_KEY_DEBUG', None)

    ICEBERG_CORS = "http://api.local.iceberg.technology:8000/cors/"

    ICEBERG_API_URL_FULL = "%s:%s" % (ICEBERG_API_URL, ICEBERG_API_PORT)
    ICEBERG_API_VERSION = "v1"
    ICEBERG_AUTH_HEADER = "IcebergAccessToken"
    ICEBERG_DEFAULT_LANG = "en"

    ICEBERG_SANDBOX_CORS = "http://api.sandbox.local.iceberg.technology:8000/cors/"


class ConfigurationDebugSandbox:
    ICEBERG_API_URL = "http://api.sandbox.local.iceberg.technology"
    ICEBERG_API_PORT = 8000
    ICEBERG_API_PRIVATE_KEY = getattr(settings, 'ICEBERG_API_PRIVATE_KEY_DEBUG_SANDBOX', None)

    ICEBERG_CORS = "http://api.sandbox.local.iceberg.technology:8000/cors/"

    ICEBERG_API_URL_FULL = "%s:%s" % (ICEBERG_API_URL, ICEBERG_API_PORT)
    ICEBERG_API_VERSION = "v1"
    ICEBERG_AUTH_HEADER = "IcebergAccessToken"
    ICEBERG_DEFAULT_LANG = "en"
    ICEBERG_ENV = "sandbox"


# NOT LOCAL
class ConfigurationSandbox:
    ICEBERG_API_URL = "http://api.sandbox.iceberg.technology"
    ICEBERG_API_PORT = 80
    ICEBERG_API_PRIVATE_KEY = getattr(settings, 'ICEBERG_API_PRIVATE_KEY_SANDBOX', None)
    ICEBERG_CORS = "http://api.sandbox.iceberg.technology/cors/"

    ICEBERG_API_URL_FULL = "%s:%s" % (ICEBERG_API_URL, ICEBERG_API_PORT)
    ICEBERG_API_VERSION = "v1"
    ICEBERG_AUTH_HEADER = "IcebergAccessToken"
    ICEBERG_DEFAULT_LANG = "en"
    ICEBERG_ENV = "sandbox"


class ConfigurationStage:
    ICEBERG_API_URL = "http://api.stage.iceberg.technology"
    ICEBERG_API_PORT = 80
    ICEBERG_API_PRIVATE_KEY = getattr(settings, 'ICEBERG_API_PRIVATE_KEY_STAGE', None)
    ICEBERG_CORS = "http://api.stage.iceberg.technology/cors/"

    ICEBERG_API_URL_FULL = "%s:%s" % (ICEBERG_API_URL, ICEBERG_API_PORT)
    ICEBERG_API_VERSION = "v1"
    ICEBERG_AUTH_HEADER = "IcebergAccessToken"
    ICEBERG_DEFAULT_LANG = "en"


