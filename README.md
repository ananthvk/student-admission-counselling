# student-college matcher
This is an implementation of the Gale-Shapely algorithm, also known as the deferred acceptance algorithm, which is used to obtain stable matching. Here, the application tries to match a number of students to courses in various colleges. This project aims to simulate the working of a system such as KCET, COMEDK, or JOSSA.
The algorithm is written in C++, which is then accessed by python through a Cython extension module. The UI is implemented in Django along with Vue for certain pages. Celery and redis is also used for caching and task management.

## Getting started

Firstly, to create the necessary tables:
```
$ docker compose run web python manage.py migrate 
```

Create the superuser with
```
$ docker compose run web python manage.py createsuperuser
```

Then seed the database if required (optional)
```
$ mkdir scm_site/db_data
$ cp dataset/data.json scm_site/db_data
$ docker compose run web python manage.py seed db_data/data.json
$ docker compose run web python manage.py generate_users
$ docker compose down --remove-orphans
```

Start the site with
```
$ docker compose up
```

View the application at [http://localhost:8000/counselling](http://localhost:8000/counselling)

Usernames follow the following pattern: 00001, 00002, 00003 ....

and the password for every user is `password`
