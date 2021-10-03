from django.urls import path
from . import views



urlpatterns = [
	path('', views.login, name='login'),
	path('login_otp', views.login_otp, name='login_otp'),
	path('resend_otp', views.resend_otp, name='resend_otp'),

	path('registration', views.registration, name='registration'),
	path('check_user_email', views.check_user_email, name='check_user_email'),

	path('dashboard', views.dashboard,  name='dashboard'),
	
]