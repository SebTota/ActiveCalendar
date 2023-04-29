FROM nginx/unit:1.26.1-python3.10

COPY /backend /backend

RUN pip install --upgrade -r /backend/requirements.txt

COPY nginx/config.json /docker-entrypoint.d/config.json
COPY nginx/bundle.pem /docker-entrypoint.d/bundle.pem