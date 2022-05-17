# Build step #1: build the React front end
FROM node:17-alpine as build-step

# set working directory
RUN mkdir /app
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
# install and cache app dependencies
COPY package.json /app/package.json
RUN npm install
RUN npm install react-scripts@5.0.1 -g
RUN chmod -R 777 node_modules/.cache
COPY . /app
EXPOSE 3000

ENTRYPOINT [ "npm" ]

CMD ["start"]