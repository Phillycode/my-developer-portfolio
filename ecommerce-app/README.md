# Evermarket project - An eCommerce Web application made with Django

This is my project where I built an eCommerce web application using Django. A user registers as either a buyer or vendor, and then gains menu options and permissions based on their user role. Vendors have CRUD functionality over their Stores and Products, while Buyers can view and purchase products as well as leave reviews. When leaving a review, the review will be unverified unless the buyer has purchased the product. Buyers can view, and add items to their cart and checkout (invoice sent to the user's email). Emails are sent as invoices or when a password reset is requested.

Emails are currently file-based and will be stored in the emails folder: evermarket/emails

Database used for this application: MariaDB

Latest updates:

- Added API integration with Django REST Framework (DRF)
- Set up a Twitter dev account and automated tweets to be sent out when new stores or products are added. Twitter account used: @DevRiposte
- Updated and corrected the sequence diagram to display the workings of DRF more effectively

- I made some edits to the groups and register system to help fix permission issues.
- I moved my setup_group_permissions function to utils.py and imported it to the ready method in apps.py to be run once at startup. Then removed the line from register_user as it was no longer needed. Made some additional tweaks for the function to work properly with django's signals utility.

# Setup instructions for the Web APP

- Install MariaDB, and change the database settings in evermarket/settings.py accordingly.
- Create and activate a virtual environment (venv)
- Then install the dependencies from the included requirements.txt file:

```bash
pip install -r requirements.txt
```

- Apply database migrations and run the server.

```bash
python manage.py migrate
python manage.py runserver
```

- Open your browser at http://127.0.0.1:8000

# Twitter setup instructions

The Twitter class has an authenticate() method that is designed to be run only once in order to acquire the Access Token and Access Token Secret required. These can then be saved and stored in the settings.py (check for the Twitter section indicated by the comments).

If you need to acquire a new Access Token and/or Access Token Secret, follow these steps:

```bash
python manage.py shell
```

Enter the following:

```python
from market.functions.twitter import Tweet
Tweet().authenticate()
```

Follow the instructions in the shell to authorize and enter PIN.
Copy and paste the Access Token and Access Token Secret strings into their respective static variables as indicated in settings.py
Save the file and you can now exit the shell:

```python
exit()
```

# Tests

No unit tests are implemented yet.

# Formatters used

- Black for Python
- Prettier for HTML/CSS

# Planning

For project planning files: See planning folder in main branch

# References

The main source of information for this app was the HyperionDev course material.

Additional research done on forms in Django for registration and login forms:
https://docs.djangoproject.com/en/5.2/topics/forms/

I researched the Django decorators such as @login_required for a simple login check before views can be accessed via urls:
Info on this decorator obtained from: https://docs.djangoproject.com/en/5.2/topics/auth/default/

I did additional research on bootstrap's navbar, which is an ideal solution for login, logout and register links at the top of the web app: https://getbootstrap.com/docs/4.0/components/navbar/

Update: Additional research done on the Django Rest Framework and how the sequence diagram can be used to display the structure.
Obtained from: https://felipedemorais.com.br/building-your-first-api-with-django-and-django-rest-framework/

# Credits

Fantasy market banner picture obtained from: https://www.artstation.com/artwork/mq5GNd

Tavern banner picture used in footer obtained from: https://www.reddit.com/r/WidescreenWallpaper/comments/l20a3a/fantasy_tavern_2560x1080/

Man with keys picture obtained from: https://za.pinterest.com/pin/5066618323288978/

Market Icon obtained from: https://www.citypng.com/photo/21576/download-store-marketplace-shopping-black-icon-png
