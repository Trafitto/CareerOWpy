import sqlite3
import datetime
class dbHelper:
    def __init__(self,dbname="CareerDB.sqlite3"):
        self.dbname=dbname
        self.conn=sqlite3.connect(dbname)

    def getLastData(self):
        query='''
            SELECT a.name,a.ranks,a.playedTime,a.totGame,a.win,a.tied,a.lost FROM Career as a
            WHERE a.updated=(SELECT updated FROM Career WHERE name=a.name ORDER BY updated DESC LIMIT 1)
        '''
        return [x[0] for x in self.conn.execute(query)]

    def insertData(self,name,ranks,playedTime,totGame,win,tied,lost):
        query='''
            INSERT INTO Career (name,ranks,playedTime,totGame,win,tied,lost,updated)
            VALUES (?,?,?,?,?,?,?,?)
        '''
        args = (name,ranks,playedTime,totGame,win,tied,lost,datetime.datetime.now() )
        self.conn.execute(query, args)
        self.conn.commit()

#From python cli
# from dbUtils import dbManage
# db=dbManage()
# db.CreateTable()
class dbManage:
    def __init__(self,dbname="CareerDB.sqlite3"):
        self.dbname=dbname
        self.conn=sqlite3.connect(dbname)

    def CreateTable(self):
        cursor=self.conn.cursor()
        cursor.execute('''
            CREATE TABLE Career(
                id INTEGER PRIMARY KEY,
                name TEXT,
                ranks INTEGER,
                playedTime INTEGER,
                totGame INTEGER,
                win INTEGER,
                tied INTEGER,
                lost INTEGER,
                updated DATETIME
            )
        ''')
        self.conn.commit()
    def DropTable():
        cursor=self.conn.cursor()
        cursor.execute('''
            DROP TABLE Career
        ''')
        self.conn.commit()
