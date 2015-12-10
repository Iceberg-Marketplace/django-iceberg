# -*- coding: utf-8 -*-

from django.dispatch import Signal

""" Signals triggered by webhook endpoint with raw webhook_data """

webhook_received = Signal(providing_args=["webhook_data"])  # generic signal


product_updated_webhook = Signal(providing_args=["webhook_data"])
product_offer_updated_webhook = Signal(providing_args=["webhook_data"])

merchant_paused_webhook = Signal(providing_args=["webhook_data"])
merchant_stopped_webhook = Signal(providing_args=["webhook_data"])
merchant_activated_webhook = Signal(providing_args=["webhook_data"])
new_merchant_available_webhook = Signal(providing_args=["webhook_data"])

user_profile_updated_webhook = Signal(providing_args=["webhook_data"])

cart_status_changed_webhook = Signal(providing_args=["webhook_data"])

merchant_order_authorized_webhook = Signal(providing_args=["webhook_data"])
merchant_order_confirmed_webhook = Signal(providing_args=["webhook_data"])
merchant_order_sent_webhook = Signal(providing_args=["webhook_data"])
merchant_order_received_webhook = Signal(providing_args=["webhook_data"])
merchant_order_cancelled_webhook = Signal(providing_args=["webhook_data"])

order_item_cancelled_webhook = Signal(providing_args=["webhook_data"])

user_payment_card_created_webhook = Signal(providing_args=["webhook_data"])
user_payment_card_status_changed_webhook = Signal(providing_args=["webhook_data"])
payment_status_changed_webhook = Signal(providing_args=["webhook_data"])


""" Signals triggered after webhook processing, where sender is the Iceberg object (to connect)"""

product_updated = Signal()
product_offer_updated = Signal()

merchant_paused = Signal()
merchant_stopped = Signal()
merchant_activated = Signal()
new_merchant_available = Signal()

user_profile_updated = Signal()

cart_status_changed = Signal()

merchant_order_authorized = Signal()
merchant_order_confirmed = Signal()
merchant_order_sent = Signal()
merchant_order_received = Signal()
merchant_order_cancelled = Signal()

order_item_cancelled = Signal()

user_payment_card_created = Signal()
user_payment_card_status_changed = Signal()
payment_status_changed = Signal()


