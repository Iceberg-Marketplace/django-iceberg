# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django_iceberg.models import UserIcebergEnvironment

@csrf_exempt
@login_required
def switch_env(request, **kwargs):
    environment = request.POST.get('environment', None)
    if not environment:
        return HttpResponse(status = 400)


    user_env_conf, created = UserIcebergEnvironment.objects.get_or_create(user = request.user)
    user_env_conf.environment = environment
    try:
        user_env_conf.save()
    except:
        return HttpResponse(status = 500)

    success_url = request.GET.get('next', False) or request.POST.get('next', False) or "/"
    return HttpResponseRedirect(success_url)

