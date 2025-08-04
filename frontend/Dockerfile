FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

# Instalar herramientas de diagnóstico
RUN apk add --no-cache curl iputils bind-tools

COPY . .

EXPOSE 5173

# Asegurarnos de que el servidor Vite escuche en todas las interfaces
ENV HOST=0.0.0.0

CMD ["npm", "run", "dev"]