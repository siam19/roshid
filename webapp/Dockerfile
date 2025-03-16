# Development stage
FROM node:20-alpine AS development

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install


# Change ownership of the /app directory to the node user
RUN chown -R node:node /app

# Switch to the node user
USER node

# Expose the port Next.js runs on
EXPOSE 3001

# Start the development server
CMD ["npm", "run", "dev", "--", "-L"]


# Production stage
FROM node:20-alpine AS production

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install production dependencies
RUN npm ci --only=production

# Copy the rest of the application code
# COPY . .

# # Build the Next.js application
# RUN npm run build

# Change ownership of the /app directory to the node user
RUN chown -R node:node /app

# Switch to the node user
USER node

# Expose the port Next.js runs on
EXPOSE 4000

# Start the production server
# CMD ["npm", "start"]