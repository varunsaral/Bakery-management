from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(MyUser)
admin.site.register(Inventory)
admin.site.register(InventoryItems)
admin.site.register(Ingredients)
admin.site.register(BakeryItems)
admin.site.register(Cart)
admin.site.register(CartOrders)