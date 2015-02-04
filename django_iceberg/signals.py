# -*- coding: utf-8 -*-

from django.dispatch import Signal

product_updated = Signal(providing_args=['webhook_data'])
product_offer_updated = Signal(providing_args=['webhook_data'])

merchant_paused = Signal(providing_args=['webhook_data'])
merchant_stopped = Signal(providing_args=['webhook_data'])
merchant_activated = Signal(providing_args=['webhook_data'])
new_merchant_available = Signal(providing_args=['webhook_data'])

user_profile_updated = Signal(providing_args=['webhook_data'])

cart_status_changed = Signal(providing_args=['webhook_data'])

merchant_order_received = Signal(providing_args=['webhook_data'])
merchant_order_sent = Signal(providing_args=['webhook_data'])
merchant_order_confirmed = Signal(providing_args=['webhook_data'])
merchant_order_authorized = Signal(providing_args=['webhook_data'])
merchant_order_cancelled = Signal(providing_args=['webhook_data'])

order_item_cancelled = Signal(providing_args=['webhook_data'])

user_payment_card_created = Signal(providing_args=['webhook_data'])
user_payment_card_status_changed = Signal(providing_args=['webhook_data'])
payment_status_changed = Signal(providing_args=['webhook_data'])

