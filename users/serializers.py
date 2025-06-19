from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
        )
        return user


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = '__all__'
        read_only_fields = ['user']


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = '__all__'
        read_only_fields = ['user']

class DoctorDirectorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = DoctorProfile
        fields = ['id', 'name', 'email', 'specialty', 'bio', 'contact_number', 'location']

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['id', 'day_of_week', 'start_time', 'end_time']
