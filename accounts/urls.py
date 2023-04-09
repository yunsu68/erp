from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.signup, name='sign-up'),
    path('user-login/', views.user_login, name='user-login'),
    path('user-logout/', views.user_logout,name='user-logout'),
]