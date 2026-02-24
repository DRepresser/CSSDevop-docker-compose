# frontend/Dockerfile
FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# The built files are in /app/dist
# Caddy will mount this via a named volume
CMD ["sh", "-c", "cp -r /app/dist/* /shared/ && echo 'Frontend build complete'"]
