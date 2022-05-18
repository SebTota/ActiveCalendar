FROM python:3.8
WORKDIR /code
COPY . /code/strava_calendar_summary_web_service
RUN pip install --no-cache-dir --upgrade -r /code/strava_calendar_summary_web_service/requirements.txt
CMD ["uvicorn", "strava_calendar_summary_web_service.server:app", "--host", "0.0.0.0"]