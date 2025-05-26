from typing import Optional, Annotated
from pydantic import BaseModel, Field, field_validator, BeforeValidator
from enum import Enum

def protocol_validator(*protocols):
    def validator(cls, value):
        protocol = value.lower()
        if protocol not in protocols:
            raise ValueError(f"Protocol must be one of {protocols}")
        return protocol
    return validator

class ServiceInfo(BaseModel):
    """
    Information about the service, but no information that is crucial to running it.
    """
    name: str = Field(..., description="Name of the service")
    description: str = Field(..., description="Description of the service")
    website: str = Field(..., description="Public website for the service")
    categories: list[str] = Field(..., description="Categories the service belongs to")
    image_src: str = Field(..., description="URL to the service's image")

class ServicePortforwarding(BaseModel):
    """
    Port forwarding configuration for the service.
    """
    enable: bool = Field(..., description="Whether port forwarding is enabled")
    port: int = Field(..., description="Port number for port forwarding")
    protocol: Annotated[str, BeforeValidator(protocol_validator("tcp"))] = Field(..., description="Protocol used for port forwarding (currently only tcp)")

    @field_validator("protocol")
    def validate_protocol(cls, value):
        if value not in ["TCP", "UDP"]:
            raise ValueError("Protocol must be either 'TCP' or 'UDP'")
        return value

class ServiceConfig(BaseModel):
    """
    Configuration for a service.
    """
    enable: Optional[bool] = Field(..., description="Whether the service is enabled")
    provider: str = Field(..., description="Name of the provider managing the service")
    info: ServiceInfo = Field(..., description="Information about the service")
    provider_data: dict = Field(..., description="Additional data specific to the provider")


class ServiceStatus(str, Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    RESTARTING = "restarting"
    ERROR = "error"
    UPDATING = "updating"
    NOT_FOUND = "not_found"
