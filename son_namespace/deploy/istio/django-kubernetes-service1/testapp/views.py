from django.contrib.auth.models import User
from testapp.serializers import UserSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]