## Etapa 1 — build
FROM node:20-alpine AS builder

ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=$REACT_APP_API_URL

WORKDIR /app

COPY package*.json .
RUN npm ci

COPY . .
RUN npm run build

## Etapa 2 — servidor estático con nginx
FROM nginx:alpine

COPY --from=builder /app/build /usr/share/nginx/html

# Configuración nginx para SPA (React Router)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
