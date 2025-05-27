from abc import ABC, abstractmethod
from .config import ServiceConfig, EigenConfig
from ..models import ServiceStatus
import time
from pathlib import Path
from pydantic import BaseModel, ValidationError

class ServiceError(Exception):
    pass

class ServiceBusyError(ServiceError):
    """
    Exception raised when a service is busy and cannot be started, stopped, or restarted.
    """
    def __init__(self, message: str = "Service is busy and cannot be modified."):
        super().__init__(message)

class ServiceLock:
    """
    A lock class to ensure that only one operation can be performed on a service at a time.
    """
    def __init__(self, slug: str, lock_dir: Path):
        """
        Initialize the lock with a service slug.

        :param slug: The unique identifier for the service.
        """
        self.slug = slug
        self.filepath = lock_dir / f"{slug}.lock"

        self._last_release = 0
        self._next_delay = 0

    def is_locked(self) -> bool:
        """
        Check if the lock file exists.

        :return: True if the lock file exists, False otherwise.
        """
        return self.filepath.exists() or (time.time() - self._last_release < self._next_delay)

    def acquire(self):
        """
        Acquire the lock for the service.

        :raises ServiceBusyError: If the lock file already exists.
        """
        self._next_delay = 0
        while self.is_locked():
            time.sleep(.1)
        self.filepath.touch()

    def add_delay(self, delay):
        """
        Add a delay before releasing the lock.

        :param delay: The delay in seconds to add.
        """
        self._next_delay += delay

    def release(self):
        """
        Release the lock for the service.

        :raises ServiceError: If the lock file does not exist.
        """
        if self.filepath.exists():
            self.filepath.unlink()
            self._last_release = time.time()
        else:
            raise ServiceError(f"Lock file for service '{self.slug}' does not exist.")

    def __enter__(self):
        """
        Enter the context manager, acquiring the lock.

        :return: The ServiceLock instance.
        :raises ServiceBusyError: If the lock cannot be acquired.
        """
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager, releasing the lock.

        :param exc_type: The type of exception raised, if any.
        :param exc_value: The value of the exception raised, if any.
        :param traceback: The traceback object, if any.
        :return: False to propagate exceptions, True to suppress them.
        :raises ServiceError: If there is an error releasing the lock.
        """
        self.release()
        return False  # Do not suppress exceptions



class Service(ABC):
    """
    Abstract base class for a service.
    """
    @staticmethod
    def ensure_lock(func):
        """
        Decorator to ensure that a lock is acquired before executing the function.

        :param func: The function to be decorated.
        :return: The wrapped function.
        """
        def wrapper(self, *args, **kwargs):
            if not self.lock.is_locked():
                raise ServiceBusyError(f"Lock required to perform action on '{self.slug}'.")
            return func(self, *args, **kwargs)
        return wrapper

    def __init__(self, slug: str, config: ServiceConfig, eigen_config: EigenConfig, provider_model: type[BaseModel]):
        """
        Initialize the service with a model.

        :param slug: The unique identifier for the service.
        :param config: An instance of ServiceModel containing service details.
        :param eigen_config: An Eigen configuration.
        :param provider_model: The model class for the provider data.
        :raises ValidationError: If the data does not match the provider model.
        """
        self.slug = slug
        self.lock = ServiceLock(slug, eigen_config.services.lock_dir)
        self._config = config
        self._config.provider.options = provider_model(**config.provider.options)

    def is_busy(self) -> bool:
        """
        Check if the service is busy.

        :return: True if the service is busy, False otherwise.
        """
        return self.lock.is_locked()

    @abstractmethod
    def is_installed(self) -> bool:
        """
        Check if the service is installed.

        :return: True if the service is installed, False otherwise.
        """
        ...

    @ensure_lock
    def install(self) -> None:
        """
        Install the service.

        :raises ServiceError: if the service cannot be installed.
        """
        if self.is_installed():
            raise ServiceError(f"Service '{self.slug}' is already installed.")
        self._install()

    @abstractmethod
    def _install(self) -> None:
        """
        Install the service without acquiring the lock.

        This method should be implemented by subclasses to perform the actual installation.
        """
        ...

    @ensure_lock
    def uninstall(self) -> None:
        """
        Uninstall the service.

        :raises ServiceError: if the service cannot be uninstalled.
        """
        if not self.is_installed():
            raise ServiceError(f"Service '{self.slug}' is not installed.")
        self._uninstall()

    @abstractmethod
    def _uninstall(self) -> None:
        """
        Uninstall the service.

        :raises ServiceError: if the service cannot be uninstalled.
        """
        ...

    @property
    def config(self) -> ServiceConfig:
        """
        Get the service configuration.

        :return: The service configuration.
        """
        return self._config

    @ensure_lock
    def start(self) -> None:
        """
        Start the service.

        :raises ServiceError: if the service cannot be started.
        """
        self._start()

    @abstractmethod
    def _start(self) -> None:
        """
        Start the service without acquiring the lock.

        This method should be implemented by subclasses to perform the actual start operation.
        """
        ...

    @ensure_lock
    def stop(self) -> None:
        """
        Stop the service.

        :raises ServiceError: if the service cannot be stopped.
        """
        self._stop()

    @abstractmethod
    def _stop(self) -> None:
        """
        Stop the service without acquiring the lock.

        This method should be implemented by subclasses to perform the actual stop operation.
        """
        ...

    @ensure_lock
    def restart(self) -> None:
        """
        Restart the service.

        :raises ServiceError: if the service cannot be restarted.
        """
        self._restart()

    @abstractmethod
    def _restart(self) -> None:
        """
        Restart the service without acquiring the lock.

        This method should be implemented by subclasses to perform the actual restart operation.
        """
        ...

    @property
    def status(self) -> ServiceStatus:
        """
        Get the status of the service.

        :return: The status of the service.
        :raises ServiceError: if the status cannot be retrieved.
        """
        return self._status()

    @abstractmethod
    def _status(self) -> ServiceStatus:
        """
        Get the status of the service without acquiring the lock.

        This method should be implemented by subclasses to perform the actual status retrieval.
        """
        ...
