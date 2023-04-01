FROM nginx/unit:1.26.1-python3.10

COPY /backend/requirements.txt /backend/requirements.txt
COPY client_secret.json client_secret.json

RUN pip install --upgrade -r /backend/requirements.txt

COPY /backend /backend
COPY /frontend/dist /frontend

COPY nginx/config.json /docker-entrypoint.d/config.json
COPY nginx/bundle.pem /docker-entrypoint.d/bundle.pem
