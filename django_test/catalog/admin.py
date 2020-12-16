from django.contrib import admin
from .models import Catalog, Category, Product

# Register your models here.
admin.site.register(Catalog)
admin.site.register(Category)
admin.site.register(Product)