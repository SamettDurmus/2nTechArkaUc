from rest_framework import serializers
from .models import Personel, IzinTalebi, GecikmeKaydi

class PersonelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personel
        fields = '__all__'

class IzinTalebiSerializer(serializers.ModelSerializer):
    class Meta:
        model = IzinTalebi
        fields = '__all__'

class GecikmeKaydiSerializer(serializers.ModelSerializer):
    class Meta:
        model = GecikmeKaydi
        fields = '__all__'