FROM node:16 as build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=prod 
COPY . ./
RUN npm run build

# final image
FROM nginx:1.21
EXPOSE 80
COPY --from=build /app/dist /usr/share/nginx/html