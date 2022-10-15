from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import UserSignupView


app_name = 'authentication'


urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(
        template_name='authentication/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]