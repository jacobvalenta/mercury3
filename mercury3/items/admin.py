from django.contrib import admin

from .models import Item

class ItemAdmin(admin.ModelAdmin):
	model = Item
	list_display = ('pk', '__str__',  'status', "price_in", "price", "price_out")

admin.site.register(Item, ItemAdmin)