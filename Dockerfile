FROM python:3.8
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./strava_calendar_summary_web_service /code/strava_calendar_summary_web_service
COPY ./private_key.pem /code/private_key.pem
COPY ./cert_key.pem /code/cert_key.pem
EXPOSE 80
CMD ["uvicorn", "strava_calendar_summary_web_service.server:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80", "--ssl-certfile", "cert_key.pem", "--ssl-keyfile", "private_key.pem"]