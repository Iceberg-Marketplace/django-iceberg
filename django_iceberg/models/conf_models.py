# -*- coding: utf-8 -*-

from copy import copy

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.conf.global_settings import LANGUAGES
from django.utils.translation import ugettext_lazy as _

DEFAULT_ICEBERG_ENV = getattr(settings, 'ICEBERG_DEFAULT_ENVIRO', "prod")
IMAGE_SERVER_URL = getattr(settings, 'ICEBERG_IMAGE_SERVER_URL', None)


class IcebergConfigurationBase(models.Model):

    """ Abstract model that can store an Iceberg Configuration """

    class Meta:
        abstract = True

    PROD_ENV = "prod"
    STAGE_ENV = "stage"
    SANDBOX_ENV = "sandbox"
    SANDBOX_STAGE_ENV = "sandbox_stage"
    ENV_CHOICES = (
        (PROD_ENV, _("Production")),
        (STAGE_ENV, _("Stage Production")),
        (SANDBOX_ENV, _("Sandbox")),
        (SANDBOX_STAGE_ENV, _("Stage Sandbox")),
    )
    iceberg_environment = models.CharField(max_length=32, choices=ENV_CHOICES, default=DEFAULT_ICEBERG_ENV, db_index=True)

    iceberg_api_version = models.CharField(max_length=32, default="v1")
    iceberg_auth_header = models.CharField(max_length=128, default="IcebergAccessToken")
    iceberg_default_lang = models.CharField(max_length=2, default="en", choices=LANGUAGES)

    PRODUCTION_API_URL = "https://api.iceberg.technology"
    SANDBOX_API_URL = "https://api.sandbox.iceberg.technology"
    LOCAL_PRODUCTION_API_URL = "http://api.local.iceberg.technology"
    LOCAL_SANDBOX_API_URL = "http://api.sandbox.local.iceberg.technology"

    API_URL_CHOICES = (
        (PRODUCTION_API_URL, _("Production")),
        (SANDBOX_API_URL, _("Sandbox")),
        (LOCAL_PRODUCTION_API_URL, _("Local Production")),
        (LOCAL_SANDBOX_API_URL, _("Local Sandbox")),
    )

    # no URLField because we want no trailing slash
    iceberg_api_url = models.CharField(max_length=512, default=SANDBOX_API_URL, choices=API_URL_CHOICES)

    iceberg_api_port = models.PositiveSmallIntegerField(default=443)

    iceberg_cors_url = models.CharField(
        max_length=512, blank=True, null=True, default="/cors/",
        help_text=_("CORS urls, can be relative to iceberg_api_url or absolute")
    )

    DEFAULT_ICEBERG_MODULES_URL = "http://connect.iceberg-marketplace.com/modules/"
    iceberg_modules_url = models.CharField(max_length=512, default=DEFAULT_ICEBERG_MODULES_URL)

    # keys
    iceberg_api_private_key = models.CharField(max_length=512, blank=True, null=True)
    iceberg_application_namespace = models.CharField(max_length=512, blank=True, null=True)
    iceberg_application_secret_key = models.CharField(max_length=512, blank=True, null=True)
    iceberg_application_staff_email = models.EmailField(blank=True, null=True)
    iceberg_application_staff_first_name = models.CharField(max_length=128, blank=True, null=True)
    iceberg_application_staff_last_name = models.CharField(max_length=128, blank=True, null=True)

    image_server_url = models.URLField(max_length=512, blank=True, null=True)

    @property
    def iceberg_api_url_full(self):
        if not self.iceberg_api_url:
            return ""
        return "%s:%s" % (self.iceberg_api_url, self.iceberg_api_port)

    @property
    def iceberg_cors(self):
        if not self.iceberg_cors_url:
            return ""
        if self.iceberg_cors_url.startswith("http"):
            # absolute url
            return self.iceberg_cors_url
        else:
            return "%s%s" % (self.iceberg_api_url_full, self.iceberg_cors_url)

    def get_iceberg_configuration(self, base_conf=None):
        """
        Returns the iceberg configuration starting from given base_conf (or ConfigurationBase if None)
        and overwriting it with values if set in object
        """
        from icebergsdk.conf import ConfigurationBase

        if base_conf is None:
            conf = ConfigurationBase()
        elif type(base_conf) == type:
            # instanciate class
            conf = base_conf()
        else:
            # copying base_conf to be sure it's not modified and used somewhere else
            conf = copy(base_conf)

        conf.ICEBERG_ENV = self.iceberg_environment

        if self.iceberg_api_version:
            conf.ICEBERG_API_VERSION = self.iceberg_api_version
        if self.iceberg_auth_header:
            conf.ICEBERG_AUTH_HEADER = self.iceberg_auth_header
        if self.iceberg_default_lang:
            conf.ICEBERG_DEFAULT_LANG = self.iceberg_default_lang
        if self.iceberg_api_url:
            conf.ICEBERG_API_URL = self.iceberg_api_url
            conf.ICEBERG_API_URL_FULL = self.iceberg_api_url_full
        if self.iceberg_api_port:
            conf.ICEBERG_API_PORT = self.iceberg_api_port
        if self.iceberg_cors:
            conf.ICEBERG_CORS = self.iceberg_cors
        if self.iceberg_modules_url:
            conf.ICEBERG_MODULES_URL = self.iceberg_modules_url

        if self.iceberg_api_private_key:
            conf.ICEBERG_API_PRIVATE_KEY = self.iceberg_api_private_key

        if self.iceberg_application_namespace:
            conf.ICEBERG_APPLICATION_NAMESPACE = self.iceberg_application_namespace

        if self.iceberg_application_secret_key:
            conf.ICEBERG_APPLICATION_SECRET_KEY = self.iceberg_application_secret_key

        conf.IMAGE_SERVER_URL = IMAGE_SERVER_URL  # TODO add it as model field

        return conf

    def get_api_handler(self, sso_as_application_staff=False):
        from icebergsdk.api import IcebergAPI
        api_handler = IcebergAPI(conf=self.get_iceberg_configuration())
        if sso_as_application_staff:
            api_handler.sso_user(
                email=self.iceberg_application_staff_email,
                first_name=self.iceberg_application_staff_first_name,
                last_name=self.iceberg_application_staff_last_name,
            )
        return api_handler

    def check_valid_credentials(self):
        try:
            api_handler = self.get_api_handler(sso_as_application_staff=True)
            me_user = api_handler.User.me()
        except Exception, e:
            raise ValidationError(e.message)

        if me_user.username == "anonymous":
            raise ValidationError("Should not be anonymous")

        if me_user.email != self.iceberg_application_staff_email:
            raise ValidationError("Not logged as %s" % self.iceberg_application_staff_email)

        if not me_user.is_application_staff:
            raise ValidationError("User %s is not staff on app %s" %
                                  (self.iceberg_application_staff_email, self.iceberg_application_namespace)
                                  )

        return True

    def clean(self):
        self.check_valid_credentials()
