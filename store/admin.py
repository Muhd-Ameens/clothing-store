from django.contrib import admin

from store.models import Category,Product,Size


# Register your models here.

admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Product)

