FROM dockercodata.pb.gov.br/ci-base-images/node:18 AS build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install --no-save
COPY . .
RUN npm run build

# produção
FROM dockercodata.pb.gov.br/ci-base-images/nginx:latest
COPY --from=build-stage --chown=nginx:nginx /app/dist .
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
