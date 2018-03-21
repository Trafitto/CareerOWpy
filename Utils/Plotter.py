#Frist time with matplotlib
import matplotlib.pyplot as plt
from Utils.dbUtils import dbHelper

db=dbHelper()

def plotUser(user):

    plt.ylabel('Rank')
    plt.xlabel('Data')
    plt.title(user)
    data=db.getLastUserData(user)
    rank=[]
    update=[]

    for d in data:
        rank.append(d[0])
        update.append(d[1])


    plt.plot(update,rank, 'ro--')
    #plt.axis([0, 6, 0, 20])

    plt.savefig('./PlotImg/'+ user+'.png')
    plt.close()
    #plt.show()


def plotAll():
    users=db.getUsers()
    for u in users:
        print(u)
        plotUser(u)
