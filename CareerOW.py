import requests
from bs4 import BeautifulSoup
from datetime import datetime
startTime = datetime.now()
from Users import users
from dbUtils import dbHelper
db=dbHelper()

url='https://playoverwatch.com/en-us/career/pc/'


for user in users:

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
		for p in c[5].find_all('tr'):
			t=p.find_all('td')

			for f in t:
				stat.append(f.get_text())



		user['time'],text=stat[1].split(' ') #pythonic way to get just the hours
		user['totGame']=stat[3]
		user['win']=stat[5]
		user['tied']=stat[7]
		user['lost']=stat[9]
		print('->',user['name'])

print('\nScraping running in: ')
print(datetime.now() - startTime)
print('\n')
for user in users:
	db.insertData(user['name'],int(user['rank']),int(user['time']),int(user['totGame']),int(user['win']),int(user['tied']),int(user['lost']))
	print(user['name']+' rank:'+user['rank']+ ' time played '+user['time'] +'\n'+'w /t /l  tot'+'\n'+user['win']+'/'+user['tied']+'/'+user['lost']+' '+user['totGame'])

print('\nTotal script running in: ')
print(datetime.now() - startTime)
