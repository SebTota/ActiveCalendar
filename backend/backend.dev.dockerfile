FROM python:3.8

COPY requirements.txt requirements.txt

RUN pip install --upgrade -r requirements.txt

ENV ENVIRONMENT=development

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "80", "--reload"]