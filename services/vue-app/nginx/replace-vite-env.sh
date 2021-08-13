#!/bin/sh

ROOT_DIR=/usr/share/nginx/html

echo "Replacing vite environment variables"
for file in $ROOT_DIR/assets/*.js $ROOT_DIR/index.html
do
  echo "Processing $file ..."
  sed -i "s|VITE_RECORD_API|${RECORD_API}|g" $file
  sed -i "s|VITE_NODE_API|${NODE_API}|g" $file 
  sed -i "s|VITE_NODE_VIDEO|${NODE_VIDEO}|g" $file 
done

exit 0