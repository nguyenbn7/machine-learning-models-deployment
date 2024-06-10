from json import load
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from classification.urls import router as classification_router

with open(Path(__file__).parent.joinpath("settings.json"), mode="r") as json_file:
    config = {**load(json_file)}

DEBUG = config["DEBUG"]
ALLOW_ORIGINS = ["*"] if DEBUG else config["ALLOW_ORIGINS"]
ALLOW_METHODS = ["*"] if DEBUG else config["ALLOW_METHODS"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_methods=ALLOW_METHODS,
)

app.include_router(classification_router, prefix="/services")
