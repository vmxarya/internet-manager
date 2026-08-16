import subprocess
import time
import requests
import platform

# Import platform-specific implementations
if platform.system() == "Windows":
    from .quality_windows import (
        ping_test_windows as ping_test,
        website_test_windows as website_test,
        calculate_score,
        check_quality_windows as check_quality
    )
else:
    # Linux implementation
    def ping_test(interface, host="8.8.8.8"):
        """
        Test latency and packet loss (Linux version)
        """

        result = subprocess.run(
            [
                "ping",
                "-I",
                interface,
                "-c",
                "4",
                host
            ],
            capture_output=True,
            text=True
        )

        output = result.stdout

        if result.returncode != 0:
            return {
                "online": False,
                "latency": None,
                "loss": 100
            }

        latency = None
        loss = None

        for line in output.split("\n"):

            if "packet loss" in line:
                loss = int(
                    line.split("%")[0]
                    .split()[-1]
                )

            if "avg" in line:
                latency = float(
                    line.split("=")[1]
                    .split("/")[1]
                )

        return {
            "online": True,
            "latency": latency,
            "loss": loss
        }

    def website_test(interface, url):

        start = time.time()

        try:

            response = requests.get(
                url,
                timeout=5
            )

            total = time.time() - start

            return {
                "url": url,
                "status": response.status_code,
                "time": round(total, 3)
            }

        except:

            return {
                "url": url,
                "status": "failed",
                "time": None
            }

    def calculate_score(ping, websites):

        score = 100

        # Ping is useful but not critical
        if ping["latency"]:

            if ping["latency"] > 100:
                score -= 10

            if ping["latency"] > 200:
                score -= 20

        # Packet loss matters only if ping works
        if ping["online"] and ping["loss"]:

            score -= ping["loss"] * 0.3

        # Website quality
        failed = 0
        slow = 0

        for site in websites:

            if site["status"] == "failed":
                failed += 1

            elif site["time"] > 2:
                slow += 1

        score -= failed * 30
        score -= slow * 10

        if score < 0:
            score = 0

        return round(score)

    def check_quality(interface):

        ping = ping_test(interface)

        urls = [
            "https://www.google.com",
            "https://github.com",
            "https://openai.com"
        ]

        websites = []

        for url in urls:
            websites.append(
                website_test(interface, url)
            )

        score = calculate_score(
            ping,
            websites
        )

        return score


if __name__ == "__main__":

    if platform.system() == "Windows":
        print("Testing quality on Windows...")
        score = check_quality()
    else:
        interface = "wlx1cbfce2def95"
        print("Testing:", interface)
        score = check_quality(interface)

    print("\nInternet Quality Score:")
    print(score)
