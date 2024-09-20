from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from rest_framework.validators import UniqueValidator

from apps.authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    tg_id = serializers.IntegerField()
    password = serializers.CharField()

    class Meta:
        fields = ('tg_id', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_tg_id(self, value):
        try:
            get_user_model().objects.get(tg_id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist')

    def validate_password(self, value):
        try:
            validate_password(value)
            return value
        except DjangoValidationError as e:
            raise serializers.ValidationError(
                'Пароль должен состоять минимум из 8ми символов и содержать цифры, заглавные и строчные буквы')
