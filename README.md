# interview_task
Python, Django, Git,


Here Follw below stpe to run this project:
1. Create Virtualenv 
	virtualenv venv

2. active Virtualenv
	source venv/bin/activate

3. install rerequirement.txt using:-
	pip install -r requirements.txt

4. configure mysql database in settings.Py file
	line_number = 81 give database name ('NAME': 'interview')
	line_number = 82 give user name ('USER': 'root')
	line_number = 83 give password for login ('PASSWORD': '')

5. configure Email in settings.Py file
	line_number = 144 give database name (EMAIL_HOST_USER = 'examples@gmail.com')
	line_number = 145 give database name (EMAIL_HOST_PASSWORD = 'xxxxxxxxxxx')

6. now makemigration for database using:-
	python manage.py makemigration

7. now migrate for database using:-
	python manage.py migrate

8. Run Project using below command:
	python manage.py runserver
 