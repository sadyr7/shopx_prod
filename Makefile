.PHONY: install migrate createsuperuser runserver


install:
	pip install -r requirements.txt
 
migrate:
	python manage.py makemigrations app_chat
	python manage.py makemigrations app_support_service
	python manage.py makemigrations Category
	python manage.py makemigrations notification
	python manage.py makemigrations product
	python manage.py makemigrations app_user
	python manage.py makemigrations app_userbase
	python manage.py makemigrations app_userseller
	python manage.py makemigrations app_baner
	python manage.py makemigrations app_vip
	python manage.py migrate
 
createsuperuser:
	python manage.py createsuperuser
 
runserver:
	python manage.py runserver --noasg