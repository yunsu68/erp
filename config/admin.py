from django.contrib import admin
from .models import Product, Inbound, Inventory

# Register your models here.

admin.site.register(Product)
admin.site.register(Inbound)
admin.site.register(Inventory)