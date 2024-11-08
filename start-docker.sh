docker run -d -p 8088:8088 \
--network=slivka-bio-docker_default -e SLIVKA_URL=http://slivka-bio:8000/ \
  --name dundeewebapp \
  -v your-flask-logs:/var/log/myapp \
  -v your-flask-sessions:/data/sessions \
  -v your-flask-db:/data/db \
  dundeewebapp
