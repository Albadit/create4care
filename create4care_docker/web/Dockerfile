# Use official Node.js image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy project files
COPY web .

# Install dependencies
RUN npm install

# Build Next.js app
RUN npm run build

# Start the app
CMD ["npm", "start"]
