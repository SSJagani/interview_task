from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from random import randint
from datetime import datetime, timedelta
import pytz

# Below lib use for email send
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.template.loader import render_to_string

# Import all Model
from .models import User,OTPVerification

# Create your views here.
def login(request):
	if request.method == 'POST':
		mobile_number = request.POST['mobile_number']
		qry_check_user = User.objects.filter(mobile_number=mobile_number)
		if not qry_check_user.exists():
			messages.error(request, 'Mobile number not registered yet!')
			return redirect('/')
		else:
			now = pytz.utc.localize(datetime.now())
			if qry_check_user[0].block_time is None or qry_check_user[0].block_time < now:
				otp = randint(100000, 999999)
				qry_qtp_verification = OTPVerification(mobile_number=mobile_number, otp=otp)
				qry_qtp_verification.save()
				request.session['mobile_number'] = mobile_number
				return redirect('/login_otp')
			else:
				messages.error(request, 'You are multiple time wrong opt! wait 5 minutes for new opt')
				return redirect('/')
	else:
		return render(request, 'authentication/login.html')


def login_otp(request):
	if request.method == 'POST':
		mobile_number = request.session['mobile_number']
		otp = request.POST['otp']

		now = datetime.now()
		now_plus_5 = now + timedelta(minutes = 5)

		qry_otp_verification = OTPVerification.objects.filter(
				mobile_number=mobile_number,
				otp=otp
			).last()

		if qry_otp_verification:
			qry_otp_verification.delete()
			qry_user = User.objects.get(mobile_number=mobile_number)
			request.session['user_id'] = qry_user.user_id
			del request.session['mobile_number']
			return redirect('/dashboard')
		else:
			qry_check_user = User.objects.get(mobile_number=mobile_number)
			if qry_check_user.login_try == 2:
				messages.error(request, "Invalid OTP And user login should be blocked for 5 minutes!")
				qry_check_user.login_try = 0
				qry_check_user.block_time = now_plus_5
				qry_check_user.save()
				return redirect('/')
			else:
				qry_check_user.login_try+=1
				messages.error(request, "Invalid OTP!")
				qry_check_user.save()
				return redirect('/login_otp')

	else:	
		mobile_number = request.session['mobile_number']

		qry_otp_verification = OTPVerification.objects.filter(
			mobile_number=mobile_number).last()
		otp = qry_otp_verification.otp
		context = {
			'OTP': str(otp),
		}

		return render(request, 'authentication/login_otp.html', context=context)


def resend_otp(request):
	if request.method == 'POST':
		mobile_number = request.POST['mobile_number']
		qry_check_user = User.objects.filter(mobile_number=mobile_number)
		if not qry_check_user.exists():
			messages.error(request, 'Mobile number not registered yet!')
			return redirect('/resend_otp')
		else:
			now = pytz.utc.localize(datetime.now())
			if qry_check_user[0].block_time is None or qry_check_user[0].block_time < now:
				otp = randint(100000, 999999)
				qry_qtp_verification = OTPVerification(mobile_number=mobile_number, otp=otp)
				qry_qtp_verification.save()
				request.session['mobile_number'] = mobile_number
				return redirect('/login_otp')
			else:
				messages.error(request, 'You are multiple time wrong opt! wait 5 minutes for new opt')
				return redirect('/')
	else:
		return render(request, 'authentication/resend_otp.html')


def registration(request):
	if request.method == 'POST':
		user_name = request.POST['user_name']
		email_address = request.POST['email_address']
		mobile_number = request.POST['mobile_number']
		password = request.POST['password']
		confirm_password = request.POST['confirm_password']
		if password != confirm_password:
			messages.error(request,'Password mismatch with Confirm Password!')
			return redirect('/registration')
		else:
			qry_create_user = User(full_name=user_name, email_address=email_address, mobile_number=mobile_number)
			qry_create_user.set_password(password)
			qry_create_user.save()
			subject = "Welcome to Our Company."
			email_template_name = "authentication/welcome_mail.html"
			context = {
				"User": qry_create_user,
			}
			body_message = render_to_string(email_template_name, context)
			print(body_message)
			try:
				send_mail(subject, body_message, settings.EMAIL_HOST_USER, [qry_create_user.email_address], fail_silently=False)
			except BadHeaderError:
				messages.error(request, 'Some thing want to wrong!')
				return redirect('/registration')
			return redirect('/')

		# client_ip = request.META['REMOTE_ADDR']

	else:
		return render(request, 'authentication/registration.html')


def check_user_email(request):
	if request.method == 'POST':
		email = request.POST['email']
		qry_check_email = User.objects.filter(email_address=email)
		if qry_check_email.exists():
			context = {
				'status': True,
				'message': 'This Email Already exists.'
			}	
		else:
			context = {
				'status': False,
				'message': ''
			}
		return JsonResponse(context)


def dashboard(request):
	print(request.session['user_id'])
	return HttpResponse("hellooo")