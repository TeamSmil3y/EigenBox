from ...models import EigenConfig as EigenConfigModel
from . import TomlConfig
from pathlib import Path

class EigenConfig(EigenConfigModel, TomlConfig):
    def __init__(self, config_path: Path, config_data: dict):
        """
        Initialize the Config instance with the given path and data.

        :param config_path: Path to the configuration file.
        :param config_data: Dictionary containing the configuration data.
        """
        super().__init__(self, config_data)

        self._path = config_path

        self.services._location = self.services.location
        self.services.location = self._path / Path(self.services._location)


    @classmethod
    def load(cls, filepath: Path) -> "EigenConfig":
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
        Save the current configuration to the file.

        :raises IOError: If there is an error writing to the file.
        """
        self._save_toml(self._path, dict(self))

    def to_toml(self) -> str:
        """
        Convert the configuration to a TOML string.

        :return: A string representation of the configuration in TOML format.
        """
        dict_data = dict(self)
        dict_data["services"]["location"] = self.services._location
        return "s"
