import requests
from bs4 import BeautifulSoup
from datetime import datetime
startTime = datetime.now()

from Utils.dbUtils import dbHelper


def scraper(url,battletag):
    user={}
    user['name']=battletag
    r=requests.get(url+user['name'])

    data=r.text

    soup=BeautifulSoup(data,'html.parser')

    RankElement=soup.find_all("div",class_="competitive-rank")
    user['rank']=RankElement[0].div.get_text()

    compElement=soup.find_all("div",id='competitive')

    for e in compElement:
        a=e.find('section',class_='content-box u-max-width-container career-stats-section')
        c= a.find_all('div',class_='column xs-12 md-6 xl-4')

        #c[n] -> Stat quads... (c[5] -> Game)

        stat=[]
        ## Game quads
        for p in c[5].find_all('tr'):
            t=p.find_all('td')
            for f in t:
                stat.append(f.get_text())
        ## COMBAT quads
        for p in c[0].find_all('tr'):
            t=p.find_all('td')
            for f in t:
                stat.append(f.get_text())

        ### Prevent no data error
        user['time']=0
        user['totGame']=0
        user['win']=0
        user['tied']=0
        user['lost']=0
        user['death']=0
        user['soloKill']=0
        user['elimination']=0
        for i in range(0,len(stat)):
            if stat[i]=='Time Played' or stat[i]=='Tempo di gioco':
                user['time'],text=stat[i+1].split(' ') #pythonic way to get just the hours
            if stat[i]=='Games Played' or stat[i]=='Partite giocate':
                user['totGame']=stat[i+1]
            if stat[i]=='Games Won' or stat[i]=='Partite vinte':
                user['win']=stat[i+1]
            if stat[i]=='Games Tied' or stat[i]=='Partite pareggiate':
                user['tied']=stat[i+1]
            if stat[i]=='Games Lost' or stat[i]=='Partite perse' :
                user['lost']=stat[i+1]

            if stat[i]=='Deaths' or stat[i]=='Morti' :
                user['death']=stat[i+1]
            if stat[i]=='Solo Kills' or stat[i]=='Uccisioni solitarie' :
                user['soloKill']=stat[i+1]
            if stat[i]=='Eliminations' or stat[i]=='Eliminazioni' :
                user['elimination']=stat[i+1]
        # user['time'],text=stat[1].split(' ') #pythonic way to get just the hours
        # user['totGame']=stat[3]
        # user['win']=stat[5]
        # user['tied']=stat[7]
        # user['lost']=stat[9]

        return user

def UpdateOverlay(battletag,url='https://playoverwatch.com/it-it/career/pc/'):
    user={}
    try:
        user=scraper(url,battletag)
    except Exception as e :
        print('Errore!\n'+str(e))
    print('\nScraping running in: ')
    print(datetime.now() - startTime)
    print('\n')
    return user

def Update(url='https://playoverwatch.com/it-it/career/pc/'):
    db=dbHelper()

    users=db.getUsers()

    if users!= None:
        for u in users:
            user={}
            user=scraper(url,u)
        	#	print('->',user['name'])

            db.insertData(user['name'],int(user['rank']),int(user['time']),int(user['totGame']),int(user['win']),int(user['tied']),int(user['lost']))


        print('\nScraping running in: ')
        print(datetime.now() - startTime)
        print('\n')


        # 	print(user['name']+' rank:'+user['rank']+ ' time played '+user['time'] +'\n'+'w /t /l  tot'+'\n'+user['win']+'/'+user['tied']+'/'+user['lost']+' '+user['totGame'])
    else:
        print ('Nessun battletag trovato')
    # print('\nTotal script running in: ')
    # print(datetime.now() - startTime)
