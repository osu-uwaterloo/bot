import sqlite3

from extensions.auth import plugin
from utils import config
from utils.auth_session import AuthSession

import hikari
import lightbulb
from exchangelib import Credentials, Account, Message, DELEGATE

from datetime import timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
    
    db: sqlite3.Connection = plugin.bot.d.db

    sess = AuthSession(
        db,
        candidate_email,
        15,
        timedelta(minutes=15)
    )

    code = sess.prepare()

    msg = MIMEMultipart()
    msg["From"] = config.EMAIL_ADDRESS
    msg["To"] = candidate_email
    msg["Subject"] = "osu!UWaterloo email verification"

    body = f"Your osu!UWaterloo email verification code is {code}"
    msg.attach(MIMEText(body, "plain"))

    port = 587
    try:
        with smtplib.SMTP(config.EMAIL_SERVER, port) as server:
            server.starttls()
            server.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
            sess.save()
            server.sendmail(config.EMAIL_ADDRESS, candidate_email, msg.as_string())
    except Exception as e:
        print(f"ERROR OCCURRED DURING EMAIL SEND: {e}")
        await ctx.respond("Something went wrong. Check logs.")
        return
    
    await ctx.respond("End of test.")



def load(_: lightbulb.Plugin) -> None:
    pass
