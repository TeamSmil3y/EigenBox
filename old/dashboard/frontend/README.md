## nginx config for eigenbox
server {
    listen 80;
    server_name dash.smiley.hb.teamsmiley.org;

    root /opt/Hackaburg25/dashboard/frontend/build;
    index index.html;

    location / {
        try_files $uri /index.html;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot|otf|ttf|map)$ {
        expires 1y;
        access_log off;
        add_header Cache-Control "public";
    }

    error_page 404 /index.html;
}

## setup permissions
sudo chown -R www-data:www-data /opt/Hackaburg25/dashboard/frontend/build
sudo chmod -R 755 /opt/Hackaburg25/dashboard/frontend/build