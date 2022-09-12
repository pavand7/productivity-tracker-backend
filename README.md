# productivity-tracker-backend setup

## DOWNLOADING THE PROJECT
- Make sure git and python are installed in your system.
- Clone the backend github repository by running the following command in the terminal window:
 git clone https://github.com/pavand7/productivity-tracker-backend.git


## INSTALLING THE PACKAGES
Install the following packages in your system by running ‘pip install <package_name>’ in the terminal..
- python-dateutil
- google-api-python-client
- google-auth-oauthlib

## PRE-REQUISITES
To be able to run the backend code, following prerequisites need to be met.
- Install postgresql and pgadmin4.
- While installing postgresql, create a superuser and save the credentials (username and password).
- In pgadmin4, create a server and a database in it. Give a name to the database and authorize it with superuser credentials. Select the correct port (sometimes only <1000 works).
- Use the same credentials in the DATABASES variable in the root/backend/settings.py file to connect the server to the database created. (root is the root directory of the codebase)
The DATABASES variable should look like the following:

```
{

  'default':
  
  {
       
       'ENGINE': 'django.db.backends.postgresql',
       
       'NAME': <name of db created>,
       
       'USER': <superuser name>,
       
       'PASSWORD': <superuser password>,
       
       'HOST': 'localhost'
   
   }
   
}
```
	
- In the root/userapi/migrations folder, delete all migration files whose name starts with 0001, 0002, etc.
- In the root directory, run ‘python manage.py makemigrations’ and ‘python manage.py migrate’. These will migrate the changes in table models to the database.
- Change ALLOWED HOSTS variable in ‘root/backend/settings.py’ file for frontend to be able to call backend apis. It should look something like this: (10.0.2.2 is the host for the emulator in android studio)

**ALLOWED_HOSTS = ['10.0.2.2', 'localhost']**

## RUNNING THE PROJECT

- In the root directory, run ‘python manage.py runserver’ to start the server.
- If there are errors related to some missing packages, install them using ‘pip install <package_name>’ in the terminal.
- If you wish to have some dummy data to start with, go to ‘http://localhost:<port_number>/createTables/’ in your browser to populate all the tables in the database. Else, you are good to go.

