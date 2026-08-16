import psutil
import socket
import subprocess
import platform

if platform.system() == "Windows":
    from .network_windows import (
        get_interfaces_windows,
        get_routes_windows,
        get_default_gateway_windows,
        get_ip_config
    )


def get_interfaces():
    """
    Get network interfaces - works cross-platform
    """
    if platform.system() == "Windows":
        return get_interfaces_windows()
    
    # Linux implementation
    interfaces = {}

    for name, addresses in psutil.net_if_addrs().items():
        info = {
            "interface": name,
            "ipv4": None,
            "mac": None
        }

        for addr in addresses:
            if addr.family == socket.AF_INET:
                info["ipv4"] = addr.address

            elif addr.family == psutil.AF_LINK:
                info["mac"] = addr.address

        interfaces[name] = info

    return interfaces


def get_routes():
    """
    Get routing table - platform specific
    """
    if platform.system() == "Windows":
        return get_routes_windows()
    
    # Linux implementation
    result = subprocess.run(
        ["ip", "route"],
        capture_output=True,
        text=True
    )

    return result.stdout


def get_default_gateway():
    """
    Get default gateway - platform specific
    """
    if platform.system() == "Windows":
        return get_default_gateway_windows()
    
    # Linux implementation
    result = subprocess.run(
        ["ip", "route", "show"],
        capture_output=True,
        text=True
    )

    output = result.stdout

    for line in output.split("\n"):
        if line.startswith("default"):
            parts = line.split()
            if len(parts) > 2:
                return parts[2]

    return None


if __name__ == "__main__":

    print("\n=== Network Interfaces ===")

    interfaces = get_interfaces()

    for name, info in interfaces.items():
        print(info)


    print("\n=== Routing Table ===")

    print(get_routes())

    print("\n=== Default Gateway ===")

    print(get_default_gateway())
