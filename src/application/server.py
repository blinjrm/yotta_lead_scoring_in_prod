import datetime
from typing import List

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.domain.lead import Lead
from src.infrastructure.config.config import config


lead = Lead()
app = FastAPI(
    title="Lead scoring Yotta",
    description="This API calls a lead scoring model deployed on GKE. ",
    version="1.0.0",
)

PORT = config["api"]["port"]
HOST = config["api"]["host"]

app.add_middleware(
    CORSMiddleware, allow_credentials=True, allow_methods=["POST", "GET"], allow_headers=["*"]
)


@app.post("/")
def get_prediction(leads: List[dict]):
    predictions = []

    for l in leads:
        prediction = lead.predict(l)
        predictions.append(prediction)

    return predictions


if __name__ == "__main__":
    print("starting API", datetime.datetime.now())
    uvicorn.run(app, host=HOST, port=PORT)
