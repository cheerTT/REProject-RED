# @Time    : 2019/3/6 20:00
# @Author  : Virus
# @Remark  :




from django.db import models

# Create your models here.
class Users_Recommendations(models.Model):
    """
    与User_Recommendations表中的字段相对应，
    """
    user_id = models.CharField(max_length=100, blank=False, null=False)
    product_id_1 = models.TextField(max_length=100, blank=True, null=True)
    product_id_2 = models.TextField(max_length=100, blank=True, null=True)
    product_id_3 = models.TextField(blank=True, null=True)
    product_id_4 = models.TextField(max_length=1000, blank=True, null=True)
    product_id_5 = models.TextField(max_length=100, blank=True, null=True)
    class Meta:
        """
        表名
        """
        db_table = "users_recommendations"

class Users_AllRecommendations(models.Model):
    """
    与User_Recommendations表中的字段相对应，
    """
    user_id = models.CharField(max_length=100, blank=False, null=False)
    products_id = models.TextField(blank = False, null = False)
    class Meta:
        """
        表名
        """
        db_table = "users_allrecommendations"
