# 1. Standard library
from django.contrib.auth.models import User

# 2. Third-party
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Attributes:
        repeat_password (CharField): Field for confirming password.
        type (ChoiceField): Field to select user type (customer or business).
    """
    repeat_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=[('customer', 'Customer'), ('business', 'Business')], write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        """
        Validate that the email is unique.

        Args:
            value (str): The email address to validate.

        Returns:
            str: The validated email address.

        Raises:
            serializers.ValidationError: If the email is already in use.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value
    
    def save(self):
        """
        Save the user instance after validating passwords match.

        Returns:
            User: The created user instance.

        Raises:
            serializers.ValidationError: If the passwords do not match.
        """
        pw = self.validated_data['password']
        rpw = self.validated_data['repeated_password']
        if pw != rpw:
            raise serializers.ValidationError("Passwords do not match.")
        account = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        account.set_password(pw)
        account.save()
        return account