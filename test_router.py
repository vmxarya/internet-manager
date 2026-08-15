from core.router import RouterController


connections = {

    "TCI":{
        "gateway":"192.168.1.1",
        "interface":"wlx1cbfce2def95"
    },


    "Irancell":{
        "gateway":"192.168.2.1",
        "interface":"enp4s0"
    }

}


router = RouterController(connections)


router.switch("Irancell")
