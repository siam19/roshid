FROM node:22

WORKDIR /app

COPY package*.json ./

RUN npm install


# Change ownership of the app directory to the node user
RUN chown -R node:node /app

USER node


#RUN npm run build

#RUN npm install -g http-server

EXPOSE 5173

# Command to run the app
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]