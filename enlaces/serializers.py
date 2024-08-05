from rest_framework import serializers
from .models import Enlace

class EnlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enlace
        fields = '__all__'