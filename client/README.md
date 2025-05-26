# Eigen
Eigen is a python service management suite designed to simplify the management of services in a microservices architecture. It provides a unified interface for controlling services, managing configurations, and accessing logs.

## Features
- **Service Management**: Start, stop, restart services, and check their status.
- **Configuration Management**: Load, save, and modify service configurations.
- **Logging**: Access service logs for debugging and monitoring.

### ToDo
- [X] Implement basic web interface.
- [X] Implement basic service management features.
- [ ] Implement search functionality for services.
- [ ] Add logging capabilities.
- [ ] Implement reverse proxy management.
- [ ] Implement mesh network management.
- [ ] Add more service management features. (?)

## Usage
### EigenWeb
EigenWeb is a web interface for managing services. It allows you to view and control services through a user-friendly interface.

#### Start the web interface
```bash
poetry install
poetry run eigen-web
```

### EigenAPI
#### Control a service
```python
from eigen import Eigen
from pathlib import Path

CONFIG_PATH: Path = ...
eigen = Eigen(CONFIG_PATH)

# List all services
for service in eigen.services:
    print(service.name, service.status)

# Get a specific service
my_service = eigen.services["my_service"]

with my_service.lock:
    # Start the service
    my_service.start()
    # Restart the service
    my_service.restart()
    # Stop the service
    my_service.stop()

# Get the status of the service
print(my_service.status)
# Get the logs of the service
print(my_service.logs)

# NOTE: the following will require access to an eigen root server
with my_service.lock:
    # turn on reverse proxy
    my_service.enable_reverse_proxy()
    # turn off reverse proxy
    my_service.disable_reverse_proxy()
```

#### Manage configurations
```python
...
my_config = my_service.config
my_config.description = "New description"
my_config.save()
```
