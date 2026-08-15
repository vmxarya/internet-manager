import subprocess


class RouterController:


    def __init__(self, connections):

        self.connections = connections



    def switch(self, name):

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
