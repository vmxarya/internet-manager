from fastapi import FastAPI
from core.controller import InternetController


app = FastAPI(
    title="Internet Manager"
)


controller = InternetController()


@app.get("/")
def home():
    return {
        "message": "Internet Manager API running"
    }


@app.get("/status")
def status():

    return {
        "mode": controller.config["mode"],
        "active": controller.config["active"],
        "connections": controller.config["connections"]
    }
