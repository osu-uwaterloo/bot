import sqlite3

import hikari.components
import miru.text_input

from extensions.auth import plugin
from utils import config
from utils.auth_session import AuthSession
from utils.exceptions import MaxSessionsExceededError

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
        res = AuthSession.validate(self.code_input.value, ctx.member.id, plugin.bot.d.db)
        if not res["success"]:
            await ctx.respond(f"Verification failed. Reason: {res["reason"]}", flags=hikari.MessageFlag.EPHEMERAL)
            return
        
        if config.CWS_ROLE_ID != -1:
            await ctx.member.add_role(config.CWS_ROLE_ID)
        await ctx.respond("Verification successful!", flags=hikari.MessageFlag.EPHEMERAL)


@plugin.command
@lightbulb.option(name="email", required=True, description="Your UWaterloo email address")
@lightbulb.command("verify", "Authenticate as a current waterloo student")
@lightbulb.implements(lightbulb.SlashCommand)
async def verify(ctx: lightbulb.SlashContext):

    if (config.CWS_ROLE_ID != -1) and (config.CWS_ROLE_ID in ctx.member.role_ids):
        await ctx.respond("You are already verified!", flags=hikari.MessageFlag.EPHEMERAL)
        return
    
    
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
        ctx.author.id,
        candidate_email,
        config.AUTH_CODE_LEN,
        timedelta(minutes=config.AUTH_CODE_DURATION)
    )

    try:
        code = sess.prepare()
    except MaxSessionsExceededError:
        await ctx.respond(
            "You are making too many verification requests too quickly! Please try again after a few minutes.",
            flags=hikari.MessageFlag.EPHEMERAL
        )
        return

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
