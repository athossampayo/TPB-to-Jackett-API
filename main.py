from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

import get_torrents

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
    "http://127.0.0.1",
]
origins = ["*"]
@app.get("/api/v2.0/indexers/all/results")
def api_endpoint(request: Request):
    params = request.query_params
    torrents = get_torrents.get(params['Query'] + ' ' + params['year'])
    return torrents 

@app.get("/healthcheck")
def read_root():
    return {"status": "ok"}

app = CORSMiddleware(
    app=app,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)