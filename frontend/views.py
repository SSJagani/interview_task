from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

# Below lib use for email send
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.template.loader import render_to_string

# Import all Model
from .models import User

# Create your views here.
def login(request):
	print("hellooooo")
	return HttpResponse("LOGIN")



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
			email_template_name = "frontend/welcome_mail.html"
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
		return render(request, 'frontend/registration.html')



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