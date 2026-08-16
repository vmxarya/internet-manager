import sys
import platform


def get_platform():
    """
    Detect if running on Windows or Linux
    """
    return platform.system()


def is_windows():
    return get_platform() == "Windows"


def is_linux():
    return get_platform() == "Linux"


def get_os_info():
    return {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine()
    }
