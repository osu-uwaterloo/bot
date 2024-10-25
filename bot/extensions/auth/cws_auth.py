import sqlite3

from extensions.auth import plugin
from utils import config
from utils.auth_session import AuthSession

import hikari
import lightbulb
from exchangelib import Credentials, Account, Message, DELEGATE

from datetime import timedelta

@plugin.command
@lightbulb.option(name="email", required=True, description="Your UWaterloo email address")
@lightbulb.command("verify", "Authenticate as a current waterloo student")
@lightbulb.implements(lightbulb.SlashCommand)
async def verify(ctx: lightbulb.SlashContext):
    """
    This is just a test implementation to see if email works.
    It does not support actual code validation yet.

    Note: The actual email part isn't working yet.
    """
    options = ctx.options.items()
    
    candidate_email: str = None
    for opt in options:
        if opt[0] == "email":
            candidate_email = opt[1]
            break
    
    if not candidate_email.endswith("@uwaterloo.ca"):
        await ctx.respond("You can only verify with a uwaterloo email address.", flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    await ctx.respond("This command isn't ready yet XD") # REMOVE THESE TWO LINES WHEN FIXED
    return
    
    db: sqlite3.Connection = plugin.bot.d.db

    credentials = Credentials(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
    account = Account(
        config.EMAIL_ADDRESS,
        credentials=credentials,
        autodiscover=True,
        access_type=DELEGATE
    )

    sess = AuthSession(
        db,
        candidate_email,
        15,
        timedelta(minutes=15)
    )

    code = sess.prepare()

    message = Message(
        account=account,
        folder=account.sent,
        subject="osu!UWaterloo Verification Code",
        body=f"Your osu!Uwaterloo Verification Code is {code}",
        to_recipients=[candidate_email]
    )

    message.send()
    sess.save()

    await ctx.respond("End of test", flags=hikari.MessageFlag.EPHEMERAL)


def load(_: lightbulb.Plugin) -> None:
    pass
