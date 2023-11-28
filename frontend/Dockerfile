FROM node:18-alpine

# Setting up the work directory
WORKDIR /frontend

# Installing dependencies
COPY ./package.json .

RUN yarn install

COPY . .

EXPOSE 3000

# Starting our application
CMD yarn start
