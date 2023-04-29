from django.contrib import admin
from .models import *

# Register your models here.
class SoruAdmin(admin.ModelAdmin):
    list_display=('baslik', 'kullanici')
    search_fields=('baslik', 'icerik')
    
admin.site.register(Soru, SoruAdmin)
admin.site.register(Yorum)

