FROM node:16 as build
WORKDIR /app
COPY . ./
RUN npm ci && \
  npm run build
EXPOSE 6100
ENTRYPOINT [ "node", "dist/bundle.min.js" ]