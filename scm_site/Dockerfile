FROM python:3.12-alpine AS build
# Install required build tools
RUN apk add --no-cache build-base python3-dev meson cython libstdc++
WORKDIR /app
COPY pymatcher-src .
RUN pip wheel . -w /app/wheels

FROM python:3.12-alpine
RUN apk add --no-cache libstdc++
RUN echo "#!/bin/sh" > /start_celery_worker
#RUN echo "python -m celery -A scm_site worker -l info" >> /start_celery_worker
RUN echo "python manage.py start_celery_worker" >> /start_celery_worker
RUN chmod +x /start_celery_worker
WORKDIR /app 
COPY --from=build /app/wheels /app/wheels
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install /app/wheels/*.whl
COPY scm_site ./
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]