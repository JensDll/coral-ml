FROM node:16 as build
ARG mode=production
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . ./
RUN npm run build -- --mode ${mode}
# final image
FROM nginx:1.21
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx/replace-vite-env.sh /docker-entrypoint.d
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80