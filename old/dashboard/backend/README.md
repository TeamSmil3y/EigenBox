| Method | Endpoint                           | Description                                  |
| ------ | ---------------------------------- | -------------------------------------------- |
| GET    | `/services/list`                   | List all available services.                 |
| GET    | `/services/{service_name}/status`  | Get the status of a specific service.        |
| GET    | `/services/{service_name}/help`    | Get help information for a specific service. |
| GET    | `/services/{service_name}/restart` | Restart a specific service.                  |
| GET    | `/services/{service_name}/stop`    | Stop a specific service.                     |
| GET    | `/services/{service_name}/start`   | Start a specific service.                    |


## Examples
- curl http://localhost:8080/services/list
  ```json
  {
    "nextcloud": {
      "status": "running",
      "description": "Self-hosted cloud storage and collaboration platform."
    },
    "immich": {
      "status": "not found",
      "description": "Self-hosted Google Photos alternative with AI features."
    }
  }
- curl http://localhost:8080/services/nextcloud/status
  ```json
  {
    "status": "running"
  }
- curl http://localhost:8080/services/nextcloud/restart
  ```json
  {
    "status": "restarted"
  }
- curl http://localhost:8080/services/nextcloud/start
  ```json
  {
    "help": "Self-hosted cloud storage and collaboration platform."
  }

- curl http://localhost:8080/services/immich/status
- curl http://localhost:8080/services/immich/start
- curl http://localhost:8080/services/immich/stop

## Raw docker commands
- docker run -d --memory 1024m --name nextcloud \
  -v /opt/nextcloud/data:/var/www/html/data \
  -p 8010:80 \
  nextcloud
- docker run -d --memory 2048m --name immich_server \
  -v /opt/immich/data:/app/data \
  -p 8020:2283 \
  altran1502/immich-server:v1.89.0/immich-server:latest
- docker run --memory 2048m --name immich_server -v /opt/immich/data:/app/data -p 8020:2283 altran1502/immich-server:v1.89.0
- docker run --rm --name immich_server -v /opt/immich/data:/app/data -p 8020:2283 altran1502/immich-server:v1.89.0
- docker run --rm --name nextcloud -v /opt/nextcloud/data:/var/www/html/data -p 8010:80 nextcloud

## raspi config
- hostname: raspberrypi.local
- username: teamsmiley
- password: teamsmiley
- public-ip: 100.124.251.22

## tailscale oatuh client
- client id: kTFg6gjfRC21CNTRL
- client secret: tskey-client-kTFg6gjfRC21CNTRL-dUjJpNkSFLNpvGh6fgk2MNrVMs1uJQYsE

## Development
- Create virtual environment  
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate

- Setup dependencies
  ```bash
  pip freeze > requirements.txt
  pip install -r requirements.txt