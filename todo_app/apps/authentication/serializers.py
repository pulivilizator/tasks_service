from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from rest_framework.validators import UniqueValidator

from apps.authentication.models import User


class UserSerializer(serializers.Serializer):
    tg_id = serializers.IntegerField(required=True)
    password = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    username = serializers.CharField(max_length=255, required=False, allow_null=True)
    first_name = serializers.CharField(max_length=255, required=False, allow_null=True)
    last_name = serializers.CharField(max_length=255, required=False, allow_null=True)
    confirmation = serializers.BooleanField(default=False)

    class Meta:
        fields = ('tg_id', 'password', 'username', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        try:
            validate_password(value)
            return value
        except DjangoValidationError as e:
            raise serializers.ValidationError(
                'Пароль должен состоять минимум из 8ми символов и содержать цифры, заглавные и строчные буквы')
