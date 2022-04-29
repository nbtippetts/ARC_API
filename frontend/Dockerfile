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
RUN npm run build
# CMD ["npm", "start"]


# Build step #2: build an nginx container
FROM nginx:stable-alpine
COPY --from=build-step /app/build /usr/share/nginx/html
COPY deployment/nginx.default.conf /etc/nginx/conf.d/default.conf