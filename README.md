# flask-restful-auth

## Deployment
### Instructions for deployment on a Linux server with Node, PM2, Python, MySQL, and Nginx installed. Pyenv recommended.
Clone project from GitHub, create virtual environment, and install modules.
```
git clone https://github.com/kylehench/flask-restful-auth
cd flask-restful-auth
pipenv install
```

Copy .env.example, edit variables in nano or vim:
```
cp .env.example .env
vim .env
```

Export schema (and data if desired) to MySQL. Export to self-contained file and include create schema.
Login to MySQL on server:
```
mysql -u root -p
(enter password)
```

Paste schema in shell and verfiy creation with `SHOW DATABASES;`

Leave the shell with `EXIT;`

Test Server:
```
gunicorn --bind 0.0.0.0:4999 wsgi:application
```

Start app in PM2:
```
pm2 --name=authServer start "cd ~/flask-restful-auth && pipenv run gunicorn --env SCRIPT_NAME=/auth --bind 0.0.0.0:5001 wsgi:application"
```

Configure nginx:
```
sudo vim /etc/nginx/sites-available/default
```
Example location block:
```
location /auth {
  proxy_pass http://localhost:[PORT];
  proxy_http_version 1.1;
  proxy_set_header Upgrade $http_upgrade;
  proxy_set_header Connection 'upgrade';
  proxy_set_header Host $host;
  proxy_set_header X-Forwarded-For $remote_addr;
  proxy_cache_bypass $http_upgrade;
}
```