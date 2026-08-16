import subprocess
import platform

if platform.system() == "Windows":
    from .router_windows import WindowsRouterController

class RouterController:

    def __init__(self, connections):

        self.connections = connections
        self.platform = platform.system()
        
        if self.platform == "Windows":
            self.controller = WindowsRouterController(connections)

    def switch(self, name):

        if self.platform == "Windows":
            self.controller.switch(name)
        else:
            # Linux implementation
            conn = self.connections[name]

            gateway = conn["gateway"]
            interface = conn["interface"]

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

            subprocess.run(command)

            print(
                f"Switched to {name}"
            )

    def get_platform(self):
        return self.platform

