FROM node:18-alpine

WORKDIR /app

# Install global Quasar CLI
RUN npm install -g @quasar/cli

# Copy all configuration files first
COPY package.json yarn.lock ./
COPY quasar.config.ts tsconfig.json eslint.config.js postcss.config.js ./
COPY index.html ./

# Install dependencies
RUN yarn install

# Copy source files and assets
COPY public ./public
COPY src ./src

EXPOSE 9000

# Development mode with host setting for docker
CMD ["quasar", "dev", "-H", "0.0.0.0"]