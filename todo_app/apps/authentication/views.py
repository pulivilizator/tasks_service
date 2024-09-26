from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
# from rest_framework.authentication import

from .publisher import registration_publish
from .serializers import UserSerializer
from .schema import schema


@schema.registration_extend_schema
class HttpRegistrationAPIView(APIView):
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            tg_id = serializer.validated_data.get('tg_id')
            has_user = get_user_model().objects.filter(tg_id=tg_id).exists()
            password = serializer.validated_data.get('password')
            if has_user and password:
                confirmation = serializer.validated_data.pop('confirmation', None)
                if confirmation:
                    user = get_user_model().objects.get(tg_id=tg_id)
                    user.password = password
                    user.save()
                    return Response({
                        'token': str(RefreshToken.for_user(user)),
                        'user': UserSerializer(user).data
                    }, status=status.HTTP_201_CREATED)
                hashed_password = make_password(password)
                registration_publish(user_id=tg_id, password_hash=hashed_password)
                return Response({
                    'message': 'Confirm registration in telegram'
                }, status=status.HTTP_201_CREATED)
            elif has_user and password is None:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                get_user_model().objects.create(**serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@schema.login_extend_schema
class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        tg_id = data.get('tg_id', None)
        password = data.get('password', None)
        if not tg_id or not password:
            return Response({'error': 'Отсутствует логин или пароль'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(tg_id=tg_id, password=password)
        if user is None:
            return Response({'error': 'Неверные данные'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'tg_id': user.tg_id,
        })
        user.last_login = timezone.now()

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_200_OK)


@schema.logout_extend_schema
class LogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Необходим refresh token'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({'error': 'Неверный refresh token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=['Authentication'],
    summary='Замена устаревшего токена авторизации',
    description='Принимает токен refresh и возвращает токен новую пару токенов'
)
class TokenRefreshSchemaView(TokenRefreshView):
    pass

