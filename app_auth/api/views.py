# 1. Standard library
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# 2. Third-party
from rest_framework import status, generics
# from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema

# 3. Local application
from .serializers import RegistrationSerializer, UserDetailSerializer, UserBusinessListSerializer, UserCustomerListSerializer
from .permissions import IsProfileOwner
from app_auth.models import UserProfile


@extend_schema(tags=['Authentication'])
class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {'token': token.key,
                    'username': saved_account.username,
                    'email': saved_account.email,
                    'user_id': saved_account.id}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Authentication'])
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            request, username=user_obj.username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Profile'], 
    description="List all user profiles. Admin-only endpoint.",
    responses={200: UserDetailSerializer}
)
class UserDetailView(generics.RetrieveUpdateAPIView):
    http_method_names = ['get', 'patch', 'head', 'options']
    queryset = UserProfile.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsProfileOwner, IsAuthenticated]
    lookup_field = 'user_id'
    # parser_classes = [MultiPartParser, FormParser]


@extend_schema(
    tags=['Profile'],
    description="List all business profiles. Authenticated users only.",
    responses={200: UserBusinessListSerializer}
)
class BusinessUserListView(generics.ListAPIView):
    queryset = UserProfile.objects.filter(type='business')
    serializer_class = UserBusinessListSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=['Profile'],
    description="List all customer profiles. Authenticated users only.",
    responses={200: UserCustomerListSerializer}
)
class CustomerUserListView(generics.ListAPIView):
    queryset = UserProfile.objects.filter(type='customer')
    serializer_class = UserCustomerListSerializer
    permission_classes = [IsAuthenticated]
