class HLBoxError(Exception):
    """The base class for custom exceptions raised by hlbox."""


class DockerError(HLBoxError):
    """An error occurred with the underlying docker system."""
