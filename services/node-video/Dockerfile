FROM node:16 as build

WORKDIR /app
COPY . ./
RUN npm ci
RUN npm run build


FROM node:16-bullseye-slim

WORKDIR /app
COPY --from=build /app/dist/bundle.min.js /app/package.json /app/package-lock.json ./
RUN npm ci --only=prod

ENV MODE=PROD
ENV APP_HOST=node-video

# Stream in port
EXPOSE 8080
ENV PORT_STREAM_IN=8080
# Socket out port
EXPOSE 80
ENV PORT_STREAM_OUT=80

ENTRYPOINT [ "node", "bundle.min.js" ]