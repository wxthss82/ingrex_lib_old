import logging
import sqlite3
import telegram

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)



def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def listplayer(bot, update):
    conn = sqlite3.connect("message.db")
    c = conn.cursor()
    ret = queryPlayer(c)
    bot.sendMessage(update.message.chat_id, text=ret)


def main():
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
    return ret

def queryPlayer(c,faction = "ALL"):
    if (faction == "ALL"):
        c.execute("SELECT DISTINCT PLAYER FROM MESSAGE")
    else:
        c.execute("SELECT DISTINCT PLAYER, TEAM FROM MESSAGE WHERE TEAM=? AND LNG!=\"-1\"", (faction,))
    i = 0
    ret = ""
    for row in c.fetchall():
        i += 1
        print row
        ret += str(row) + "\n"
    ret += str(i)
    return ret





if __name__ == '__main__':
    main()
