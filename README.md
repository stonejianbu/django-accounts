## django-accounts 

### Introduction

Just a simple application for managing user logins and registrations, 
which provides front-end display and background verification of related pages.
 
It contains serverl urls and view functions, 
such as `accounts/login/, accounts/register/, accounts/reset_password, accounts/change_password` e.t.c and you can use it easily.

### Quick start


1. Install it:
```
	Download the file to your `path/to` and then execute the following command 
  in your django-projects virtual environment or other.
  
	pip3 install --user path/to/django-accounts/dist/django-accounts-0.1.tar.gz
```

2. Add "accounts" to your INSTALLED_APPS setting like this:
```
    INSTALLED_APPS = [
        ...
        'accounts',
    ]
```


3. Include the accounts URLconf in your project urls.py like this::
```
    path('accounts/', include('accounts.urls'))
```

4. Run `python manage.py migrate` to create the auth models and more.

5. In order to provide email activation, you must set up a mailbox.If you are not familiar with
the mailbox settings, I think you can view https://docs.djangoproject.com/zh-hans/2.2/topics/email/.


6. Start the development server and visit `http://127.0.0.1:8000/accounts/register/`
   to create a accounts and more that you can try it.

7. Uninstall it:
	 `pip3 uninstall django-accounts`
   
```
Just do it!
