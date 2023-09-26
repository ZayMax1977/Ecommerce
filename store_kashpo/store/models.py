# from django.contrib.auth.models import User
# from django.db import models
#
#

# class Customer(models.Model):
#     user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200, null=True)
#     email = models.CharField(max_length=200)
#
#     def __str__(self):
#         return self.name
#
# class Color(models.Model):
#     name = models.CharField(max_length=200, null=True, blank=True)
#
#     def __str__(self):
#         return self.name
#
#
# class Product(models.Model):
#     name = models.CharField(max_length=200)
#     price = models.FloatField()
#     is_active = models.BooleanField(default=False)
#     # image = models.ImageField(null=True, blank=True)
#     color = models.ForeignKey(Color, on_delete=models.PROTECT)
#
#     def __str__(self):
#         return self.name
#
#
#
# class Order(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
#     date_ordered = models.DateTimeField(auto_now_add=True)
#     complete = models.BooleanField(default=False)
#     transaction_id = models.CharField(max_length=100, null=True)
#
#     def __str__(self):
#         return str(self.id)