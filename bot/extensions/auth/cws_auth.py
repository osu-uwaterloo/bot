import sqlite3

import hikari.components
import miru.text_input

from extensions.auth import plugin
from utils import config
from utils.auth_session import AuthSession

import hikari
import lightbulb
import miru

from datetime import timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class CodeInputModal(miru.Modal, title="osu!UWaterloo Student Email Verification"):

    code_input = miru.TextInput(
        label = "Verification Code",
        placeholder="Enter code here...",
        required=True,
        style=hikari.TextInputStyle.SHORT
    )

    async def callback(self, ctx: miru.ModalContext):
        res = AuthSession.validate(self.code_input.value, plugin.bot.d.db)
        if not res["success"]:
            await ctx.respond(f"Verification failed. Reason: {res["reason"]}", flags=hikari.MessageFlag.EPHEMERAL)
            return
        
        await ctx.respond("Verification successful!", flags=hikari.MessageFlag.EPHEMERAL)


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

    # need to check if user already has the cws role
    # ...
    
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
    
    client: miru.Client = plugin.bot.d.miru
    modal = CodeInputModal()
    builder = modal.build_response(client)

    await builder.create_modal_response(ctx.interaction)
    client.start_modal(modal)

        


def load(_: lightbulb.Plugin) -> None:
    pass
