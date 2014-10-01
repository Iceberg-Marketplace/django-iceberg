# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
# from django.core.exceptions import ValidationError

from .models import UserIcebergModel

User = get_user_model()

class UserShoppingPreferencesForm(forms.Form):
    CURRENCY_CHOICES = (
        ('EUR', _('Euro')),
        ('USD', _('Dollar'))
    )

    currency = forms.ChoiceField(
        label = _("Currency"),
        choices = CURRENCY_CHOICES,
        required = False,
    )

    SHIPPING_COUNTRY_CHOICES = (
        ('FR', _('France')),
        ('UK', _('United Kingdom')),
        ('AU', _('Australia')),
        ('BE', _('Belgium')),
    )
    shipping_country = forms.ChoiceField(
        label = _("Shipping Country"),
        choices = SHIPPING_COUNTRY_CHOICES,
        required = False,
    )

    def save(self, user):
        user_iceberg_model, created = UserIcebergModel.objects.get_or_create(user = user)

        user_iceberg_model.shipping_country =  self.cleaned_data.get('shipping_country', None)
        user_iceberg_model.currency = self.cleaned_data.get('currency', None)
        user_iceberg_model.sync_shopping_preferences()
        user_iceberg_model.save()



