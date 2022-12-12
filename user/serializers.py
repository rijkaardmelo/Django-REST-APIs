from rest_framework import serializers
from user.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
