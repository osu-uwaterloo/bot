import hikari
import lightbulb
from ossapi import Ossapi

from extensions.woc import plugin
from utils.exceptions import UserNotConnectedError
from utils.user import User
from utils.google import SheetsAPI


@plugin.command
@lightbulb.option("user", "User to view Wo!C data for", required=False, default=None, type=hikari.Member)
@lightbulb.command("woc", "View your Waterloo osu! Cup profile")
@lightbulb.implements(lightbulb.SlashCommand)
async def woc_profile(ctx: lightbulb.SlashContext) -> None:
    """View your Wo!C profile"""
    user_util: User = plugin.bot.d.user_util
    osu_api: Ossapi = plugin.bot.d.osu_api
    sheets_api: SheetsAPI = plugin.bot.d.sheets_api
    
    user: hikari.Member = ctx.options.user
    if user is None:
        bancho_id = user_util.get_bancho_user_id(ctx)
    else:
        raise UserNotConnectedError

    osu_user = osu_api.user(bancho_id)
    woc_user_data = user_util.get_woc_user(bancho_id, sheets_api)
    results = [0, 0, 0, 0]
    if woc_user_data is None:
        await ctx.respond("Bad")
        return

    for column, value in woc_user_data.items():
        if column.startswith("WoC") and value == "1ST PLACE":
            results[0] += 1
            results[3] += 1
        if column.startswith("WoC") and value == "2ND PLACE":
            results[1] += 1
            results[3] += 1
        if column.startswith("WoC") and value == "3RD PLACE":
            results[2] += 1
            results[3] += 1
        if column.startswith("WoC") and value == "✔":
            results[3] += 1

    if results[3] <= 2:
        title = "Rookie"
    elif results[3] <= 4:
        title = "Amateur"
    elif results[3] <= 6:
        title = "Pro"
    elif results[3] <= 9:
        title = "Veteran"
    else:
        title = "Legend"

    embed = hikari.Embed()
    embed.set_author(name=f"{osu_user.username} - Wo!C Performance")
    embed.set_thumbnail(osu_user.avatar_url)
    embed.add_field("1ST PLACE", str(results[0]), inline=True)
    embed.add_field("2ND PLACE", str(results[1]), inline=True)
    embed.add_field("3RD PLACE", str(results[2]), inline=True)
    embed.set_footer(f"Wo!C {title} - {results[3]} tournaments played")
    await ctx.respond(embed=embed)


@woc_profile.set_error_handler
async def woc_profile_error_handler(event: lightbulb.CommandErrorEvent) -> None:
    exception = event.exception.__cause__ or event.exception
    if isinstance(exception, UserNotConnectedError):
        await event.context.respond("No valid osu! account linked for the user.")


def load(_: lightbulb.Plugin) -> None:
    pass