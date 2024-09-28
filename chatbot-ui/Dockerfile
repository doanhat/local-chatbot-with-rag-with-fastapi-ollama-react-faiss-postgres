# Dockerfile for frontend
FROM node:16

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of your application code
COPY . .

# Build the application
RUN npm run build

# Serve the application
CMD ["npx", "serve", "-s", "build", "-l", "3000"]
