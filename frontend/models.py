from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser 

# Create your models here.

class UserManager(BaseUserManager):
	def create_user(self, email_address, password=None):
		if not email_address:
			raise ValueError('Users must have an email address')

		user = self.model(
			email_address=self.normalize_email(email_address),
		)
		user.set_password(password)
		user.save(using=self._db)
		return user
	def create_superuser(self, email_address, password):
		user = self.create_user(
			email_address,
			password=password,
		)
		user.is_staff = True
		user.is_admin = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser):
	user_id = models.AutoField(primary_key=True)
	full_name = models.CharField(max_length=30)
	email_address = models.EmailField(max_length=255, unique=True)
	mobile_number = models.CharField(max_length=20)
	password = models.CharField(max_length=100)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	
	login_try = models.IntegerField(default=0)
	block_time = models.DateTimeField(null=True)

	create_at = models.DateField(auto_now_add=True)
	update_at = models.DateField(auto_now=True)

	USERNAME_FIELD = 'email_address'

	objects = UserManager()

	class Meta:
		db_table = 'user'


class OTPVerification(models.Model):
    mobile_number = models.CharField(max_length=20)
    otp = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'otp_verification'

