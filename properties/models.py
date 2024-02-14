from django.db import models
# from tenant.models import Agreement

# Create your models here.
class Property(models.Model):
    name = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    region = models.CharField(max_length=30)
    pincode = models.CharField(max_length=10)
    land_mark = models.CharField(max_length=120)
    features = models.TextField(null=True, blank=True)


class Unit(models.Model):
    BHK_CHOICES = (
        ('1BHK', '1BHK'),
        ('2BHK', '2BHK'),
        ('3BHK', '3BHK'),
        ('4BHK', '4BHK'),
    )

    property = models.ForeignKey(Property, on_delete=models.CASCADE, null=True, blank=True)
    rent = models.CharField(max_length=30)
    is_available = models.BooleanField(default=True)
    unit_type = models.CharField(max_length=20, choices=BHK_CHOICES)


