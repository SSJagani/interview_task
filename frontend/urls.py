from django.urls import path
from . import views



urlpatterns = [
	path('', views.login, name='login'),
	path('registration', views.registration, name='registration'),
	path('check_user_email', views.check_user_email, name='check_user_email'),
	
]