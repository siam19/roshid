# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Development stage
FROM node:18
WORKDIR /app
COPY --from=builder /app ./
RUN chown -R node:node /app
USER node
EXPOSE 3000
CMD ["npm", "run", "dev"]
