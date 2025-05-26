from abc import ABC, abstractmethod
from typing import Union
from pathlib import Path

class Config(ABC):
    """
    Abstract base class for configuration management.
    """
    @abstractmethod
    def __init__(self, filepath: Path, data: dict):
        """
        Initialize the Config instance with the given path and data.

        :param filepath: Path to the configuration file.
        :param data: Dictionary containing the configuration data.
        """
        ...

    @classmethod
    @abstractmethod
    def load(cls, filepath: Path) -> Union["Config", type["Config"]]:
        """
        Load the configuration from the specified file.

        :param filepath: Path to the configuration file.
        """
        ...

    @abstractmethod
    def save(self):
        """
        Save the configuration.
        """
        ...
