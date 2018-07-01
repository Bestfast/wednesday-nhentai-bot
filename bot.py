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
        c.execute("CREATE TABLE users (user_id INTEGER);")
    
    data = c.fetchall()
    
    if not data:
        c.execute('INSERT INTO users VALUES (?)', (message.sender.id,))
        conn.commit()
    
    conn.close()

bot.run()