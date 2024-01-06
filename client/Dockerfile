From node:lts-alpine

WORKDIR /app

COPY ./client /app

RUN npm install

RUN npm run build

RUN npm install -g serve

CMD ["serve", "-s", "dist"]