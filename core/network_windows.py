import psutil
import socket
import subprocess
import re


def get_interfaces_windows():
    """
    Get network interfaces info on Windows
    Uses psutil which works cross-platform
    """
    interfaces = {}

    for name, addresses in psutil.net_if_addrs().items():
        info = {
            "interface": name,
            "ipv4": None,
            "ipv6": None,
            "mac": None,
            "status": None
        }

        for addr in addresses:
            if addr.family == socket.AF_INET:
                info["ipv4"] = addr.address
            elif addr.family == socket.AF_INET6:
                info["ipv6"] = addr.address
            elif addr.family == psutil.AF_LINK:
                info["mac"] = addr.address

        # Get interface status
        try:
            stats = psutil.net_if_stats()[name]
            info["status"] = "up" if stats.isup else "down"
        except:
            pass

        interfaces[name] = info

    return interfaces


def get_routes_windows():
    """
    Get routing table on Windows using netsh
    """
    try:
        result = subprocess.run(
            [
                "netsh",
                "interface",
                "ip",
                "show",
                "route"
            ],
            capture_output=True,
            text=True
        )

        return result.stdout

    except Exception as e:
        print(f"Error getting routes: {str(e)}")
        return None


def get_default_gateway_windows():
    """
    Get default gateway on Windows
    """
    try:
        # Use ipconfig or netsh to get default gateway
        result = subprocess.run(
            [
                "netsh",
                "interface",
                "ip",
                "show",
                "route"
            ],
            capture_output=True,
            text=True
        )

        output = result.stdout

        # Parse output to find default gateway
        for line in output.split("\n"):
            if "0.0.0.0" in line and "0.0.0.0" in line.split():
                parts = line.split()
                if len(parts) > 3:
                    return parts[3]  # Gateway is typically at index 3

        return None

    except Exception as e:
        print(f"Error getting default gateway: {str(e)}")
        return None


def get_interface_by_gateway_windows(gateway_ip):
    """
    Find interface that connects to a specific gateway
    """
    try:
        result = subprocess.run(
            [
                "netsh",
                "interface",
                "ip",
                "show",
                "route"
            ],
            capture_output=True,
            text=True
        )

        output = result.stdout

        for line in output.split("\n"):
            if gateway_ip in line:
                # Parse to find interface
                parts = line.split()
                if len(parts) >= 4:
                    return parts[4]  # Interface typically at index 4

        return None

    except Exception as e:
        print(f"Error finding interface: {str(e)}")
        return None


def get_ip_config():
    """
    Get detailed IP configuration on Windows
    """
    try:
        result = subprocess.run(
            [
                "ipconfig"
            ],
            capture_output=True,
            text=True
        )

        return result.stdout

    except Exception as e:
        print(f"Error getting IP config: {str(e)}")
        return None


def get_adapter_status():
    """
    Get status of all network adapters
    """
    interfaces = get_interfaces_windows()
    status = {}

    for name, info in interfaces.items():
        status[name] = {
            "name": name,
            "ipv4": info["ipv4"],
            "mac": info["mac"],
            "status": info["status"]
        }

    return status


if __name__ == "__main__":

    print("\n=== Windows Network Interfaces ===")

    interfaces = get_interfaces_windows()

    for name, info in interfaces.items():
        print(f"\n{name}:")
        print(f"  IPv4: {info['ipv4']}")
        print(f"  IPv6: {info['ipv6']}")
        print(f"  MAC: {info['mac']}")
        print(f"  Status: {info['status']}")

    print("\n=== Windows Routing Table ===")

    print(get_routes_windows())

    print("\n=== Default Gateway ===")

    print(get_default_gateway_windows())

    print("\n=== IP Configuration ===")

    print(get_ip_config())
