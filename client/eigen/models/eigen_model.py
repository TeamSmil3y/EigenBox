from pydantic import BaseModel, Field, BeforeValidator
from . import version_validator, domain_validator, path_converter
from typing import Annotated, Optional
from pathlib import Path

class EigenGeneral(BaseModel):
    """
    General configuration for the Eigen service.
    """
    version: Annotated[str, BeforeValidator(version_validator)] = Field(..., description="Version of the Eigen service")
    root_domain: Annotated[str, BeforeValidator(domain_validator)] = Field(..., description="Root domain for the Eigen service", alias="root-domain")
    subdomain: str = Field(..., description="Subdomain for the Eigen service")
    secret_key: Optional[str] = Field(..., description="Secret key to authenticate to root server", alias="secret-key")

class EigenServices(BaseModel):
    """
    Configuration for services.
    """
    lock_dir: Annotated[Path, BeforeValidator(path_converter)] = Field(..., description="Path to the directory for service locks", alias="lock-dir")
    location: Annotated[Path, BeforeValidator(path_converter)] = Field(..., description="Path to the directory containing service configurations")

class EigenConfig(BaseModel):
    """
    Configuration for the Eigen service.
    """
    general: EigenGeneral = Field(..., description="General configuration for the Eigen service")
    services: EigenServices = Field(..., description="Configuration for services")
