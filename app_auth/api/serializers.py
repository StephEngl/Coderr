# 1. Standard library
from django.contrib.auth.models import User

# 2. Third-party
from rest_framework import serializers

from app_auth.models import UserProfile


class UserInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for user information.

    Attributes:
        id (IntegerField): The user's ID.
        username (CharField): The user's username.
        email (EmailField): The user's email address.
    """
    class Meta:
        model = User
        fields = ['username', 'email']


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Attributes:
        repeat_password (CharField): Field for confirming password.
        type (ChoiceField): Field to select user type (customer or business).
    """
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(
        choices=UserProfile.USER_TYPE_CHOICES, write_only=True)

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

        user_type = self.validated_data.get('type', '')
        UserProfile.objects.create(user=account, type=user_type)
        return account


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed user information.
    """
    user = serializers.CharField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name',
                'file', 'location', 'tel', 'description',
                'working_hours', 'type', 'email', 'created_at']
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        email = user_data.get('email')
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')

        if email:
            instance.user.email = email
        if first_name:
            instance.user.first_name = first_name
        if last_name:
            instance.user.last_name = last_name
        instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserBusinessListSerializer(UserDetailSerializer):
    """
    Serializer for listing business users.
    """
    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name',
                'file', 'location', 'tel', 'description', 'working_hours', 'type']
        read_only_fields = fields


class UserCustomerListSerializer(UserDetailSerializer):
    """
    Serializer for listing customer users.
    """
    uploaded_at = serializers.DateTimeField(
        source='file_uploaded_at', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name',
                'file', 'uploaded_at', 'type']
        read_only_fields = fields
