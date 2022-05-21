FROM nginx/unit:1.26.1-python3.10

COPY /backend/requirements.txt /backend/requirements.txt
#COPY google_creds.json google_creds.json
COPY client_secret.json client_secret.json

RUN pip install --upgrade -r /backend/requirements.txt
#RUN npm --prefix frontend/ run build

COPY /backend /backend
COPY /frontend/dist /frontend

COPY nginx/config.json /docker-entrypoint.d/config.json
COPY nginx/bundle.pem /docker-entrypoint.d/bundle.pem
