#!/usr/bin/env bash
# Sets up web servers for deployment of web_static

if [ "$(which nginx)" == "" ]
then
	sudo apt-get upgrade
	sudo apt-get update
	sudo apt-get install -y nginx;
fi

[ -d /data/ ] || sudo mkdir /data/
[ -d /data/web_static/ ] || sudo mkdir /data/web_static/
[ -d /data/web_static/releases/ ] || sudo mkdir /data/web_static/releases/
[ -d /data/web_static/shared/ ] || sudo mkdir /data/web_static/shared/
[ -d /data/web_static/releases/test/ ] || sudo mkdir /data/web_static/releases/test/

html_content='
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nginx Config Status</title>
  <style>
    body {
      display: flex; 
      justify-content;
      align-items: center;
      min-height: 100vh;
      margin: 0;
      font-family: sans-serif;

    }
	h1 {
	  color: green;
	  font-weight: bold;
	}
  </style>
</head>
<body>
  <h1>Your Nginx Config is A-Ok</h1>
</body>
</html>
'
sudo touch /data/web_static/releases/test/index.html
echo "$html_content" | sudo tee /data/web_static/releases/test/index.html

target_dir="/data/web_static/current"
source_dir="/data/web_static/releases/test"

rm -f "$target_dir" && sudo ln -s "$source_dir" "$target_dir"
sudo chown -R ubuntu:ubuntu /data/

new_config="\tserver_name _;\n\n\tlocation \/hbnb_static\/ \{\n\t\talias \/data\/web_static\/current\/;\n\t\tindex index.html index.htm;\n\t\}\n"

sudo sed -i "s/\tserver_name _;/$new_config/" /etc/nginx/sites-enabled/default

sudo service nginx restart