from pydantic import ValidationError
from pathlib import Path
import re

def domain_validator(domain: str) -> str:
    """
    Validate a domain name.

    :param domain: The domain name to validate.
    :raises ValidationError: If the domain is invalid.
    :return: The validated domain name.
    """
    if not re.match(r"^([A-Za-z0-9-]+\\.)+[A-Za-z]+$", domain):
        raise ValidationError(f"Invalid domain name: {domain}")
    return domain

def port_validator(port: int) -> int:
    """
    Validate a port number.

    :param port: The port number to validate.
    :raises ValidationError: If the port is not in the range 1-65535.
    :return: The validated port number.
    """
    if not (1 <= port <= 65535):
        raise ValidationError(f"Port must be between 1 and 65535, got {port}")
    return port

def version_validator(version: str) -> str:
    """
    Validate a version string.

    :param version: The version string to validate.
    :raises ValidationError: If the version is not in the format X.Y.Z.
    :return: The validated version string.
    """
    if not re.match(r"^\d+\.\d+\.\d+$", version):
        raise ValidationError(f"Invalid version format: {version}")
    return version

def set_validator(*items):
    """
    Create a validator that checks if a value is in a set of allowed items.

    :param items: A set of allowed values.
    :return: A validator function that raises ValueError if the value is not in the set.
    """
    def validator(value):
        """
        Validator function that checks if the value is in the set of allowed items.

        :param value: The value to validate.
        :raises ValueError: If the value is not in the set of allowed items.
        """
        if value not in items:
            raise ValueError(f"Value must be one of {items}, got {value}")
        return value
    return validator

def path_converter(path: str) -> Path:
    """
    Convert a path to a standardized format.

    :param path: The path to convert.
    :raises ValidationError: If the path is not valid.
    :return: The standardized path.
    """
    try:
        filepath = Path(path)
    except Exception as e:
        raise ValidationError(f"Invalid path: {path}. Error: {e}")
    return filepath
