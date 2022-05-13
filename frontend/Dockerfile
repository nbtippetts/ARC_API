# Build step #1: build the React front end
FROM node:17-alpine as build-step

# set working directory
RUN mkdir /app
WORKDIR /app
# install and cache app dependencies
COPY package.json /app/package.json
RUN npm install --silent
RUN mkdir node_modules/.cache && chmod -R 777 node_modules/.cache
COPY . /app
EXPOSE 3000

ENTRYPOINT [ "npm" ]

CMD ["start"]