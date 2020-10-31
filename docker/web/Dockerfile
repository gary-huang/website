FROM node:14.15.0-buster-slim

WORKDIR /app

COPY ./web/yarn.lock ./web/package.json ./web/tsconfig.json /app/
RUN yarn install
