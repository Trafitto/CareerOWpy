import requests
from bs4 import BeautifulSoup
from datetime import datetime


from Utils.dbUtils import dbHelper


def scraper(url,battletag):
    user={}
    user['name']=battletag
    ### Prevent no data error
    ### User init fast way
    user['rank']=0
    user['time']=0
    user['totGame']=0
    user['win']=0
    user['tied']=0
    user['lost']=0
    user['death']=0
    user['soloKill']=0
    user['elimination']=0
    user['healingDone']=0
    ### Daily record
    user['winD']=0
    user['tiedD']=0
    user['lostD']=0
    user['deathD']=0
    user['soloKillD']=0
    user['eliminationD']=0
    user['healingDoneD']=0
    r=requests.get(url+user['name'])

    data=r.text

    soup=BeautifulSoup(data,'html.parser')

    RankElement=soup.find_all("div",class_="competitive-rank")
    if RankElement:
        user['rank']=RankElement[0].div.get_text()

    compElement=soup.find_all("div",id='competitive')

    for e in compElement:
        a=e.find('section',class_='content-box u-max-width-container career-stats-section')
        c= a.find_all('div',class_='column xs-12 md-6 xl-4')

        #c[n] -> Stat quads... (c[5] -> Game)

        stat=[]
        ## COMBAT quads
        for p in c[0].find_all('tr'):
            t=p.find_all('td')
            for f in t:
                stat.append(f.get_text())
        ### Assist quads
        for p in c[1].find_all('tr'):
            t=p.find_all('td')
            for f in t:
                stat.append(f.get_text())
        ## Game quads
        for p in c[5].find_all('tr'):
            t=p.find_all('td')
            for f in t:
                stat.append(f.get_text())



        ### .replace('.','') when number reach 1000> the Ow site use . for separate
        for i in range(0,len(stat)):
            ### Game quads
            if stat[i]=='Time Played' or stat[i]=='Tempo di gioco':
                user['time'],text=stat[i+1].split(' ') #pythonic way to get just the hours
            if stat[i]=='Games Played' or stat[i]=='Partite giocate':
                user['totGame']=stat[i+1].replace('.','')
            if stat[i]=='Games Won' or stat[i]=='Partite vinte':
                user['win']=stat[i+1].replace('.','')
            if stat[i]=='Games Tied' or stat[i]=='Partite pareggiate':
                user['tied']=stat[i+1].replace('.','')
            if stat[i]=='Games Lost' or stat[i]=='Partite perse' :
                user['lost']=stat[i+1].replace('.','')
            ### Combat quads
            if stat[i]=='Deaths' or stat[i]=='Morti' :
                user['death']=stat[i+1].replace('.','')
            if stat[i]=='Solo Kills' or stat[i]=='Uccisioni solitarie' :
                user['soloKill']=stat[i+1].replace('.','')
            if stat[i]=='Eliminations' or stat[i]=='Eliminazioni' :
                user['elimination']=stat[i+1].replace('.','')
            ### Assist quads
            if stat[i]=='Healing Done' or stat[i]=='Cure fornite' :
                user['healingDone']=stat[i+1].replace('.','')


        return user



def Update(url='https://playoverwatch.com/it-it/career/pc/'):
    startTime = datetime.now()
    db=dbHelper()

    users=db.getUsers()

    if users!= None:
        for u in users:
            user={}
            user=scraper(url,u)
            # Add data on DB
            db.insertData(user['name'],int(user['rank']),int(user['time']),int(user['totGame']),int(user['win']),int(user['tied']),int(user['lost']))

        print('\nScraping running in: ')
        print(datetime.now() - startTime)
        print('\n')
    else:
        print ('Nessun battletag trovato')


### This function will be deprecated because the Ow site does not update the statistics in real time
def UpdateOverlay(battletag,url='https://playoverwatch.com/it-it/career/pc/'):
    startTime = datetime.now()
    user={}
    dailyU={}
    db=dbHelper()

    try:
        user=scraper(url,battletag)

        ### Check for daily records
        dailyU=db.getDailyData(battletag)

        if dailyU is None or len(dailyU)<=0:
            ### Insert on daily table (once a day)
            db.insertdailyData(user['name'],int(user['rank']),int(user['time']),int(user['totGame'])
                ,int(user['win']),int(user['tied']),int(user['lost']),int(user['death']),int(user['soloKill']),int(user['elimination']),int(user['healingDone']))
        else:

            for daily in dailyU:

                user['winD']=int(user['win'])-int(daily[5])
                user['tiedD']=int(user['tied'])-int(daily[6])
                user['lostD']=int(user['lost'])-int(daily[7])
                user['deathD']=int(user['death'])-int(daily[8])
                user['soloKillD']=int(user['soloKill'])-int(daily[9])
                user['eliminationD']=int(user['elimination'])-int(daily[10])
                user['healingDoneD']=int(user['healingDone'])-int(daily[11])

    except Exception as e :
        print('Errore!\n'+str(e))
    print('\nScraping running in: ')
    print(datetime.now() - startTime)
    print('\n')
    return user
