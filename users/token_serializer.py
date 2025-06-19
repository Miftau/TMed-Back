from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials", code='authorization')

        data = super().validate(attrs)
        data['user'] = {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "username": user.username,
        }
        return data
