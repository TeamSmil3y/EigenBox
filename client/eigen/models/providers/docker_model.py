from typing import Any
from pydantic import BaseModel, Field

class DockerServiceConfig(BaseModel):
    image: str = Field(..., description="Docker image to use for the service")
    container_name: str = Field(..., description="Name of the Docker container")
    memory: str = Field(..., description="Memory limit for the Docker container")
    ports: dict[str, int] = Field(..., description="List of ports to expose from the container")
    volumes: list[str] = Field(..., description="List of volumes to mount in the container")
    environment: dict[str, Any] = Field(..., description="Environment variables to set in the container")
