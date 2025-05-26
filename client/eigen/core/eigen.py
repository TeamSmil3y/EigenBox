from toml import TomlDecodeError
from . import EigenConfig, Service, Provider
from ..models import ServiceConfig
from ..providers import PROVIDERS
from tomllib import load as load_toml
import logging
from pydantic import ValidationError
from pathlib import Path

class Eigen:
    """
    Eigen class for managing the Eigen service.
    """
    def __init__(self, config_path: Path):
        self.config = EigenConfig.load(config_path)
        self._service_configs = self._gather_configs()
        self.services = self._gather_services()

    def _gather_configs(self) -> dict[str, ServiceConfig]:
        """
        Gather all service configs. Invalid configs are ignored.

        :return: A dictionary of service configs keyed by their slug.
        """
        service_dir = Path(self.config.services.location)
        service_configs = {}
        for service_path in service_dir.glob("*.toml"):
            if service_path.is_dir():
                continue
            slug = service_path.stem
            try:
                service_configs[slug] = self._get_config(slug)
            except ValidationError as e:
                # invalid service configuration, log the error and continue
                logging.error(f"Invalid service configuration for '{slug}': {e}")
            except TomlDecodeError as e:
                # invalid TOML file, log the error and continue
                logging.error(f"Invalid TOML file for service '{slug}': {e}")
        return service_configs

    def _gather_services(self) -> dict[str, ServiceConfig]:
        """
        Gather all services from the service configurations.

        :return: A dictionary of services keyed by their slug.
        """
        services = {}
        for slug, service_config in self._service_configs.items():
            services[slug] = self._create_service(slug, service_config)
        return services

    def _create_service(self, slug, service_config: ServiceConfig) -> Service:
        """
        Create a service instance from the given configuration.

        :param service_config: The configuration for the service.
        :raises ValueError: If the provider for the service is not found.
        :raises ProviderError: If the service cannot be created.
        :return: An instance of Service.
        """
        provider = PROVIDERS.get(service_config.provider)
        if not provider:
            raise ValueError(f"Provider '{service_config.provider}' not found for service '{service_config.slug}'.")
        return provider.create_service(slug, service_config, self.config)

    def _get_config(self, slug: str) -> ServiceConfig:
        """
        Get the configuration for a service by its slug.

        :param slug: The slug of the service.
        :raises FileNotFoundError: If the service configuration file does not exist.
        :raises ValidationError: If the service configuration is invalid.

        :return: The configuration for the service.
        """
        service_dir = self.config.services.location
        service_path = service_dir / f"{slug}.toml"

        return ServiceConfig.load(service_path)
