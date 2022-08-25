from rest_framework.serializers import ModelSerializer
from .models import Vessel


class VesselsSerializer(ModelSerializer):
    class Meta:
        model = Vessel
        fields = '__all__'
