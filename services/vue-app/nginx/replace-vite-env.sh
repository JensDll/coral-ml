#!/bin/sh

ROOT_DIR=/usr/share/nginx/html

echo "Replacing vite environment variables"
for file in $ROOT_DIR/assets/*.js $ROOT_DIR/index.html
do
  echo "Processing $file ..."
  sed -i "s|__RECORD_API_URI|${API_URI}|g" $file
  sed -i "s|__PROXY_URI|${PROXY_URI}|g" $file
done

exit 0