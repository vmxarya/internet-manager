import subprocess
import time
import requests


def ping_test_windows(interface=None, host="8.8.8.8"):
    """
    Windows version of ping test.
    Note: Windows doesn't support binding ping to a specific interface
    as easily as Linux. This is a limitation on Windows.
    """
    
    result = subprocess.run(
        [
            "ping",
            "-n",  # Windows uses -n instead of -c
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

        if "% loss" in line:
            loss_str = line.split("% loss")[0].strip().split()[-1]
            loss = int(loss_str)

        if "Average = " in line:
            latency = float(
                line.split("Average = ")[1]
                .replace("ms", "")
            )

    return {
        "online": True,
        "latency": latency,
        "loss": loss
    }


def website_test_windows(url):
    """
    Test website connectivity and response time
    """
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
    """
    Calculate internet quality score (platform-independent)
    """
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

        elif site["time"] and site["time"] > 2:
            slow += 1

    score -= failed * 30
    score -= slow * 10

    if score < 0:
        score = 0

    return round(score)


def check_quality_windows(interface=None):
    """
    Windows version of quality checking
    Note: Windows doesn't support interface-specific pings easily,
    so we test the default route
    """

    ping = ping_test_windows()

    urls = [
        "https://www.google.com",
        "https://github.com",
        "https://openai.com"
    ]

    websites = []

    for url in urls:
        websites.append(
            website_test_windows(url)
        )

    score = calculate_score(
        ping,
        websites
    )

    return score


if __name__ == "__main__":

    print("Testing Windows quality checking...")

    ping = ping_test_windows()
    print("Ping result:", ping)

    websites = []
    urls = [
        "https://www.google.com",
        "https://github.com",
        "https://openai.com"
    ]

    for url in urls:
        result = website_test_windows(url)
        websites.append(result)
        print(result)

    score = calculate_score(ping, websites)

    print("\nInternet Quality Score:")
    print(score)
