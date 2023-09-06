# It's a makefile!

# export DJANGOPORT := 8001
# export DEBUG := True

PSQL = psql
CMD = python3 manage.py
APP = models 

# create alumnodb super user
create_super_user:
	$(CMD) shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('alumnodb', 'admin@myproject.com', 'alumnodb')"


runserver:
	$(CMD) runserver $(DJANGOPORT)

update_models:
	$(CMD) makemigrations 
	$(CMD) migrate
	

help:
	@echo "open the makefile and see the targets"
