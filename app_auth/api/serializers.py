# 1. Standard library
from django.contrib.auth.models import User

# 2. Third-party
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=[('customer', 'Customer'), ('business', 'Business')], write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeat_password', 'type']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value
    
    def save(self):
        pass