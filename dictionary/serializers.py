from rest_framework import serializers
from .models import Definition


class DefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Definition
        fields = ('__all__')

class SearchDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Definition
        fields = ('word', 'slug', 'meaning')
