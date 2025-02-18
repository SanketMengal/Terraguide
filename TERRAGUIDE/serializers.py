from rest_framework import serializers
from .models import office,Gardner,Dweller
 
class officeserializer(serializers.ModelSerializer):
    class Meta:
        model=office
        fields='__all__'

class Gardnerserializer(serializers.ModelSerializer):
    class Meta:
        model=Gardner
        fields='__all__'


class Dwellerserializer(serializers.ModelSerializer):
    class Meta:
        model=Dweller
        fields='__all__'
