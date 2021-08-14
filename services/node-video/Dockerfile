FROM node:16 as build
WORKDIR /app
COPY . ./
RUN npm ci
RUN npm run build
FROM node:16-buster-slim
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=prod
COPY --from=build /app/dist/bundle.min.js ./
# Stream in port
EXPOSE 8080
# Socket out port
EXPOSE 80
ENTRYPOINT [ "node", "bundle.min.js" ]