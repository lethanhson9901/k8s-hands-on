from django.urls import path
from testapp.views import *

urlpatterns = [
    path('users/', UserList.as_view()),
]