from django.contrib import admin

from .models import *

admin.site.register(CustomUser)
admin.site.register(Item)
admin.site.register(Suppliers)
admin.site.register(Rental)
