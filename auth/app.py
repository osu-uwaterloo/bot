import requests
import valkey
from fastapi import FastAPI, HTTPException

import config

app = FastAPI()
r = valkey.Valkey(host="valkey", port=6379, db=0)

@app.get("/callback")
async def connect(code: str, state: str):
    # Get user access token
    res = requests.post("https://osu.ppy.sh/oauth/token", data={
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": config.REDIRECT_URI,
    }, headers={
        "Accept": "application/json",
    })
    res.raise_for_status()

    token_type = res.json()["token_type"]
    access_token = res.json()["access_token"]
    # Get osu! user ID
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": token_type + " " + access_token
    }
    res = requests.get("https://osu.ppy.sh/api/v2/me/", headers=headers)
    res.raise_for_status()

    user_id = res.json()["id"]
    r.set(state, user_id)
    return {"message": f"Successfully authenticated as Bancho user {user_id}"}

@app.get("/user")
async def user(state: str):
    user_id = r.get(state)
    if user_id is None:
        raise HTTPException(404, detail="A bancho user with the given code does not exist")
    return {"id": user_id}
