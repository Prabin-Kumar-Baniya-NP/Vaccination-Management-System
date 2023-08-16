# Use the official Python image as the base image
FROM python:3.10

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

RUN apt update && apt upgrade -y
RUN apt install gettext -y

# Copy the requirements file to the container and install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the Django project files to the container
COPY ./mysite/ /app/

ENV DEBUG=True
ENV SECRET_KEY=1234

# Collect static files for Django
RUN python manage.py collectstatic --noinput

RUN python manage.py compilemessages

# Expose the Gunicorn port (change this to the port your Django app uses)
EXPOSE 8000

# Start Gunicorn to serve the Django application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mysite.wsgi:application"]