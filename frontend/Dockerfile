FROM node:18-alpine

WORKDIR /app

COPY package.json /app/package.json
RUN npm install --silent

COPY . /app

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]