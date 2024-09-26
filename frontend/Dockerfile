FROM node:22

WORKDIR /home/node/app

COPY package.json .

RUN npm install

COPY . .

#RUN npm run build

#RUN npm install -g http-server

EXPOSE 5173

# Command to run the app
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]