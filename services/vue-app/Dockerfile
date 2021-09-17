FROM node:16 as build
ARG mode=production
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . ./
RUN npm run build -- --mode ${mode}
# Final image
FROM nginx:1.21
ENV PROXY_URI=iot2050-debian
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx/replace-vite-env.sh /docker-entrypoint.d
RUN chmod +x /docker-entrypoint.d/replace-vite-env.sh
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80