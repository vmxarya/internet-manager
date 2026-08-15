import psutil
import socket
import subprocess


def get_interfaces():
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
    result = subprocess.run(
        ["ip", "route"],
        capture_output=True,
        text=True
    )

    return result.stdout


if __name__ == "__main__":

    print("\n=== Network Interfaces ===")

    interfaces = get_interfaces()

    for name, info in interfaces.items():
        print(info)


    print("\n=== Routing Table ===")

    print(get_routes())
