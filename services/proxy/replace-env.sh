#!/bin/sh

set -e

CONF_LOCATION=/etc/nginx/conf.d/default.conf

echo "Replacing environment variables"

sed -i "s|\$RECORD_API_URI|${RECORD_API_URI}|g" $CONF_LOCATION
sed -i "s|\$NODE_API_URI|${NODE_API_URI}|g" $CONF_LOCATION
sed -i "s|\$NODE_VIDEO_URI|${NODE_VIDEO_URI}|g" $CONF_LOCATION

exit 0