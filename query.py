import logging
import telegram
import sys
import MySQLdb


maxMessageLength = 1200 + 1
maxLogMessageLength = 2400 + 1
maxSingleMessageLength = 400

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

db_name = "comm.db"

def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    str = "/listplayer" + "\n" \
          + "/listplayerres" + "\n" \
          + "/listplayerenl" + "\n" \
          + "/listfrackerportal" + "\n" \
          + "/listfrackerowner" + "\n" \
          + "/listplayerlog wwx" + "\n"
    bot.sendMessage(update.message.chat_id, text=str)


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def listPlayer(bot, update):
    db = MySQLdb.connect(host="ingrex-lib.cbxixqiqoaj0.ap-northeast-1.rds.amazonaws.com", user="wangxin",
                         passwd="tsinghua", db="ingrex", charset="utf8mb4")
    # prepare a cursor object using cursor() method
    db.set_character_set('utf8')

    c = db.cursor()
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')
    ret = listplayer(c)
    bot.sendMessage(update.message.chat_id, text=ret)

def listPlayerRes(bot, update):
    db = MySQLdb.connect(host="ingrex-lib.cbxixqiqoaj0.ap-northeast-1.rds.amazonaws.com", user="wangxin",
                         passwd="tsinghua", db="ingrex", charset="utf8mb4")
    # prepare a cursor object using cursor() method
    db.set_character_set('utf8')

    c = db.cursor()
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')
    ret = listplayer(c, "RESISTANCE")
    i = 0
    while i + maxSingleMessageLength < maxMessageLength:
        str = ret[i:i+maxSingleMessageLength]
        bot.sendMessage(update.message.chat_id, text=str)
        i += maxSingleMessageLength

def listPlayerEnl(bot, update):
    db = MySQLdb.connect(host="ingrex-lib.cbxixqiqoaj0.ap-northeast-1.rds.amazonaws.com", user="wangxin",
                         passwd="tsinghua", db="ingrex", charset="utf8mb4")
    # prepare a cursor object using cursor() method
    db.set_character_set('utf8')

    c = db.cursor()
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')
    ret = listplayer(c, "ENLIGHTENED")
    i = 0
    while i + maxSingleMessageLength < maxMessageLength:
        str = ret[i:i+maxSingleMessageLength]
        bot.sendMessage(update.message.chat_id, text=str)
        i += maxSingleMessageLength

def listFrackerPortal(bot, update):
    db = MySQLdb.connect(host="ingrex-lib.cbxixqiqoaj0.ap-northeast-1.rds.amazonaws.com", user="wangxin",
                         passwd="tsinghua", db="ingrex", charset="utf8mb4")
    # prepare a cursor object using cursor() method
    db.set_character_set('utf8')

    c = db.cursor()
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')
    ret = listfrackerportal(c)
    i = 0
    while i + maxSingleMessageLength < maxMessageLength:
        str = ret[i:i+maxSingleMessageLength]
        bot.sendMessage(update.message.chat_id, text=str)
        i += maxSingleMessageLength

def listFrackerOwner(bot, update):
    db = MySQLdb.connect(host="ingrex-lib.cbxixqiqoaj0.ap-northeast-1.rds.amazonaws.com", user="wangxin",
                         passwd="tsinghua", db="ingrex", charset="utf8mb4")
    # prepare a cursor object using cursor() method
    db.set_character_set('utf8')

    c = db.cursor()
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')
    ret = listfrackerowner(c)
    i = 0
    while i + maxSingleMessageLength < maxMessageLength:
        str = ret[i:i+maxSingleMessageLength]
        bot.sendMessage(update.message.chat_id, text=str)
        i += maxSingleMessageLength

def listPlayerLog(bot, update, args):
    db = MySQLdb.connect(host="ingrex-lib.cbxixqiqoaj0.ap-northeast-1.rds.amazonaws.com", user="wangxin",
                         passwd="tsinghua", db="ingrex", charset="utf8mb4")
    # prepare a cursor object using cursor() method
    db.set_character_set('utf8')

    c = db.cursor()
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')
    print ' '.join(args)
    ret = listplayerlog(c, ' '.join(args))
    i = 0
    while i + maxSingleMessageLength < maxLogMessageLength:
        str = ret[i:i+maxSingleMessageLength]
        bot.sendMessage(update.message.chat_id, text=str)
        i += maxSingleMessageLength


def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # Open database connection
    db = MySQLdb.connect(host="ingrex-lib.cbxixqiqoaj0.ap-northeast-1.rds.amazonaws.com", user="wangxin",
                         passwd="tsinghua", db="ingrex", charset="utf8mb4")
    # prepare a cursor object using cursor() method
    db.set_character_set('utf8')

    c = db.cursor()
    c.execute('SET NAMES utf8;')
    c.execute('SET CHARACTER SET utf8;')
    c.execute('SET character_set_connection=utf8;')

    print listplayer(c)
    print listplayer(c, 'ENLIGHTENED')
    print listplayer(c, 'RESISTANCE')
    print listfrackerowner(c)
    # print listplayerlog(c, 'dabogei')

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
    c.execute("SELECT * FROM message WHERE player=? ORDER BY TIME DESC ", (player,))
    ret = ""
    i = 0
    for row in c.fetchmany(10):
        i += 1
        ret += row + "\n"
    ret += i
    return ret[:maxMessageLength]

def listplayer(c, faction ="ALL"):
    if (faction == "ALL"):
        c.execute("SELECT player, team, COUNT(*) AS player_occurrence FROM (SELECT player, team  FROM  message WHERE TIME > (DATE_SUB(curdate(), INTERVAL 2 WEEK)))  AS A GROUP BY player ORDER BY COUNT(*) DESC;")
    else:
        c.execute("""SELECT player, COUNT(player) AS player_occurrence FROM (SELECT player, team FROM message WHERE team='%s'  and TIME > (DATE_SUB(curdate(), INTERVAL 2 WEEK))) AS A GROUP BY player ORDER BY player_occurrence DESC;""" % faction)
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
    c.execute("SELECT portalname, COUNT(portalname) as freq FROM (SELECT portalname FROM message WHERE message LIKE '%fracker%') GROUP BY portalname ORDER BY freq DESC")
    ret = ""
    for row in c.fetchall():
        ret += str(row)[2:-1].replace("\'", "").decode('unicode-escape') + "\n"
        if ret.__sizeof__() > maxMessageLength:
            break
    return ret


def listfrackerowner(c):
    c.execute("SELECT player, COUNT(player) as freq FROM (SELECT player FROM message WHERE message LIKE '%fracker%') GROUP BY player ORDER BY freq DESC")
    ret = ""
    for row in c.fetchall():
        ret += str(row)[2:-1].replace("\'", "") + "\n"
        if ret.__sizeof__() > maxMessageLength:
            break
    return ret

def listplayerlog(c, player):
    c.execute(
        "SELECT TIME, message FROM message WHERE player=? COLLATE NOCASE ORDER BY TIME DESC", (player, ))
    ret = ""
    for row in c.fetchall():
        ret += str(row)[2:-1].decode('unicode-escape') + "\n"
        if ret.__sizeof__() > maxLogMessageLength:
            break
    return ret


if __name__ == '__main__':
    main()
