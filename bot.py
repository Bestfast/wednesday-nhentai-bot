import botogram, os

bot = botogram.create(os.environ['BOT'])
bot.about = "A nHentai's (unofficial) bot"
bot.owner = "@Bestfast"

bot.run()