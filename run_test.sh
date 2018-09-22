# start reveljs service
#bash -c 'gnome-terminal --working-directory=/home/maxi/GIT/geostation/revealjs/reveal.js -x grunt serve'
# start tornado server
bash -c 'gnome-terminal --working-directory=/home/maxi/GIT/geostation -x python3 server.py'
# start screen 11
bash -c 'gnome-terminal --working-directory=/home/maxi/GIT/geostation -x python3 screenX.py S11 300x400 1:1'
# start screen 12
bash -c 'gnome-terminal --working-directory=/home/maxi/GIT/geostation -x python3 screenX.py S12 300x400 1:2'
# start lab to run tests
bash -c 'gnome-terminal --working-directory=/home/maxi/GIT/geostation -x jupyter lab'


