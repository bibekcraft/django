from django.contrib import admin
from .models import Category, Place, Details,Blog

# Register your models here.
admin.site.register(Category)
admin.site.register(Place)
admin.site.register(Details)
admin.site.register(Blog)