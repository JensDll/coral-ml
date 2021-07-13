ffmpeg -re -i stream.avi -vcodec copy -loop -1 -c:a aac -b:a 160k -ar 44100 -strict -2 -f flv rtmp:localhost:1935/live/test



ffmpeg -re -y -i .\stream.avi -vcodec libx264 \
-b:v 600k -r 25 -s 640x480 -filter:v yadif -ab 64k -ac 1 -ar 44100 -f flv \
"rtmp://127.0.0.1:1935/live/livestream"