import logging
import sqlite3
import telegram

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

db_name = "message.db"

def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def activeplayer(bot, update):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    ret = queryPlayer(c)
    bot.sendMessage(update.message.chat_id, text=ret)

def activeplayerres(bot, update):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    ret = queryPlayer(c, "RESISTANCE")
    bot.sendMessage(update.message.chat_id, text=ret)

def activeplayerenl(bot, update):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    ret = queryPlayer(c, "ENLIGHTENED")
    bot.sendMessage(update.message.chat_id, text=ret)

def listfracker(bot, update):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    ret = queryFracker(c)
    bot.sendMessage(update.message.chat_id, text=ret)


def main():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    print queryPlayer(c)
    print queryFracker(c)

    bot = telegram.Bot("203372574:AAHQn2Z-a5r-Hvgmj2YCNlCYDCqYMEDLto4")
    print bot.getMe()


    # queryPlayerLog(c, 'plopl666')
    # queryPlayer(c)
    # queryPlayer(c)

    # updates = bot.getUpdates()
    # chat_id = bot.getUpdates()[-1].message.chat_id
    # bot.sendMessage(chat_id=chat_id, text="I'm sorry Dave I'm afraid I can't do that.")
    # print [u.message.text for u in updates]


    # Create the EventHandler and pass it your bot's token.
    updater = telegram.Updater("203372574:AAHQn2Z-a5r-Hvgmj2YCNlCYDCqYMEDLto4")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("help", help)
    dp.addTelegramCommandHandler("listplayer", activeplayer)
    dp.addTelegramCommandHandler("listplayer", activeplayerres)
    dp.addTelegramCommandHandler("listplayer", activeplayerenl)




    # on noncommand i.e message - echo the message on Telegram
    dp.addTelegramMessageHandler(echo)

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


def queryPlayerLog(c, player):
    c.execute("SELECT * FROM MESSAGE WHERE PLAYER=? ORDER BY TIME DESC ", (player,))
    ret = ""
    i = 0
    for row in c.fetchmany(10):
        i += 1
        ret += row + "\n"
    ret += i
    return ret[:390]

def queryPlayer(c,faction = "ALL"):
    if (faction == "ALL"):
        c.execute("SELECT PLAYER, TEAM, COUNT(PLAYER) AS player_occurrence FROM MESSAGE GROUP BY PLAYER ORDER BY player_occurrence DESC")
    else:
        c.execute("SELECT PLAYER, COUNT(PLAYER) AS player_occurrence FROM MESSAGE GROUP BY PLAYER ORDER BY player_occurrence DESC WHERE TEAM=?", (faction,))
    i = 0
    ret = ""
    for row in c.fetchall():
        i += 1
        ret += str(row).replace('u\'', "").replace("\'", "") + "\n"
        if ret.__sizeof__() > 390:
            break
    ret += str(i)
    return ret

def queryFracker(c):
    c.execute("SELECT PORTALNAME, PLAYER, COUNT(PORTALNAME) AS portal_occurrence FROM MESSAGE GROUP BY PORTALNAME ORDER BY portal_occurrence DESC WHERE BODY LIKE '%fracker%'")
    ret = ""
    for row in c.fetchall():
        ret += str(row).replace('u\'', "").replace("\'", "") + "\n"
        if ret.__sizeof__() > 390:
            break
    return ret

if __name__ == '__main__':
    main()
