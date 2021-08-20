FROM node:16 as build
WORKDIR /app
COPY . ./
RUN npm ci
RUN npm run build && rm -r node_modules
RUN npm ci --only=prod
FROM node:16-bullseye-slim
WORKDIR /app
COPY --from=build /app ./
EXPOSE 80
ENTRYPOINT [ "node", "dist/bundle.min.js" ]