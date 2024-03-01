# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, Vendor

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    print("signal instance",instance)
    if instance.status == 'Completed':
        vendor = instance.vendor
        vendor.update_performance_metrics()
