import secrets
import sqlite3

import asyncio
import hikari
import lightbulb
import requests

from extensions.auth import plugin
from utils import config
from utils.user import User


@plugin.command
@lightbulb.command("authenticate", "Authenticate as an osu! user on Bancho")
@lightbulb.implements(lightbulb.SlashCommand)
async def authenticate(ctx: lightbulb.SlashContext) -> None:
    """Login to osu! and be connected to the bot"""
    db: sqlite3.Connection = plugin.bot.d.db

    state = secrets.token_urlsafe(16)

    auth_req = requests.Request()
    auth_req.url = "https://osu.ppy.sh/oauth/authorize"
    auth_req.params = {
        "client_id": config.CLIENT_ID,
        "redirect_uri": config.REDIRECT_URI,
        "response_type": "code",
        "scope": "identify",
        "state": state
    }
    auth_req_prepared = auth_req.prepare()

    embed = hikari.Embed(description=auth_req_prepared.url)
    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)

    user_id = None
    for _ in range(60):
        res = requests.get("http://auth:8000/user", params={"state": state})
        if res.ok:
            print("res.text:", res.text)
            user_id = res.json()["id"]
            break
        else:
            await asyncio.sleep(1)
            
    if user_id is None:
        await ctx.respond("Timed out, please try again", flags=hikari.MessageFlag.EPHEMERAL)
        return

    discord_id = int(ctx.author.id)
    bancho_id = int(user_id)
    user = User(db, discord_id, bancho_id)
    res = user.insert()
    if res is not None:
        await ctx.respond(f"Successfully authenticated as Bancho user {bancho_id}!", flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond(f"Failed to authenticate as a Bancho user.", flags=hikari.MessageFlag.EPHEMERAL)


def load(_: lightbulb.Plugin) -> None:
    pass