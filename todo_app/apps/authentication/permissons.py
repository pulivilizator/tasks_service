import base64
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.backends import default_backend
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from django.conf import settings
from cryptography.exceptions import InvalidSignature


class RSAPublicKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Декодируем публичный ключ из Base64
        public_key_base64 = request.headers.get('X-Public-Key')

        if not public_key_base64:
            raise AuthenticationFailed('Public key is missing')

        try:
            # Декодируем Base64-ключ и загружаем его в PEM-формате
            public_key_pem = base64.b64decode(public_key_base64)
            public_key = load_pem_public_key(public_key_pem, backend=default_backend())
        except (ValueError, TypeError):
            raise AuthenticationFailed('Invalid public key format')

        # Загрузка приватного ключа
        try:
            private_key_pem = settings.PRIVATE_SERVICE_KEY.read_text()
            private_key = load_pem_private_key(private_key_pem.encode('utf-8'), password=None,
                                               backend=default_backend())
        except ValueError:
            raise AuthenticationFailed('Invalid private key format')

        # Сравниваем ключи
        if self.is_matching_key_pair(public_key, private_key):
            return get_user_model().objects.all()[0], None  # Здесь нужно вернуть пользователя, если аутентификация успешна)

    def is_matching_key_pair(self, public_key, private_key):
        test_message = b"test"  # Тестовое сообщение
        try:
            # Подписываем тестовое сообщение приватным ключом
            signature = private_key.sign(
                test_message,
                padding.PKCS1v15(),
                hashes.SHA256()
            )

            # Проверяем подпись публичным ключом
            public_key.verify(
                signature,
                test_message,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True  # Если подпись успешно проверена, ключи совпадают
        except InvalidSignature:
            return False  # Подпись не совпадает, ключи разные
