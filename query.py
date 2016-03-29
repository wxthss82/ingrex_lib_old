import sqlite3
import telegram

def main():
    bot = telegram.Bot('203372574:AAHQn2Z-a5r-Hvgmj2YCNlCYDCqYMEDLto4')
    print bot.getMe()

    conn = sqlite3.connect("test1.db")
    c = conn.cursor()
    # queryPlayerLog(c, 'plopl666')
    # queryPlayer(c)
    queryPlayer(c)

def queryPlayerLog(c, player):
    c.execute("SELECT * FROM MESSAGE WHERE PLAYER=? ORDER BY TIME DESC ", (player,))
    for i in c.fetchmany(10):
        print i

def queryPlayer(c,faction = "ALL"):
    if (faction == "ALL"):
        c.execute("SELECT DISTINCT PLAYER FROM MESSAGE")
    else:
        c.execute("SELECT DISTINCT PLAYER, TEAM FROM MESSAGE WHERE TEAM=? AND LNG!=\"-1\"", (faction,))
    i = 0
    for row in c.fetchall():
        i += 1
        print row
    print i





if __name__ == '__main__':
    main()
