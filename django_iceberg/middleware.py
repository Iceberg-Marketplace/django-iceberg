# -*- coding: utf-8 -*-

from django_iceberg.views import switch_user_env
  
class IcebergMiddleware(object):
    """
    Set the language for the site based on the subdomain the request
    is being served on. For example, serving on 'fr.domain.com' would
    make the language French (fr).
    """ 
    def process_request(self, request):
        iceberg_enviro = request.GET.get("iceberg_enviro", None)
        if iceberg_enviro:
            iceberg_enviro = iceberg_enviro.lower()

            switch_user_env(request, iceberg_enviro)

