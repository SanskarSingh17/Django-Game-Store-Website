from django.contrib import admin
from myapp.models import Games,Cart

# Register your models here.
class GamesAdmin(admin.ModelAdmin):
    list_display=['id','name','type','price']

class CartAdmin(admin.ModelAdmin):
    list_display=['id','gid','uid','quantity']


admin.site.register(Games, GamesAdmin)
admin.site.register(Cart,CartAdmin)
