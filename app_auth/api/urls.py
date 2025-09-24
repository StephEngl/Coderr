from django.urls import path
from .views import RegistrationView, LoginView, UserDetailView, BusinessUserListView, CustomerUserListView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('profile/business/', BusinessUserListView.as_view(), name='business-user-list'),
    path('profile/customer/', CustomerUserListView.as_view(), name='customer-user-list'),
]
