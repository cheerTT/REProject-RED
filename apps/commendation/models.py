from django.db import models

# Create your models here.

class Commendation(models.Model):
    assin = models.CharField(max_length=100, blank=False, null=False)
    title = models.CharField(max_length=200, blank=True, null=True)
    sales = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'commendation'
        
class sales_counts(models.Model):
    assin = models.CharField(max_length=100, blank=False, null=False)
    sales_count = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'sale_counts'