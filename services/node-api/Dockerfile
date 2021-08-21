FROM node:16 as build
WORKDIR /app
COPY . ./
RUN npm ci
RUN npm run build && rm -r node_modules
RUN npm ci --only=prod

FROM node:16-bullseye-slim
WORKDIR /app
COPY --from=build /app/dist/bundle.min.js /app/package.json ./
COPY --from=build /app/node_modules ./node_modules
EXPOSE 80
ENTRYPOINT [ "node", "bundle.min.js" ]