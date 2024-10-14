# student-college matcher
This is an implementation of the Gale-Shapely algorithm, also known as the deferred acceptance algorithm, which is used to obtain stable matching. Here, the application tries to match a number of students to courses in various colleges. This project aims to simulate the working of a system such as KCET, COMEDK, or JOSSA.
The algorithm is written in C++, which is then accessed by python through a Cython extension module. The UI is implemented in Django along with Vue for certain pages. Celery and redis is also used for caching and task management.

## Getting started

Create a database `scm_site` by using `psql` or `pgadmin`.

Here is one way to do it using psql,
```
$ docker compose up db
$ docker ps
$ docker exec -it <db_container_id> ash
/ # psql -U postgres
postgres=# CREATE DATABASE scm_site;
```

Get a shell to the `web` docker container
```
$ docker compose up web
$ docker ps
$ docker exec -it <web_container_id> ash
```

To create the necessary tables:
```
# python manage.py migrate 
```

Create the superuser with
```
# python manage.py createsuperuser
```

Run this in the host,
```
$ mkdir db_data
$ cp dataset/data.json db_data
```

Then seed the database if required (optional)
```
# python manage.py seed db_data/data.json
# python manage.py generate_users
```

Start the site with
```
$ docker compose up
```

To run tests, use `docker exec -it <web_container_id> ash`, to get a shell and run the following command.
```
# python manage.py test --no-logs --parallel auto
```

View the application at [http://localhost:8000/counselling](http://localhost:8000/counselling)

Usernames follow the following pattern: 00001, 00002, 00003 ....

and the password for every user is `password`
