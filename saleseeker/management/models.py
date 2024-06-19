from django.db import models

class ShopInfoUnique4(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    post = models.TextField()
    shop_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    competitor = models.TextField(null=True, blank=True)
    saturday = models.CharField(max_length=255, null=True, blank=True)
    sunday = models.CharField(max_length=255, null=True, blank=True)
    monday = models.CharField(max_length=255, null=True, blank=True)
    tuesday = models.CharField(max_length=255, null=True, blank=True)
    wednesday = models.CharField(max_length=255, null=True, blank=True)
    thursday = models.CharField(max_length=255, null=True, blank=True)
    friday = models.CharField(max_length=255, null=True, blank=True)
    shop_status = models.CharField(max_length=10, null=True, blank=True)
    menu = models.CharField(max_length=100)
    note = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Shopinfo_unique_4'




class Postcode(models.Model):
    City = models.CharField(max_length=50, null=True, blank=True)
    Post_code = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'Postcode' 