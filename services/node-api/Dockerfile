FROM node:17 as build
WORKDIR /app
COPY . ./
RUN npm ci
RUN npm run build

FROM node:17

WORKDIR /app
COPY --from=build /app/dist/bundle.js /app/package.json /app/package-lock.json ./
RUN npm ci --only=prod

ENV MODE=PROD

ENV APP_HOST=node-api
ENV APP_LISTEN=80

ENV CORAL_HOST=coral-app
ENV CORAL_PORT_MODEL_MANAGER=7000
ENV CORAL_PORT_IMAGE_CLASSIFICATION=7020
ENV CORAL_PORT_IMAGE_SETTINGS=7021
ENV CORAL_PORT_VIDEO_SETTINGS=7041

EXPOSE 80
ENTRYPOINT [ "node", "bundle.js" ]