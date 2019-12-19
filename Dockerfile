FROM python:3

WORKDIR /app/
ADD app /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

EXPOSE 5000

ENTRYPOINT python /app/com/perosa/dashbot/App.py
