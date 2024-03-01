from django.db import models
import uuid
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import F, Avg, Count, ExpressionWrapper, fields
from datetime import timedelta
# Create your models here.


# This model stores essential information about each vendor and their performance metrics.
class Vendor(models.Model):
    vendor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    quality_rating_avg = models.FloatField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5)])
    average_response_time = models.FloatField(default=0,validators=[MinValueValidator(0)])
    fulfillment_rate = models.FloatField(default=0,validators=[MinValueValidator(0), MaxValueValidator(100)])


    def update_performance_metrics(self):
        completed_pos = PurchaseOrder.objects.filter(vendor=self, status='Completed')
        total_completed_pos = completed_pos.count()

        on_time_delivery_count = completed_pos.filter(delivery_date__lte=datetime.now()).count()
        self.on_time_delivery_rate = (on_time_delivery_count / total_completed_pos) * 100 if total_completed_pos > 0 else 0

        quality_rating_avg = completed_pos.filter(quality_rating__isnull=False).aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0
        self.quality_rating_avg = quality_rating_avg

        # avg_response_time = completed_pos.filter(acknowledgment_date__isnull=False).aggregate(
        #     avg_response_time=Avg(ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=fields.DurationField()))
        # )['avg_response_time'] or timedelta(seconds=0)
        avg_response_time_seconds = completed_pos.filter(acknowledgment_date__isnull=False).aggregate(avg_response_time=Avg(ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=fields.DurationField())))['avg_response_time'] or timedelta(seconds=0)

        # Convert the average response time to seconds as a float
        avg_response_time = avg_response_time_seconds.total_seconds() if avg_response_time_seconds else 0

        self.average_response_time = avg_response_time

        fulfilled_pos = completed_pos.filter(issue_date__lte=F('acknowledgment_date'))
        fulfillment_rate = (fulfilled_pos.count() / total_completed_pos) * 100 if total_completed_pos > 0 else 0
        self.fulfillment_rate = fulfillment_rate

        self.save()
    
    def __str__(self):
        return self.name
    
    def calculate_on_time_delivery_rate(self):
        completed_pos = PurchaseOrder.objects.filter(vendor=self, status='Completed')
        total_completed_pos = completed_pos.count()
        on_time_delivery_count = completed_pos.filter(delivery_date__lte=datetime.now()).count()
        return (on_time_delivery_count / total_completed_pos) * 100 if total_completed_pos > 0 else 0

    def calculate_quality_rating_avg(self):
        completed_pos = PurchaseOrder.objects.filter(vendor=self, status='Completed', quality_rating__isnull=False)
        return completed_pos.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0

    def calculate_fulfillment_rate(self):
        fulfilled_pos = PurchaseOrder.objects.filter(vendor=self, status='Completed', issue_date__lte=F('acknowledgment_date'))
        return (fulfilled_pos.count() / PurchaseOrder.objects.filter(vendor=self).count()) * 100 if PurchaseOrder.objects.filter(vendor=self).count() > 0 else 0

STATUS = (
    ("Pending", "Pending"),
    ("Completed", "Completed"),
    ("Canceled", "Canceled"),
)

class PurchaseOrder(models.Model):
    po_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=50, choices=STATUS)
    quality_rating = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO {self.po_number} - {self.vendor.name}"

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    quality_rating_avg = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    average_response_time = models.FloatField(validators=[MinValueValidator(0)])
    fulfillment_rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"

