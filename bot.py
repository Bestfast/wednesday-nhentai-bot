import botogram, os, sqlite3 

bot = botogram.create(os.environ['BOT'])
bot.about = "A nHentai's (unofficial) bot"
bot.owner = "@Bestfast"

@bot.command("start")
def start_command(chat, message, args):
    
    """Start the bot"""
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    try:
        c.execute("SELECT ? FROM users", (message.sender.id,))
    
    except sqlite3.OperationalError:
        c.execute("CREATE TABLE users (user_id INTEGER, lang TEXT);")
    
    data = c.fetchall()
    
    if not data:

        btns = botogram.Buttons()
        btns[0].callback("IT", "lang_it")
        btns[1].callback("EN", "lang_en")

        chat.send("Hi! First of all, select your language!", attach=btns)
        
        conn.commit()
    
    conn.close()



@bot.callback("lang_it")
def lang_it(query, chat, message):

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    try:
        c.execute('DELETE FROM users WHERE user_id = ?', (message.sender.id,))
    except sqlite3.OperationalError:
        c.execute("CREATE TABLE users (user_id INTEGER, lang TEXT);")

    c.execute('INSERT INTO users VALUES (?, ?)', (message.sender.id, "it",))

    conn.commit()
    conn.close()

    bot.edit_message(query.sender.id,  query.message.message_id, "Done!")
    

@bot.callback("lang_en")
def lang_en(query, chat, message):
    print("to do")

bot.run()