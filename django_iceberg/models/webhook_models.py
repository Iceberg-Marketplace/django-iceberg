
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from .base_models import IcebergBaseModel

from icebergsdk.api import IcebergAPI

WEBHOOK_MAX_TRIGGER_AGGREGATION = getattr(settings, 'WEBHOOK_MAX_TRIGGER_AGGREGATION', 200)
WEBHOOK_DEFAULT_AGGREGATION_DELAY = getattr(settings, 'WEBHOOK_DEFAULT_AGGREGATION_DELAY', 5*60)
WEBHOOK_DEFAULT_RETRY_DELAY = getattr(settings, 'WEBHOOK_DEFAULT_RETRY_DELAY', 15*60)
WEBHOOK_DEFAULT_MAX_ATTEMPTS = getattr(settings, 'WEBHOOK_DEFAULT_MAX_ATTEMPTS', 5)
WEBHOOK_DEFAULT_MAX_TRIGGER_AGGREGATION = getattr(settings, 'WEBHOOK_DEFAULT_MAX_TRIGGER_AGGREGATION', 10)

import logging
logger = logging.getLogger(__name__)

class IcebergWebhook(IcebergBaseModel):
    EVENT_CHOICES = (
        ('user_payment_card_created', _('A user has added a new payment card')),
        ('merchant_paused', _('A merchant is now paused')),
        ('merchant_order_received', _('A merchant order is now received')),
        ('merchant_order_sent', _('A merchant order is now sent')),
        ('payment_status_changed', _('A payment object has its status updated')),
        ('merchant_stopped', _('A merchant is now stopped')),
        ('merchant_order_confirmed', _('A merchant order is now confirmed')),
        ('merchant_order_authorized', _('A new merchant order is now authorized')),
        ('new_merchant_available', _('A new merchant is available for your application')),
        ('merchant_order_cancelled', _('An authorized merchant order is now cancelled')),
        ('order_item_cancelled', _('An authorized order item is now cancelled')),
        ('user_profile_updated', _('A user profile has been updated')),
        ('merchant_activated', _('A merchant is now activated')),
        ('product_updated', _('An active product has been updated')),
        ('product_offer_updated', _('An active product offer has been updated')),
        ('user_payment_card_status_changed', _('A user payment card has its status changed')),
        ('cart_status_changed', _('A cart status has changed'))
     )
    event = models.CharField(max_length=100, choices=EVENT_CHOICES, db_index=True)
    url = models.URLField('Target URL', max_length=255)
    
    active_merchant_only = models.BooleanField(
        _('Limit this webhook to active merchant(s) ?'), default=True
    )
    aggregation_delay = models.PositiveIntegerField(
        _('Delay in seconds before triggering the aggregated webhook'),
        default=WEBHOOK_DEFAULT_AGGREGATION_DELAY
    )
    application_id = models.PositiveIntegerField(blank=True, null=True)
    merchant_id = models.PositiveIntegerField(blank=True, null=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    label = models.CharField(max_length=128, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(blank=True, null=True)
    max_attempts = models.PositiveSmallIntegerField(
        _('Maximum Attempts'), 
        default = WEBHOOK_DEFAULT_MAX_ATTEMPTS
    )
    new_attempt_delay = models.PositiveIntegerField(
        _('Delay in seconds before retrying to fire the webhook'),
        default = WEBHOOK_DEFAULT_RETRY_DELAY
    )

    max_trigger_aggregation = models.PositiveSmallIntegerField(
        _('Maximum number of triggers that can be aggregated (1 if no aggregation)'),
        default = WEBHOOK_DEFAULT_MAX_TRIGGER_AGGREGATION
    )

    status = models.CharField(null=True, blank=True, max_length=20, db_index=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    user_id = models.PositiveIntegerField(blank=True, null=True)
    version = models.CharField(
        _('Version of the webhook (different formats)'),
        max_length=10, blank=True, null=True
    )

    def save(self, api_handler=None, iceberg_sync=True, *args, **kwargs):
        """
        if an api_handler is given, update or create the webhook on iceberg
        """
        self.full_clean()
        super(IcebergWebhook, self).save(*args, **kwargs)
        
        if not iceberg_sync:
            return

        if api_handler:
            self.create_or_update_on_iceberg(api_handler)
        else:
            if self.iceberg_id is None:
                logger.warn("No api_handler given as save() params, not created on Iceberg.\
                             Call self.create_or_update_on_iceberg to create it")
            else:
                logger.warn("No api_handler given as save() params, not updated on Iceberg.\
                             Call self.create_or_update_on_iceberg to update it")            



    def create_or_update_on_iceberg(self, api_handler):
        iceberg_webhook = api_handler.Webhook.find(self.iceberg_id) if self.iceberg_id else api_handler.Webhook()
        iceberg_webhook.application = api_handler.Application.find(self.application_id) if self.application_id else None
        iceberg_webhook.merchant = api_handler.Store.find(self.merchant_id) if self.merchant_id else None
        iceberg_webhook.event = self.event
        iceberg_webhook.url = self.url
        iceberg_webhook.active_merchant_only = self.active_merchant_only
        iceberg_webhook.aggregation_delay = self.aggregation_delay
        iceberg_webhook.comment = self.comment
        iceberg_webhook.label = self.label
        iceberg_webhook.max_attempts = self.max_attempts
        iceberg_webhook.new_attempt_delay = self.new_attempt_delay
        iceberg_webhook.max_trigger_aggregation = self.max_trigger_aggregation
        iceberg_webhook.save()
        self.iceberg_id = iceberg_webhook.id
        
        ## calling iceberg_sync() to update the fields of 'self' to the actual values (some fields might be uneditable)
        self.iceberg_sync(api_handler) 



    def iceberg_sync(self, api_handler):
        if self.iceberg_id is None:
            raise Exception("IcebergWebhook instance has no iceberg_id, can't sync")

        iceberg_webhook = api_handler.Webhook.find(self.iceberg_id)
        self.application_id = iceberg_webhook.application.id if iceberg_webhook.application else None
        self.merchant_id = iceberg_webhook.merchant.id if iceberg_webhook.merchant else None
        self.url = iceberg_webhook.url
        self.event = iceberg_webhook.event
        self.status = iceberg_webhook.status
        self.max_attempts = iceberg_webhook.max_attempts
        self.new_attempt_delay = iceberg_webhook.new_attempt_delay
        self.label = iceberg_webhook.label
        self.version = iceberg_webhook.version
        self.max_trigger_aggregation = iceberg_webhook.max_trigger_aggregation
        self.aggregation_delay = iceberg_webhook.aggregation_delay
        self.active_merchant_only = iceberg_webhook.active_merchant_only
        self.created_at = iceberg_webhook.created_at
        self.updated_at = iceberg_webhook.updated_at
        super(IcebergWebhook, self).save() ## just calling the original save()
