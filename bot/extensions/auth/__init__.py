import lightbulb

plugin = lightbulb.Plugin("Authentication")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)