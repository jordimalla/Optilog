FROM python:3.12

WORKDIR /Optilog

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy docker-entrypoint.sh
COPY ./docker-entrypoint.sh ./docker-entrypoint.sh

# copy project
COPY . .

# run docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]