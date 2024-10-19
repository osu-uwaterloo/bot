import hikari
import lightbulb

from extensions.woc import plugin
@plugin.command
@lightbulb.option("user", "User to view on the Wo!C leaderboard", required=False, default=None, type=hikari.Member)
@lightbulb.command("woc-leaderboard", "View the Waterloo osu! Cup leaderboard")
@lightbulb.implements(lightbulb.SlashCommand)
async def woc_leaderboard(ctx: lightbulb.SlashContext) -> None:
    """View the Wo!C leaderboard"""
    embed = hikari.Embed(title="Waterloo osu! Cup Leaderboard")
    await ctx.respond(embed=embed)


def load(_: lightbulb.Plugin) -> None:
    pass