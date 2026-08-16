import subprocess
import ipaddress


class WindowsRouterController:
    """
    Windows implementation of router control using netsh commands
    """

    def __init__(self, connections):

        self.connections = connections

    def switch(self, name):
        """
        Switch default route to specified connection using netsh
        
        Windows command format:
        netsh interface ip add route 0.0.0.0 mask 0.0.0.0 <gateway> metric <metric>
        """

        conn = self.connections[name]

        gateway = conn["gateway"]
        interface_name = conn["interface"]

        try:
            # Delete existing default routes
            subprocess.run(
                [
                    "netsh",
                    "interface",
                    "ip",
                    "delete",
                    "route",
                    "0.0.0.0",
                    "mask",
                    "0.0.0.0"
                ],
                capture_output=True,
                timeout=10
            )

            # Add new default route
            command = [
                "netsh",
                "interface",
                "ip",
                "add",
                "route",
                "0.0.0.0",
                "mask",
                "0.0.0.0",
                gateway
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                print(f"Switched to {name}")
            else:
                print(f"Failed to switch to {name}: {result.stderr}")

        except subprocess.TimeoutExpired:
            print(f"Timeout switching to {name}")
        except Exception as e:
            print(f"Error switching to {name}: {str(e)}")

    def get_route_info(self):
        """
        Get current routing information on Windows
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
            print(f"Error getting route info: {str(e)}")
            return None

    def get_network_adapters(self):
        """
        Get list of network adapters and their configuration
        """
        try:
            result = subprocess.run(
                [
                    "netsh",
                    "interface",
                    "show",
                    "interface"
                ],
                capture_output=True,
                text=True
            )

            return result.stdout

        except Exception as e:
            print(f"Error getting adapters: {str(e)}")
            return None

    def get_interface_config(self, interface_name):
        """
        Get specific interface configuration
        """
        try:
            result = subprocess.run(
                [
                    "netsh",
                    "interface",
                    "ip",
                    "show",
                    "config",
                    f"name=\"{interface_name}\""
                ],
                capture_output=True,
                text=True
            )

            return result.stdout

        except Exception as e:
            print(f"Error getting interface config: {str(e)}")
            return None
