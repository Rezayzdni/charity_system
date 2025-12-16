from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


User = get_user_model()

class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            data={'message': f'Bye {request.user.username}!'},
            status=status.HTTP_204_NO_CONTENT
        )


class UserRegistration(generics.CreateAPIView):
        queryset = User.objects.all()
        serializer_class = UserSerializer
    



class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        # Add is_benefactor and is_charity logic
        is_benefactor = hasattr(user, 'benefactor')
        is_charity = hasattr(user, 'charity')

        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'is_benefactor': is_benefactor,
            'is_charity': is_charity,
        })