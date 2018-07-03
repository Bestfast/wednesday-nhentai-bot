import botogram, os, sqlite3, gettext

bot = botogram.create(os.environ['BOT'])
bot.about = "A nHentai's (unofficial) bot"
bot.owner = "@Bestfast"

@bot.command("start")
def start_command(chat, message, args):
    
    """Start the bot"""
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    try:
        c.execute("SELECT user_id FROM users WHERE user_id = ?", (message.sender.id,))
    
    except sqlite3.OperationalError:
        return lang(chat, message)
    
    data = c.fetchall()
    
    if not data:

        conn.close()
        return lang(chat, message)
    else:
        _ = getlang(message.sender.id)
        btns = botogram.Buttons()
        btns[0].url(_("Open a pull request"), "https://github.com/Bestfast/wednesday-nhentai-bot/pulls")
        btns[1].url(_("Enter in the official bot's group"), "https://t.me/joinchat/Fb98J0njHKRnhj3LvF0m6A")
        btns[2].url(_("Contact the delevoper"), "https://t.me/Bestfast")
        
        chat.send(_("Hi! This bot is in development. if you want to help, you can open a pull request in the GitHub's repo."), attach=btns)


def getlang(user_id):

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
    l = [c.fetchone()[0]]
    lang = gettext.translation('base', localedir='locales', languages=l)
    lang.install()
    conn.close()
    return lang.gettext


@bot.command("lang")
def lang(chat, message):

    btns = botogram.Buttons()
    btns[0].callback("IT", "lang_it")
    btns[1].callback("EN", "lang_en")

    chat.send("Select the language that you want to use with the bot\n\nYour user_id will be stored in the database.", attach=btns)


@bot.callback("lang_it")
def lang_it(query, chat, message):

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    try:
        c.execute('DELETE FROM users WHERE user_id = ?', (query.sender.id,))
    except sqlite3.OperationalError:
        c.execute("CREATE TABLE users (user_id INTEGER, lang TEXT);")

    c.execute('INSERT INTO users VALUES (?, ?)', (query.sender.id, "it",))

    conn.commit()
    conn.close()

    _ = getlang(query.sender.id)
    bot.edit_message(query.sender.id,  query.message.message_id, _("Done!"))
    

@bot.callback("lang_en")
def lang_en(query, chat, message):
    print("to do")



bot.run()
