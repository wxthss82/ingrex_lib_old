import logging
import sqlite3
import telegram
import sys

maxMessageLength = 1200 + 1
maxSingleMessageLength = 400

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

db_name = "message.db"

def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    str = "/listplayer" + "\n" \
          + "/listplayerres" + "\n" \
          + "/listplayerenl" + "\n" \
          + "/listfrackerportal" + "\n" \
          + "/listfrackerowner" + "\n"
    bot.sendMessage(update.message.chat_id, text=str)


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def listPlayer(bot, update):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    ret = listplayer(c)
    bot.sendMessage(update.message.chat_id, text=ret)

def listPlayerRes(bot, update):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    ret = listplayer(c, "RESISTANCE")
    i = 0
    while i + maxSingleMessageLength < maxMessageLength:
        str = ret[i:i+maxSingleMessageLength]
        bot.sendMessage(update.message.chat_id, text=str)
        i += maxSingleMessageLength

def listPlayerEnl(bot, update):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    ret = listplayer(c, "ENLIGHTENED")
    i = 0
    while i + maxSingleMessageLength < maxMessageLength:
        str = ret[i:i+maxSingleMessageLength]
        bot.sendMessage(update.message.chat_id, text=str)
        i += maxSingleMessageLength

def listFrackerPortal(bot, update):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    ret = listfrackerportal(c)
    i = 0
    while i + maxSingleMessageLength < maxMessageLength:
        str = ret[i:i+maxSingleMessageLength]
        bot.sendMessage(update.message.chat_id, text=str)
        i += maxSingleMessageLength

def listFrackerOwner(bot, update):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    ret = listfrackerowner(c)
    i = 0
    while i + maxSingleMessageLength < maxMessageLength:
        str = ret[i:i+maxSingleMessageLength]
        bot.sendMessage(update.message.chat_id, text=str)
        i += maxSingleMessageLength

def listPlayerLog(bot, update, args):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    print ' '.join(args)
    ret = listplayerlog(c, ' '.join(args))
    i = 0
    while i + maxSingleMessageLength < maxMessageLength:
        str = ret[i:i+maxSingleMessageLength]
        bot.sendMessage(update.message.chat_id, text=str)
        i += maxSingleMessageLength


def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    print listplayer(c)
    print listplayer(c, 'ENLIGHTENED')
    print listplayer(c, 'RESISTANCE')
    print listfrackerowner(c)
    # print listplayerlog(c, 'wwx')

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
    dp.addTelegramCommandHandler("help", help)
    dp.addTelegramCommandHandler("listplayer", listPlayer)
    dp.addTelegramCommandHandler("listplayerres", listPlayerRes)
    dp.addTelegramCommandHandler("listplayerenl", listPlayerEnl)
    dp.addTelegramCommandHandler("listfrackerportal", listFrackerPortal)
    dp.addTelegramCommandHandler("listfrackerowner", listFrackerOwner)
    dp.addTelegramCommandHandler("listplayerlog", listPlayerLog)



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
    return ret[:maxMessageLength]

def listplayer(c, faction ="ALL"):
    if (faction == "ALL"):
        c.execute("SELECT PLAYER, TEAM, COUNT(*) AS player_occurrence FROM MESSAGE GROUP BY PLAYER ORDER BY COUNT(*) DESC")
    else:
        c.execute("SELECT PLAYER, COUNT(PLAYER) AS player_occurrence FROM (SELECT PLAYER, TEAM FROM MESSAGE WHERE TEAM=?)  GROUP BY PLAYER ORDER BY player_occurrence DESC", (faction,))
    i = 0
    ret = ""
    for row in c.fetchall():
        i += 1
        ret += str(row)[2:-1].replace("\'", "").replace(", uENLIGHTENED", ", E").replace(", uRESISTANCE", ", R")  + "\n"
        if ret.__sizeof__() > maxMessageLength:
            break
    ret += str(i)
    return ret

def listfrackerportal(c):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    c.execute("SELECT PORTALNAME, COUNT(PORTALNAME) as freq FROM (SELECT PORTALNAME FROM MESSAGE WHERE BODY LIKE '%fracker%') GROUP BY PORTALNAME ORDER BY freq DESC")
    ret = ""
    for row in c.fetchall():
        ret += str(row)[2:-1].replace("\'", "").decode('unicode-escape') + "\n"
        if ret.__sizeof__() > maxMessageLength:
            break
    return ret


def listfrackerowner(c):
    c.execute("SELECT PLAYER, COUNT(PLAYER) as freq FROM (SELECT PLAYER FROM MESSAGE WHERE BODY LIKE '%fracker%') GROUP BY PLAYER ORDER BY freq DESC")
    ret = ""
    for row in c.fetchall():
        ret += str(row)[2:-1].replace("\'", "") + "\n"
        if ret.__sizeof__() > maxMessageLength:
            break
    return ret

def listplayerlog(c, player):
    c.execute(
        "SELECT TIME, BODY FROM MESSAGE WHERE PLAYER=? ORDER BY TIME DESC", (player, ))
    ret = ""
    for row in c.fetchall():
        ret += str(row)[2:-1].decode('unicode-escape') + "\n"
        if ret.__sizeof__() > maxMessageLength:
            break
    return ret


if __name__ == '__main__':
    main()
