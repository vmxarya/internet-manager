import platform
import subprocess


class RouterController:

    def __init__(self, connections):

        self.connections = connections

    def switch(self, name):

        conn = self.connections[name]

        gateway = conn["gateway"]
        interface = conn["interface"]

        if platform.system() == "Windows":
            command = [
                "route",
                "DELETE",
                "0.0.0.0"
            ]
            subprocess.run(command, capture_output=True)

            command = [
                "route",
                "ADD",
                "0.0.0.0",
                "MASK",
                "0.0.0.0",
                gateway,
                "METRIC",
                "1"
            ]
        else:
            command = [
                "ip",
                "route",
                "replace",
                "default",
                "via",
                gateway,
                "dev",
                interface
            ]

        subprocess.run(command, capture_output=True)

        print(
            f"Switched to {name}"
        )

    def set_primary(self, name):
        """Convenience alias used by the GUI."""
        self.switch(name)
