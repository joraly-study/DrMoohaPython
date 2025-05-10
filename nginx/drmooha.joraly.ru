server {
    listen 80;
    server_name drmooha.joraly.ru;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name drmooha.joraly.ru;

    ssl_certificate /etc/letsencrypt/live/drmooha.joraly.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/drmooha.joraly.ru/privkey.pem;
    
    # Рекомендуемые настройки SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;
    ssl_stapling on;
    ssl_stapling_verify on;
    add_header Strict-Transport-Security "max-age=31536000" always;

    client_max_body_size 10M;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /c/Code/Python/DrMoohaPython/drmooha/static/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
        try_files $uri $uri/ =404;
    }

    location /media/ {
        alias /c/Code/Python/DrMoohaPython/drmooha/media/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
        try_files $uri $uri/ =404;
        autoindex on;
        autoindex_exact_size off;
        autoindex_localtime on;
    }
} 