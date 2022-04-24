FROM python:3.8
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./strava_calendar_summary_web_service /code/strava_calendar_summary_web_service
CMD ["uvicorn", "strava_calendar_summary_web_service.server:app", "--host", "0.0.0.0", "--port", "80"]