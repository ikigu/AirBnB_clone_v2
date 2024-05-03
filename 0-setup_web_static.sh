#!/usr/bin/env bash
# Sets up web servers for deployment of web_static

if [ "$(which nginx)" == "" ]
then
	sudo apt-get upgrade
	sudo apt-get update
	sudo apt-get install -y nginx;
fi

sudo mkdir -p /data/web_static/releases/
sudo mkdir /data/web_static/shared/
sudo mkdir /data/web_static/releases/test/

html_content='
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nginx Confi Status</title>
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
sudo chown -R ikigu:ikigu /data/

new_config="
	server_name _;

	location /hbnb_static/ {
		alias /data/web_static/current/;
		index index.html index.htm;
	}
"

sudo sed -i "s/\tserver_name _;/$new_config/" /etc/nginx/sites-enabled/default