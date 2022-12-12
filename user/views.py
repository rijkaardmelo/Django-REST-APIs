import jwt
import json

from django.http import HttpResponse
from rest_framework import viewsets, status, exceptions
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework.decorators import action

from user.models import UserModel
from user.serializers import UserSerializer


class UserView(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class LoginView(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        if not request.data:
            return Response({'Error': "Please provide username/password"}, status="400")

        username = request.data[0].get('username')
        password = request.data[0].get('password')

        try:
            user = UserModel.objects.get(username=username, password=password)
        except:
            return Response({'Error': "Invalid username/password"}, status="400")

        if user:
            payload = {
                'id': user.id,
                'username': user.username,
            }
            jwttoken = jwt.encode(payload, "SECRET_KEY", algorithm="HS256")

            return HttpResponse(
                json.dumps(jwttoken),
                status=200,
                content_type="application/json"
            )
        else:
            return Response(
                json.dumps({'Error': "Invalid credentials"}),
                status=400,
                content_type="application/json"
            )

