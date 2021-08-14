FROM nginx:1.21

ENV RECORD_API_URI=record-api
ENV NODE_API_URI=node-api
ENV NODE_VIDEO_URI=node-video

COPY replace-env.sh /docker-entrypoint.d
RUN chmod +x /docker-entrypoint.d/replace-env.sh
COPY default.conf /etc/nginx/conf.d/default.conf