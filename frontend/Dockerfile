FROM node:18-alpine

WORKDIR /app

# Install global Quasar CLI
RUN npm install -g @quasar/cli

# Copy package files
COPY package*.json ./
RUN npm install

# Copy the rest of the application
COPY . .

EXPOSE 9000

# Development mode
CMD ["quasar", "dev"]