import base64
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.backends import default_backend
from django.contrib.auth import get_user_model
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from django.conf import settings
from cryptography.exceptions import InvalidSignature


class RSAPublicKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        public_key_base64 = request.headers.get('X-Public-Key')

        if not public_key_base64:
            return None
        tg_id = request.headers.get('X-Tg-Id')
        user = get_user_model().objects.get(tg_id=tg_id)
        try:
            public_key_pem = base64.b64decode(public_key_base64)
            public_key = load_pem_public_key(public_key_pem, backend=default_backend())
        except (ValueError, TypeError):
            raise AuthenticationFailed('Invalid public key format')
        try:
            private_key_pem = settings.PRIVATE_SERVICE_KEY.read_text()
            private_key = load_pem_private_key(private_key_pem.encode('utf-8'), password=None,
                                               backend=default_backend())
        except ValueError:
            raise AuthenticationFailed('Invalid private key format')

        if self.is_matching_key_pair(public_key, private_key):
            return user, None

    def is_matching_key_pair(self, public_key, private_key):
        test_message = b"test"
        try:
            signature = private_key.sign(
                test_message,
                padding.PKCS1v15(),
                hashes.SHA256()
            )

            public_key.verify(
                signature,
                test_message,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False


class RSAPublicKeyAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'apps.authentication.authentications.RSAPublicKeyAuthentication'
    name = 'RSAKeyAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-Public-Key',
            'description': 'Public Key and tg id authentication for services'
        }