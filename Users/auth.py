# from rest_framework.authtoken.models import Token
# from django.contrib.auth.backends import BaseBackend


# class TokenBackend(BaseBackend):
#     def authenticate(self, request, token=None):
#         try:
#             user = Token.objects.get(key=token).user
#             return user
#         except Token.DoesNotExist:
#             return None