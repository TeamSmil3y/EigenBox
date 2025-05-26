## This should be a cloud server which hosts frp for all the client box

### For now following configuration is setup

- vm: google cloud instance (34.41.148.109)
- baseos: ubuntu
- applictions: docker
- container: frp

## FRP Server
### config
- mkdir -p /frp-server/conf
- vim /frp-server/conf/frps.ini
[common]
bind_port = 7000
dashboard_port = 7500
dashboard_user = admin
dashboard_pwd = teamsmiley
vhost_http_port = 80

### data dir
- mkdir -p /frp-server/data

### start frps server container
docker run -d \
  --name frp-server \
  -v /frp-server/conf/frps.ini:/frp/frps.ini \
  -v /frp-server/data:/frp/data \
  -p 7000:7000 \
  -p 7500:7500 \
  -p 80:80 \
  snowdreamtech/frps \
  -c /frp/frps.ini

## FRP Client
### config
- mkdir -p /frp-client/conf
- vim /frp-client/conf/frpc.ini
[common]
server_addr = hb.teamsmiley.org
server_port = 7000

[dash]
type = http
local_ip = 127.0.0.1
local_port = 80
custom_domains = dash.smiley.hb.teamsmiley.org
use_https = true

[local-dash]
type = http
local_ip = 127.0.0.1
local_port = 3000
custom_domains = local.dash.smiley.hb.teamsmiley.org
use_https = true

[backend]
type = http
local_ip = 127.0.0.1
local_port = 8080
custom_domains = backend.smiley.hb.teamsmiley.org
use_https = true

[nextcloud]
type = http
local_ip = 127.0.0.1
local_port = 8010
custom_domains = cloud.smiley.hb.teamsmiley.org
use_https = true

[photos]
type = http
local_ip = 127.0.0.1
local_port = 8020
custom_domains = photos.smiley.hb.teamsmiley.org
use_https = true

### start frps client container
docker run -d \
  --name frp-client \
  --restart unless-stopped \
  -v /frp-client/conf/frpc.ini:/frp/frpc.ini \
  --net=host \
  snowdreamtech/frpc \
  -c /frp/frpc.ini

## setting up zerotier controller
- https://sirlagz.net/2023/07/11/how-to-self-host-a-zerotier-controller-on-debian-11/
- docker-compose config (make sure to open inbound and outbound on port udp/9993):
version: "3"

services:
  postgres:
    image: postgres:15.2-alpine
    container_name: postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: ztnet
    volumes:
      - ./volumes/postgres-data:/var/lib/postgresql/data
    networks:
      - app-network

  zerotier:
    image: zyclonite/zerotier:1.14.2
    hostname: zerotier
    container_name: zerotier
    restart: unless-stopped
    volumes:
      - ./volumes/zerotier:/var/lib/zerotier-one
    cap_add:
      - NET_ADMIN
      - SYS_ADMIN
    devices:
      - /dev/net/tun:/dev/net/tun
    networks:
      - app-network
    ports:
      - "9993:9993/udp"
    environment:
      - ZT_OVERRIDE_LOCAL_CONF=true
      - ZT_ALLOW_MANAGEMENT_FROM=172.31.255.0/29

  ztnet:
    image: sinamics/ztnet:latest
    container_name: ztnet
    working_dir: /app
    volumes:
      - ./volumes/zerotier:/var/lib/zerotier-one
    restart: unless-stopped
    ports:
      - 3000:3000
    environment:
      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: ztnet
      NEXTAUTH_URL: "http://localhost:3000"
      NEXTAUTH_SECRET: "teamsmiley"
      NEXTAUTH_URL_INTERNAL: "http://ztnet:3000"
    networks:
      - app-network
    links:
      - postgres
    depends_on:
      - postgres
      - zerotier

  https-proxy:
    image: caddy:latest
    container_name: ztnet-https-proxy
    restart: unless-stopped
    depends_on:
      - ztnet
    command: caddy reverse-proxy --from zerotier.hb.teamsmiley.org --to ztnet:3000
    volumes:
      - ./volumes/caddy:/data
    networks:
      - app-network
    links:
      - ztnet
    ports:
      - "8080:80"
      - "443:443"

networks:
  app-network:
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 172.31.255.0/29
