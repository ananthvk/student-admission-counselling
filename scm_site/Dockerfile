FROM python:3.12-alpine
RUN echo "#!/bin/sh" > /start_celery_worker
#RUN echo "python -m celery -A scm_site worker -l info" >> /start_celery_worker
RUN echo "python manage.py start_celery_worker" >> /start_celery_worker
RUN chmod +x /start_celery_worker
WORKDIR /app 
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]