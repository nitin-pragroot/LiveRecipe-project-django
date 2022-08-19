from django.contrib import admin
from .models import Recipe,Reviews,Category,UserDetail
# Register your models here.
admin.site.register(Recipe)
admin.site.register(Reviews)
admin.site.register(Category)
admin.site.register(UserDetail)