from . import Config
from pathlib import Path
import toml

class TomlConfig(Config):
    @classmethod
    def _load_toml(cls, filepath: Path) -> dict:
        """
        Load the data from the specified toml file.

        :param filepath: The path to the toml file.
        :raises FileNotFoundError: If the toml file does not exist.
        :raises ValueError: If the file does not have a .toml extension.
        :raises TOMLDecodeError: If the file is not a valid toml file.
        :return: A dictionary containing the toml data.
        """
        if not filepath.exists() or filepath.is_dir():
            raise FileNotFoundError(f"Toml file {filepath} does not exist.")
        if filepath.suffix.lower() != ".toml":
            raise ValueError(f"Toml file {filepath} must have a .toml extension.")

        with open(filepath, "r") as f:
            data = toml.load(f)

        return data

    @classmethod
    def _save_toml(cls, filepath: Path, data: dict) -> None:
        """
        Save the service configuration to the specified file.

        :param filepath: The path to the service configuration file.
        :param data: The configuration data to save.
        :raises IOError: If there is an error writing to the file.
        """
        with open(filepath, "w") as f:
            toml.dump(data, f)
