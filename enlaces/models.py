from django.db import models
from datetime import timezone, datetime

import re

class Enlace(models.Model):
    url_original = models.URLField()
    url_acortado =  models.CharField(max_length=8, unique=True, blank=True)
    url_personalizado = models.CharField(max_length=100, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    clics_totales = models.PositiveIntegerField(default=0)
    fecha_ultimo_clic = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.url_original
    
    def registrar_clic(self):
        self.clics_totales += 1
        self.fecha_ultimo_clic = datetime.now()
        self.save()

    @classmethod
    def validar_url_existente(cls, url_a_validar, url):
        if url_a_validar == 'url_original':
            if cls.objects.filter(url_original=url).exists():
                return True
            return False
        
        elif url_a_validar == 'url_personalizado':
            if cls.objects.filter(url_personalizado=url).exists():
                return True
        return False    
    
    @classmethod
    def validar_url_personalizado(cls, url_personalizado):
        validar_url = bool(re.match("^[A-Za-z0-9_-]*$", url_personalizado))
        if validar_url:
            return True
        return False
        

