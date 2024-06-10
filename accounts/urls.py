from django.urls import path
from . import views
from .api_views import  LoginView, LogoutView, ProfileView


app_name='accounts'

urlpatterns = [
    path('signup',views.signup , name='signup'),
    path('profile',views.profile , name='profile'),
    path('profile/edit',views.profile_edit , name='profile_edit'),
    path('api/login/', LoginView.as_view(), name='login-api'),
    path('api/logout/', LogoutView.as_view(), name='logout-api'),
    path('api/profile/', ProfileView.as_view(), name='profile-api'),
]