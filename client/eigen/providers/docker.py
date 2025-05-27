from eigen.core import Provider, Service, ServiceConfig, ServiceError, ServiceStatus, EigenConfig
from eigen.models import ServiceConfig, DockerServiceConfig
from docker.errors import ImageNotFound, APIError
from typing import Callable
import time
import docker

class DockerService(Service):
    """
    Service managed through Docker.
    """
    LOCK_DELAY = 10
    def __init__(self, slug: str, config: ServiceConfig, eigen_config: EigenConfig):
        """
        Initialize the Docker service.

        :param config: Configuration for the Docker service.
        """
        super().__init__(slug, config, eigen_config, DockerServiceConfig)

        self._last_status_update = 0
        self._cached_status = ServiceStatus.UNKNOWN

    def _image_exists(self) -> bool:
        """
        Check if the Docker image exists.
        :return: True if the image exists, False otherwise.
        """
        client = docker.from_env()
        try:
            client.images.get(self._config.provider.options.image)
            return True
        except ImageNotFound:
            return False
        finally:
            client.close()

    def _pull_image(self) -> None:
        """
        Pull the Docker image if it does not exist.
        :raises ServiceError: if the image cannot be pulled.
        """
        client = docker.from_env()
        try:
            client.images.pull(self._config.provider.options.image)
        except APIError as e:
            raise ServiceError(f"Failed to pull Docker image: {e}")
        finally:
            client.close()

    def _container_exists(self) -> bool:
        """
        Check if the Docker container exists.
        :return: True if the container exists, False otherwise.
        """
        client = docker.from_env()
        try:
            client.containers.get(self.slug)
            return True
        except docker.errors.NotFound:
            return False
        finally:
            client.close()

    def _create_container(self) -> None:
        """
        Create a Docker container if it does not exist.
        :raises ServiceError: if the container cannot be created.
        """
        client = docker.from_env()
        try:
            client.containers.create(
                self._config.provider.options.image,
                name=self.slug,
                detach=True,
                ports=self._config.provider.options.ports,
                environment=self._config.provider.options.environment,
                volumes=self._config.provider.options.volumes
            )
        except APIError as e:
            raise ServiceError(f"Failed to create Docker container: {e}")
        finally:
            client.close()

    @staticmethod
    def _ensure_container_exists(func) -> Callable:
        """
        Decorator to ensure the Docker container exists before executing a function.
        :param func: The function to execute.
        """
        def wrapper(self, *args, **kwargs):
            """
            Ensure the Docker container exists before executing the function.
            :raises ServiceError: if the container does not exist and cannot be created.
            """
            if not self._image_exists():
                self._pull_image()
            if not self._container_exists():
                self._create_container()
            return func(self, *args, **kwargs)
        return wrapper

    @_ensure_container_exists
    def _start(self) -> None:
        """
        Start the Docker service.

        :raises ServiceError: if the service cannot be started.
        """
        client = docker.from_env()
        client.containers.get(self.slug).start()
        # small delay to ensure the container is fully started
        self.lock.add_delay(self.LOCK_DELAY)
        client.close()

    @_ensure_container_exists
    def _stop(self) -> None:
        """
        Stop the Docker service.

        :raises ServiceError: if the service cannot be stopped.
        """
        client = docker.from_env()
        client.containers.get(self.slug).stop()
        # small delay to ensure the container has time to stop gracefully
        self.lock.add_delay(self.LOCK_DELAY)
        client.close()

    @_ensure_container_exists
    def _restart(self) -> None:
        """
        Restart the Docker service.

        :raises ServiceError: if the service cannot be restarted.
        """
        client = docker.from_env()
        client.containers.get(self.slug).restart()
        # small delay to ensure the container is fully restarted
        self.lock.add_delay(self.LOCK_DELAY)
        client.close()

    def is_installed(self) -> bool:
        """
        Check if the Docker service is installed.

        :return: True if the Docker service is installed, False otherwise.
        """
        return self._image_exists()

    def _install(self) -> None:
        """
        Install the Docker service by pulling the image.

        :raises ServiceError: if the image cannot be pulled.
        """
        if not self._image_exists():
            self._pull_image()
            self.lock.add_delay(5)
        else:
            raise ServiceError("Docker service is already installed.")

    def _uninstall(self) -> None:
        """
        Uninstall the Docker service by removing the container and image.

        :raises ServiceError: if the container or image cannot be removed.
        """
        client = docker.from_env()
        try:
            self.lock.add_delay(self.LOCK_DELAY)
            if self._container_exists():
                container = client.containers.get(self.slug)
                container.remove(force=True)
            if self._image_exists():
                client.images.remove(self._config.provider.options.image, force=True)
        except APIError as e:
            raise ServiceError(f"Failed to uninstall Docker service: {e}")
        finally:
            client.close()

    def _status(self) -> ServiceStatus:
        """
        Get the status of the Docker service.

        :return: The status of the Docker service.
        :raises ServiceError: if the status cannot be retrieved.
        """

        current_time = time.time()
        if current_time - self._last_status_update < 5:
            return self._cached_status

        self._last_status_update = current_time
        if not self._container_exists():
            status = ServiceStatus.STOPPED if self._image_exists() else ServiceStatus.NOT_FOUND
            self._cached_status = status
            return status

        client = docker.from_env()
        try:
            container = client.containers.get(self.slug)
            match(container.status):
                case "running":
                    status = ServiceStatus.RUNNING
                case "exited" | "created":
                    status = ServiceStatus.STOPPED
                case "restarting":
                    status = ServiceStatus.RESTARTING
                case "paused":
                    status = ServiceStatus.PAUSED
                case "dead":
                    status = ServiceStatus.ERROR
                case _:
                    status = ServiceStatus.UNKNOWN
            self._cached_status = status
            return status
        except Exception as e:
            raise ServiceError(f"Failed to get Docker service status: {e}")
        finally:
            client.close()

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
        return DockerService(slug, service_config, eigen_config)
