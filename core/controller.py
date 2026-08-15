import json
import os


CONFIG_FILE = "data/config.json"


class InternetController:

    def __init__(self):
        self.config = self.load_config()


    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            raise FileNotFoundError(CONFIG_FILE)

        with open(CONFIG_FILE, "r") as file:
            return json.load(file)


    def status(self):

        print("\n=== Internet Manager ===")

        print("Mode:",
              self.config["mode"])

        print("Active:",
              self.config["active"])

        print("\nConnections:")

        for connection in self.config["connections"]:
            print(
                f"- {connection['name']} "
                f"({connection['interface']}) "
                f"priority={connection['priority']}"
            )


if __name__ == "__main__":

    controller = InternetController()

    controller.status()
