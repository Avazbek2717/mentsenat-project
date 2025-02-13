
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User

class CustomPermession(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.email
    