import sqlite3

import lightbulb
import hikari
import ossapi

from extensions.auth import plugin as plugin_auth
from extensions.woc import plugin as plugin_woc
from utils import config
from utils.google import SheetsAPI
from utils.user import User

# Initialize DB
db = sqlite3.connect("/home/bot/db/users.db")
init_cur = db.cursor()
init_cur.execute("CREATE TABLE IF NOT EXISTS users (discord_id INTEGER PRIMARY KEY, bancho_id INTEGER);")
db.commit()
init_cur.close()

# Get osu! API client
osu_api = ossapi.Ossapi(config.CLIENT_ID, config.CLIENT_SECRET)

# Get Google Sheets API client
sheets_api = SheetsAPI(config.GOOGLE_SHEET_ID, config.GOOGLE_SHEET_NAME, config.GOOGLE_SHEET_CELL_RANGE, config.GOOGLE_API_KEY)

# SQLite db connection
user_util = User(db)

# Setup bot
bot = lightbulb.BotApp(
    token=config.DISCORD_TOKEN,
    default_enabled_guilds=config.ALLOWED_SERVERS,
)
bot.d.osu_api = osu_api
bot.d.sheets_api = sheets_api
bot.d.user_util = user_util
bot.d.db = db

bot.load_extensions_from("./extensions", recursive=True)
bot.add_plugin(plugin_auth)
bot.add_plugin(plugin_woc)


@bot.command
@lightbulb.command("ping", "test")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.SlashContext) -> None:
    """Ping the bot"""
    embed = hikari.Embed(description="pinged!")
    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


@bot.command
@lightbulb.command("profile", "View your profile")
@lightbulb.implements(lightbulb.SlashCommand)
async def profile(ctx: lightbulb.SlashContext) -> None:
    """View your profile"""
    bancho_id = user_util.get_bancho_user_id(ctx)
    user = osu_api.user(bancho_id)
    await ctx.respond(f"You are {user.username}")


# Start running bot (blocking call)
bot.run()