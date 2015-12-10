# -*- coding: utf-8 -*-
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from django_iceberg.models import UserIcebergModel
from django_iceberg.auth_utils import init_iceberg
from django_iceberg.forms import UserShoppingPreferencesForm
from django.views.generic.edit import FormView

import logging
logger = logging.getLogger(__name__)

def switch_user_env(request, environment):
    user_env_conf, created = UserIcebergModel.objects.get_or_create(user = request.user)
    user_env_conf.switch_env(environment)
    init_iceberg(request, force_reload = True)


def class_view_decorator(function_decorator):
    """Convert a function based decorator into a class based decorator usable
    on class based Views.

    Can't subclass the `View` as it breaks inheritance (super in particular),
    so we monkey-patch instead.
    """

    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return simple_decorator

@csrf_exempt
@login_required
def switch_env(request, **kwargs):
    environment = request.POST.get('environment', request.GET.get('environment', None))

    if not environment:
        return HttpResponse(status = 400)

    try:
        switch_user_env(request, environment)
    except Exception as err:
        logger.error(str(err))
        return HttpResponse(status = 500)

    success_url = request.GET.get('next', False) or request.POST.get('next', False) or "/"
    return HttpResponseRedirect(success_url)


@class_view_decorator(login_required)
@class_view_decorator(csrf_exempt)
class UpdateShoppingPreference(FormView):
    template_name = 'django_iceberg/shopping_preferences.html'
    form_class = UserShoppingPreferencesForm

    def get_initial(self):
        user_env_conf, created = UserIcebergModel.objects.get_or_create(user = self.request.user)
        initial = {}

        initial['currency'] = user_env_conf.currency
        initial['shipping_country'] = user_env_conf.shipping_country
        return initial

    def form_valid(self, form):
        form.save(self.request.user)
        return super(UpdateShoppingPreference, self).form_valid(form)

    def get_success_url(self):
        return reverse('django_iceberg_update_shopping_prefs')


@csrf_exempt
def webhook_endpoint(request, **kwargs):
    try:
        from django_iceberg import signals
        from django_iceberg.signals import webhook_received
        try:
            webhook_data = json.loads(request.body)
            event = webhook_data["event"]
        except (KeyError, ValueError) as err:
            logger.exception("in webhook_endpoint: bad request: ")
            return HttpResponse(status=400, content=str(err))

        ## generic webhook signal
        webhook_received.send(sender=None, webhook_data=webhook_data)

        ## looking for specific webhook signal
        signal_name = "%s_webhook" % event
        signal = getattr(signals, signal_name, None)
        if signal:
            logger.info("Received webhook event %s, forwarding it as signal %s",
                        event, signal_name)
            signal.send(sender=None, webhook_data=webhook_data)
        return HttpResponse(status = 202)
    except:
        logger.exception("in webhook_endpoint: ")
        return HttpResponse(status = 500)




