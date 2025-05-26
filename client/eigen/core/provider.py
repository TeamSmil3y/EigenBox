from abc import ABC, abstractmethod
from . import Service, ServiceConfig, ServiceError, EigenConfig

class ProviderError(Exception):
    pass

class Provider(ABC):
    """
    Abstract base class for a provider.
    """
    @abstractmethod
    def create_service(self, slug: str, service_config: ServiceConfig, eigen_config: EigenConfig) -> Service:
        """
        Obtain a service by its name.

        :param slug: The slug of the service.
        :param service_config: The configuration for the service.
        :param config: The Eigen configuration.
        :return: An instance of Service.
        :raises ProviderError: if the service cannot be obtained.
        """
        ...
