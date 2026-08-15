import subprocess
import time


def ping_test(host="8.8.8.8", count=3):

    result = subprocess.run(
        [
            "ping",
            "-c",
            str(count),
            host
        ],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return True

    return False



def check_connection(name, interface):

    result = subprocess.run(
        [
            "ping",
            "-I",
            interface,
            "-c",
            "3",
            "8.8.8.8"
        ],
        capture_output=True,
        text=True
    )


    if result.returncode == 0:
        return {
            "name": name,
            "status": "online"
        }

    else:
        return {
            "name": name,
            "status": "offline"
        }



if __name__ == "__main__":

    print(
        check_connection(
            "TCI",
            "wlx1cbfce2def95"
        )
    )


    print(
        check_connection(
            "Irancell",
            "enp4s0"
        )
    )
