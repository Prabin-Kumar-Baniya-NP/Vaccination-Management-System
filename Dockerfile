FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt update && apt upgrade -y
RUN apt install gettext -y

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./mysite/ /app/

ENV DEBUG=True
ENV SECRET_KEY=1234

RUN python manage.py collectstatic --noinput

RUN python manage.py compilemessages

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mysite.wsgi:application"]