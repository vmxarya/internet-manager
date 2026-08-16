import platform
import subprocess
import time

import requests


def _is_windows():
    return platform.system() == "Windows"


def ping_test(interface, host="8.8.8.8"):
    """Test latency and packet loss. Cross-platform."""

    if _is_windows():
        command = ["ping", "-n", "4", host]
    else:
        command = ["ping", "-I", interface, "-c", "4", host]

    result = subprocess.run(
        command,
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

        if "packet loss" in line or "Packets:" in line:
            try:
                loss = int(
                    line.split("%")[0]
                    .split()[-1]
                )
            except (ValueError, IndexError):
                loss = 0

        if "avg" in line or "Minimum" in line:
            try:
                if "=" in line:
                    latency = float(
                        line.split("=")[1]
                        .split("/")[1]
                    )
                else:
                    parts = [p for p in line.split() if p.replace(".", "").replace("-", "").isdigit()]
                    if parts:
                        latency = float(parts[2]) if len(parts) >= 3 else float(parts[0])
            except (ValueError, IndexError):
                latency = None

    return {
        "online": True,
        "latency": latency,
        "loss": loss or 0
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

    except Exception:

        return {
            "url": url,
            "status": "failed",
            "time": None
        }


def calculate_score(ping, websites):

    score = 100

    if ping["latency"]:

        if ping["latency"] > 100:
            score -= 10

        if ping["latency"] > 200:
            score -= 20

    if ping["online"] and ping["loss"]:

        score -= ping["loss"] * 0.3

    failed = 0
    slow = 0

    for site in websites:

        if site["status"] == "failed":
            failed += 1

        elif site["time"] and site["time"] > 2:
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

    return {
        "score": score,
        "ping": ping
    }


if __name__ == "__main__":

    interface = "wlx1cbfce2def95"

    print("Testing:", interface)

    result = check_quality(interface)

    print("\nInternet Quality Score:")
    print(result["score"])
    print("Ping:", result["ping"])
