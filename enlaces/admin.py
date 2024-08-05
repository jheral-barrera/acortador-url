from django.contrib import admin
from .models import Enlace

class EnlaceAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'url_original', 
        'url_acortado', 
        'url_personalizado',
        'fecha_creacion', 
        'clics_totales', 
        'fecha_ultimo_clic'
    ]

admin.site.register(Enlace, EnlaceAdmin)
