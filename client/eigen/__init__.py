from pathlib import Path
from tomllib import load as load_toml
from typing import Optional
from .core import Eigen, Config, Service, ServiceStatus, Provider, ServiceConfig, ServiceError

config: Optional[Config] = None
def load_config(config_path: Path) -> None:
    """
    Load the configuration from the specified path.

    :param config_path: Path to the configuration file.
    :raises FileNotFoundError: If the configuration file does not exist.
    """
    global config
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file {config_path} does not exist.")

    with open(config_path, "rb") as f:
        config= load_toml(f)
