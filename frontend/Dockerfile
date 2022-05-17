# Build step #1: build the React front end
FROM node:17-alpine as build-step

# set working directory
RUN mkdir /app
WORKDIR /app
# install and cache app dependencies
COPY package.json /app/package.json
RUN mkdir /app/node_modules
RUN chown -R node:node /app/node_modules
RUN npm install
RUN npm install react-scripts@5.0.1 -g
COPY . /app
EXPOSE 3000

ENTRYPOINT [ "npm" ]

CMD ["start"]