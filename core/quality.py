import subprocess
import time
import requests


def ping_test(interface, host="8.8.8.8"):
    """
    Test latency and packet loss
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

    interface = "wlx1cbfce2def95"

    print("Testing:", interface)

    ping = test_ping(interface)

    websites = test_websites(interface)

    score = calculate_score(
        ping,
        websites
    )

    print("\nInternet Quality Score:")
    print(score)


    sites = [

        "https://www.google.com",
        "https://github.com",
        "https://openai.com"

    ]


    results = []


    for site in sites:

        result = website_test(
            interface,
            site
        )

        results.append(result)

        print(result)



    score = calculate_score(
        ping,
        results
    )


    print("\nInternet Quality Score:")
    print(score)
