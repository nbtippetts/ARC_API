# Build step #1: build the React front end
FROM node:17-alpine as build-step

# set working directory
RUN mkdir /app
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json ./
RUN mkdir ./node_modules
RUN chown -R node:node ./node_modules
RUN npm install
RUN npm install react-scripts@5.0.1 -g
COPY . /app
EXPOSE 3000

ENTRYPOINT [ "npm" ]

CMD ["start"]