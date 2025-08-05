FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Create next.config.js for standalone build
RUN echo "/** @type {import('next').NextConfig} */" > next.config.js && \
    echo "const nextConfig = {" >> next.config.js && \
    echo "  output: 'standalone'," >> next.config.js && \
    echo "  experimental: {" >> next.config.js && \
    echo "    appDir: true" >> next.config.js && \
    echo "  }" >> next.config.js && \
    echo "}" >> next.config.js && \
    echo "module.exports = nextConfig" >> next.config.js

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000 || exit 1

# Run the application
CMD ["npm", "run", "dev"]