import time

from core.decision import DecisionEngine
from core.router import RouterController
from core.quality import check_quality

connections = {

    "TCI": {
        "gateway": "192.168.1.1",
        "interface": "wlx1cbfce2def95"
    },


    "Irancell": {
        "gateway": "192.168.2.1",
        "interface": "enp4s0"
    }

}


engine = DecisionEngine(
    "TCI",
    "Irancell"
)


router = RouterController(connections)



while True:

    print("\nChecking internet quality...")


    # temporary test scores
    # later these come from quality.py

    scores = {

    "TCI": check_quality(
          "wlx1cbfce2def95"
     )["score"],

     "Irancell": check_quality(
          "enp4s0"
     )["score"]
    }


    active = engine.decide(scores)


    print(
        "Current ISP:",
        active
    )


    time.sleep(10)
