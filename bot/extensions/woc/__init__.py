import lightbulb

plugin = lightbulb.Plugin("WaterlooOsuCup")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)