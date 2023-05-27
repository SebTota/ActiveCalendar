FROM node:lts-alpine

WORKDIR /frontend

RUN npm install vue@latest

COPY package*.json ./

RUN npm install

COPY . .

CMD ["npm", "run", "dev"]
