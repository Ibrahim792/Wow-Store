from django.contrib import admin
from wowapp.models import Product
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','description','price','is_active']
    list_filter=['is_active']
admin.site.register(Product,ProductAdmin)