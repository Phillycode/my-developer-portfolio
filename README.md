# Sticky Notes Project

This is a simple but clean sticky notes web application created for the purposes of a bootcamp Django project and is only intended for private use and learning purposes. The application enables all of CRUD options for sticky notes and displays them in a user-friendly manner by making use of Bootstrap's components. Due to the nature of sticky notes and how I personally like to use them, I opted for a single-user application with no requirement for an admin user. The Note model also has an optional title, meaning that you can simply put in a description for the sticky note if it's a reminder or quick note. This helped to keep it simple and is everything that I would like in a sticky note application as it allows for adding and checking quick reminders and removing them as they are completed.

Latest update: Added additional tests in tests.py to cover all use cases.

# Setup instructions

- Create and activate a virtual environment (venv)
- Then install the dependencies from the included requirements.txt file:

```bash
pip install -r requirements.txt
```

- Apply database migrations and run the server:

```bash
python manage.py migrate
python manage.py runserver
```

- Open your browser at http://127.0.0.1:8000

# Running tests:

- You can run tests for this app by navigating to the sticky_notes project folder in your terminal and run:

```bash
python manage.py test notes
```

# Credits and References

**Banner Image:**
Obtained from: (https://www.vecteezy.com/vector-art/25325421-man-in-spider-costume-background)

**Webpage Icon:**
Obtained from: (https://www.flaticon.com/free-icon/spiderweb_3620494)

**References:**
Information to complete this task was primarily obtained from the HyperionDev course material
Additional information on designing with Django, its syntax and template design obtained from:
https://docs.djangoproject.com/en/5.2/intro/overview/#design-your-templates

Additional information on Bootstrap components obtained from: https://getbootstrap.com/docs/5.3/components/

I researched Django auth and session topics for the research part of the task here:
https://docs.djangoproject.com/en/5.2/topics/auth/

I researched how cookies are used to help preserve the state of an HTTP application:
https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies

I investigated the procedures for performing Django database migrations to a server-based relational database like MariaDB:
https://docs.djangoproject.com/en/5.2/ref/databases/
https://docs.djangoproject.com/en/5.2/topics/migrations/

```

```
