import logging
import sqlite3
import telegram
import sys


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

def listplayer(bot, update):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    ret = queryPlayer(c)
    bot.sendMessage(update.message.chat_id, text=ret)

def listplayerres(bot, update):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    ret = queryPlayer(c, "RESISTANCE")
    bot.sendMessage(update.message.chat_id, text=ret)

def listplayerenl(bot, update):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    ret = queryPlayer(c, "ENLIGHTENED")
    bot.sendMessage(update.message.chat_id, text=ret)

def listfrackerportal(bot, update):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    ret = queryFracker(c)
    bot.sendMessage(update.message.chat_id, text=ret)

def listfrackerowner(bot, update):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    ret = queryFrackerowner(c)
    bot.sendMessage(update.message.chat_id, text=ret)

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    print queryPlayer(c)
    print queryFracker(c)
    print queryPlayer(c, 'ENLIGHTENED')
    print queryPlayer(c, 'RESISTANCE')
    print queryFrackerowner(c)

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
    dp.addTelegramCommandHandler("listplayer", listplayer)
    dp.addTelegramCommandHandler("listplayerres", listplayerres)
    dp.addTelegramCommandHandler("listplayerenl", listplayerenl)
    dp.addTelegramCommandHandler("listfrackerportal", listfrackerportal)
    dp.addTelegramCommandHandler("listfrackerowner", listfrackerowner)






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
        c.execute("SELECT PLAYER, TEAM, COUNT(*) AS player_occurrence FROM MESSAGE GROUP BY PLAYER ORDER BY COUNT(*) DESC")
    else:
        c.execute("SELECT PLAYER, COUNT(PLAYER) AS player_occurrence FROM (SELECT PLAYER, TEAM FROM MESSAGE WHERE TEAM=?)  GROUP BY PLAYER ORDER BY player_occurrence DESC", (faction,))
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
    c.execute("SELECT PORTALNAME, COUNT(PORTALNAME) as freq FROM (SELECT PORTALNAME FROM MESSAGE WHERE BODY LIKE '%fracker%') GROUP BY PORTALNAME ORDER BY freq DESC")
    ret = ""
    for row in c.fetchall():
        ret += str(row).replace('u\'', "").replace("\'", "").encode("utf-8") + "\n"
        if ret.__sizeof__() > 390:
            break
    return ret


def queryFrackerowner(c):
    c.execute("SELECT PLAYER, COUNT(PLAYER) as freq FROM (SELECT PLAYER FROM MESSAGE WHERE BODY LIKE '%fracker%') GROUP BY PLAYER ORDER BY freq DESC")
    ret = ""
    for row in c.fetchall():
        ret += str(row).replace('u\'', "").replace("\'", "").encode("utf-8") + "\n"
        if ret.__sizeof__() > 390:
            break
    return ret

if __name__ == '__main__':
    main()
