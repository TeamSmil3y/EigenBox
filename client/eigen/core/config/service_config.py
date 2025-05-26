from ...models import ServiceConfig as ServiceConfigModel
from . import TomlConfig
import toml
from pathlib import Path

class ServiceConfig(ServiceConfigModel, TomlConfig):
    def __init__(self, filepath: Path, service_config_data: dict):
        """
        Initialize the service configuration.

        :param filepath: The path to the service configuration file.
        :param service_config: The configuration for the service.
        """
        super().__init__(**service_config_data)
        self._filepath = filepath

    @classmethod
    def load(cls, filepath: Path) -> "ServiceConfig":
        """
        Load the service configuration from the specified file.

        :param filepath: The path to the service configuration file.
        :raises FileNotFoundError: If the configuration file does not exist.
        :raises ValueError: If the file does not have a .toml extension.
        :raises ValidationError: If the service configuration is invalid.
        :raises TomlDecodeError: If the file is not a valid TOML file.
        :return: An instance of ServiceConfig with the loaded configuration.
        """
        data = cls._load_toml(filepath)
        return cls(filepath, data)

    def save(self) -> None:
        """
        Save the service configuration to the file.

        :raises IOError: If there is an error writing to the file.
        """
        self._save_toml(self._filepath, dict(self))
