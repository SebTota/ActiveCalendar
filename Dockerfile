FROM python:3.8
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./strava_calendar_summary_web_service /code/strava_calendar_summary_web_service
COPY cert.pem /code/cert.pem
COPY key.pem /code/key.pem

EXPOSE 80
EXPOSE 443

CMD ["uvicorn", "strava_calendar_summary_web_service.server:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "443", "--ssl-certfile", "cert.pem", "--ssl-keyfile", "key.pem"]
