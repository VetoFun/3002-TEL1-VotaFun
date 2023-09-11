# Use the official Node.js image
FROM node:18-slim

# Set the working directory in the container
WORKDIR /app

# Copy dependencies files to the container
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code to the container
COPY . .

# Expose the port on which your React app will run (usually 3000)
EXPOSE 3000

# Start the React app
CMD ["npm", "start"]
