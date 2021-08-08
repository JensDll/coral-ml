FROM node:16 as build
WORKDIR /app
COPY . ./
RUN npm ci
RUN npm run build
FROM node:16-buster-slim
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=prod
COPY --from=build /app/dist ./
EXPOSE 5050
ENTRYPOINT [ "node", "bundle.min.js" ]