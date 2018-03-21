import sqlite3
import datetime


#From python cli
# from dbUtils import dbManage
# db=dbHelper()
# db.CreateTable()
class dbHelper:
    def __init__(self,dbname="CareerDB.sqlite3"):
        self.dbname=dbname
        self.conn=sqlite3.connect(dbname)
        self.CreateTable()

    def CreateTable(self):
        cursor=self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Career(
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
        cursor.execute('''

            CREATE TABLE IF NOT EXISTS Users(
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE
            )
        ''')
        self.conn.commit()
    def DropAndCreateAll(self):
        self.DropTableCareer()
        self.DropTableUsers()
        self.CreateTable()

    def DropTableCareer(self):
        cursor=self.conn.cursor()
        cursor.execute('''
            DROP TABLE Career
        ''')
        self.conn.commit()

    def DropTableUsers(self):
        cursor=self.conn.cursor()
        cursor.execute('''
            DROP TABLE Users
        ''')
        self.conn.commit()

    def addUser(self,name):
        query='''
            INSERT INTO Users (name)
            VALUES (?)
        '''
        args=(name,)
        self.conn.execute(query,args)
        self.conn.commit()

    def getUsers(self):
        query='''
            SELECT name from Users
        '''
        return [x[0] for x in self.conn.execute(query)]

    def getLastData(self):
        query='''
            SELECT a.name,a.ranks,a.playedTime,a.totGame,a.win,a.tied,a.lost FROM Career as a
            WHERE a.updated=(SELECT updated FROM Career WHERE name=a.name ORDER BY updated DESC LIMIT 1)
        '''
        x=self.conn.execute(query)
        return x
        #return [x[0] for x in self.conn.execute(query)]

    def getLastUserData(self,battletag):
        query='''
            SELECT ranks,DATE(updated) FROM Career WHERE name=?  ORDER BY updated DESC LIMIT 20
        '''
        args=(battletag,)
        #x=self.conn.execute(query,args)
        return [x for x in self.conn.execute(query,args)]

    def insertData(self,name,ranks,playedTime,totGame,win,tied,lost):
        query='''
            INSERT INTO Career (name,ranks,playedTime,totGame,win,tied,lost,updated)
            VALUES (?,?,?,?,?,?,?,?)
        '''
        args = (name,ranks,playedTime,totGame,win,tied,lost,datetime.datetime.now() )
        self.conn.execute(query, args)
        self.conn.commit()
