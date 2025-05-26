from eigen.core import Provider, Service, ServiceConfig, ServiceError, ServiceStatus, EigenConfig
from eigen.models import ServiceConfig, DockerServiceConfig
from docker.errors import ImageNotFound, APIError
import docker

class DockerService(Service):
    """
    Service managed through Docker.
    """
    def __init__(self, slug: str, config: ServiceConfig):
        """
        Initialize the Docker service.

        :param config: Configuration for the Docker service.
        """
        super().__init__(slug, config, DockerServiceConfig)

    def _image_exists(self) -> bool:
        """
        Check if the Docker image exists.
        :return: True if the image exists, False otherwise.
        """
        client = docker.from_env()
        try:
            client.images.get(self._config.provider_data.image)
            return True
        except ImageNotFound:
            return False
        finally:
            client.close()

    @Service.ensure_lock
    def _pull_image(self) -> None:
        """
        Pull the Docker image if it does not exist.
        :raises ServiceError: if the image cannot be pulled.
        """
        client = docker.from_env()
        try:
            client.images.pull(self._config.provider_data.image)
        except APIError as e:
            raise ServiceError(f"Failed to pull Docker image: {e}")
        finally:
            client.close()

    @Service.ensure_lock
    def start(self) -> None:
        """
        Start the Docker service.

        :raises ServiceError: if the service cannot be started.
        """
        if not self._image_exists():
            self._pull_image()

        client = docker.from_env()
        client.containers.run(
            self._config.provider_data.image,
            name=self._config.slug,
            detach=True,
            ports=self._config.provider_data.ports,
            environment=self._config.provider_data.environment,
            volumes=self._config.provider_data.volumes
        )
        client.close()

    @Service.ensure_lock
    def stop(self) -> None:
        """
        Stop the Docker service.

        :raises ServiceError: if the service cannot be stopped.
        """
        if not self._image_exists():
            raise ServiceError("Docker image does not exist, cannot stop service.")
        # Implementation for stopping the Docker service
        raise NotImplementedError("Docker service management is not implemented yet.")

    @Service.ensure_lock
    def restart(self) -> None:
        """
        Restart the Docker service.

        :raises ServiceError: if the service cannot be restarted.
        """
        if not self._image_exists():
            raise ServiceError("Docker image does not exist, cannot restart service.")
        # Implementation for restarting the Docker service
        raise NotImplementedError("Docker service management is not implemented yet.")

    @property
    def status(self) -> ServiceStatus:
        """
        Get the status of the Docker service.

        :return: The status of the Docker service.
        :raises ServiceError: if the status cannot be retrieved.
        """
        # Implementation for getting the status of the Docker service
        raise NotImplementedError("Docker service management is not implemented yet.")

class Docker(Provider):
    """
    Provider for services managed through docker.
    """

    def create_service(self, slug: str, service_config: ServiceConfig, eigen_config: EigenConfig):
        """
        Obtain a Docker service by its name.

        :param slug: The slug of the service.
        :param config: Configuration for the Docker service.
        :return: An instance of the Docker service.
        :raises ServiceError: if the service cannot be obtained.
        """
        # Implementation for obtaining a Docker service
        return DockerService(slug, service_config)
