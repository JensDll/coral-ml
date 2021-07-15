FROM node:16 as build
WORKDIR /app
COPY . ./
RUN npm ci --only=prod && \
  npm run build
# API Port
# Http MPEG-TS Stream
# Socket video port
EXPOSE 5050 5060 8080
ENTRYPOINT [ "node", "dist/bundle.min.js" ]