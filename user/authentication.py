import jwt, json
from django.http import HttpResponse
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from user.models import UserModel


class TokenAuthentication(BaseAuthentication):

    model = None

    def get_model(self):
        return UserModel

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1]
            if token == "null":
                msg = 'Null token not allowed'
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        payload = jwt.decode(token, "SECRET_KEY")
        username = payload['username']
        id = payload['id']
        msg = {'Error': "Token mismatch", 'status': "401"}
        try:

            user = UserModel.objects.get(
                id=id,
                username=username,
                is_active=True
            )

            if not user.token['token'] == token:
                raise exceptions.AuthenticationFailed(msg)

        except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:
            return HttpResponse({'Error': "Token is invalid"}, status="403")
        except UserModel.DoesNotExist:
            return HttpResponse({'Error': "Internal server error"}, status="500")

        return (user, token)

    def authenticate_header(self, request):
        return 'Token'