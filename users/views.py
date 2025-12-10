from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserCreateSerializer, UserAuthSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random
from .models import ConfirmCode


def generate_code():
    return str(random.randint(100000, 999999))


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = User.objects.create_user(
        username=username,
        password=password,
        is_active=False
    )

    code = generate_code()

    ConfirmCode.objects.create(
        user=user,
        code=code
    )

    return Response(
        data={'user_id': user.id,
              'code': code},
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)

    if not user.is_active:
        return Response(status=status.HTTP_403_FORBIDDEN)

    token, _ = Token.objects.get_or_create(user=user)
    return Response(data={'key': token.key})


@api_view(['POST'])
def confirm_api_view(request):
    username = request.data.get('username')
    code = request.data.get('code')

    if not username or not code:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response('User not found!')

    try:
        confirm = ConfirmCode.objects.get(user=user)
    except ConfirmCode.DoesNotExist:
        return Response('Code not found!')

    if confirm.code != code:
        return Response('Invalid code!')

    user.is_active = True
    user.save()

    return Response('User confirmed!')
