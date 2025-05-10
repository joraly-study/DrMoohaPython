server {
    listen 80;
    listen [::]:80;
    server_name joraly.ru www.joraly.ru;

    # Redirect all HTTP requests to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name joraly.ru www.joraly.ru;

    ssl_certificate /etc/letsencrypt/live/joraly.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/joraly.ru/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    root /var/www/joraly.ru;
    index index.html index.htm index.nginx-debian.html;

    location /robots.txt {
        alias /var/www/moe.joraly.ru/robots.txt;
    }

    location = /favicon.ico {
        log_not_found off;
        access_log off;
    }

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Reverse proxy for the Express.js backend
    location /api/ {
        proxy_pass http://localhost:3000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
