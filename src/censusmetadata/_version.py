from importlib.metadata import version
from importlib.metadata import PackageNotFoundError


def _pkg_name() -> str:
    """Retrieve package name from metadata."""
    return (__package__ or __name__).split(".")[0]


def get_package_version() -> str:
    """
    Retrieve the installed package version, with a fallback 
    for local development.
    """
    try:
        return version(_pkg_name())
    except PackageNotFoundError:
        return "0.0.0+local"
