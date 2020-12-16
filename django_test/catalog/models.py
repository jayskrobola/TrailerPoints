from django.db import models
from UserLogin.models import Sponsor, Driver

# Create your models here.
class Catalog(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name="catalog", null=True)
    name = models.CharField(max_length=200)
    isPrimary = models.BooleanField()

    def __str__(self):
        return self.name

class Category(models.Model):
     catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
     name = models.CharField(max_length=200)

     def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=20)
    productImg = models.CharField(max_length=500)
    productid = models.CharField(max_length=100)
    rating = models.CharField(max_length=50)
    link = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Cart(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)