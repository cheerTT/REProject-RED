from django.db import models

# Create your models here.
class Users_Recommendations(models.Model):
    user_id = models.CharField(max_length=100, blank=False, null=False)
    product_id_1 = models.TextField(max_length=100, blank=True, null=True)
    product_id_2 = models.TextField(max_length=100, blank=True, null=True)
    product_id_3 = models.TextField(blank=True, null=True)
    product_id_4 = models.TextField(max_length=1000, blank=True, null=True)
    product_id_5 = models.TextField(max_length=100, blank=True, null=True)
    class Meta:
        db_table = "users_recommendations"
