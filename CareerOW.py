import os
import sys
from Utils.Scraper import Update
from Utils.Plotter import plotUser,plotAll
from Utils.Overlay import CreateImg,CreateTxt
from Utils.dbUtils import dbHelper
import time
db=dbHelper()

if not os.path.exists('Overlay'):
    os.makedirs('Overlay')
if not os.path.exists('PlotImg'):
    os.makedirs('PlotImg')

print ('Career OW CLI\n')
sleepTime=300 # in seconds
def helpMsg():
	print('\n')
	print('-update Aggiorna il database')
	print ('-add <battletag> Aggiunge un utente alla lista')
	print ('-data Visualizza gli ultimi risultati presenti nel database')
	print ("-plot <battletag> Crea un grafico con l'andamento di quell'utente")
	print ("-plotall Crea un grafico dell'andamento per ogni utente")
	print ("-soimg <battletag> Aggiorna ogni "+str(sleepTime)+" secondi un immagine utilizzabile come overlay per gli streamer")
	print ("-sotxt <battletag> Aggiorna ogni "+str(sleepTime)+" secondi un file di testo utilizzabile come overlay per gli streamer")
	print ('-users Visualizza battletag')
	print ("-removeuser <battletag> Rimuove l'utente con quel battletag")
	print ('-cleardb Cancella e ricrea tutte le tabelle del database (drop and create)')
	print('-help Visualizza questo messaggio')
	print('\n')

def PrintLastData():
	users=db.getLastData()
	text=''
	for user in users:
		text+=user[0]+' rank:'+str(user[1])+ ' time played '+str(user[2]) +'\n'+'w /t /l  tot'+'\n'+str(user[4])+'/'+str(user[5])+'/'+str(user[6])+' '+str(user[3])+'\n'
	return text
def PritnUsers():
	users=db.getUsers()
	text=''
	for u in users:
		text+=u+'\n'
	return text
try:
	command=sys.argv[1]
except:
	helpMsg()
	sys.exit()

if command=='-help' or command=='-h':
	helpMsg()
elif command=='-update' or command=='-u':
	#Scraping and update DB
	print('Aggiornamento dati in corso...')
	Update()

elif command=='-add' or command=='-a':
	user=''
	try:
		user=sys.argv[2]
	except:
		helpMsg()
		print ('E necessario un battletag ex: Nickname-123')

		sys.exit()
	if user != None or user !='':
		#Add user on DB
		db.addUser(user)
		print ('Aggiunto: ',user)

elif (command=='-users' or command=='-user' ):
	print(PritnUsers())

elif (command=='-data' or command=='-d'):
	print(PrintLastData())

elif(command=='-cleardb'):
	print ('Questa funzione cancellerà tutti i dati presenti sul database vuoi proseguire?')
	choice=''
	while(choice!='y' or choice!='n'):
		choice=input("y/n: ")
		if choice=='y':
			db.DropAndCreateAll()

			sys.exit()
		elif (choice=='n'):
			print ('Ok, ciao')
			sys.exit()
elif(command=='-removeuser'):
	user=''
	try:
		user=sys.argv[2]
	except:
		helpMsg()
		print ('E necessario un battletag ex: Nickname-123')

		sys.exit()
	if user != None or user !='':
		#Add user on DB

		print ("Questa funzione cancellerà l'utente selezionato vuoi proseguire")
		choice=''
		while(choice!='y' or choice!='n'):
			choice=input("y/n: ")
			if choice=='y':
				db.removeUser(user)
				print ('Rimosso',user)
				sys.exit()
			elif (choice=='n'):
				print ('Ok, ciao')
				sys.exit()
elif (command=='-plot'):
	user=''
	try:
		user=sys.argv[2]
	except:
		helpMsg()
		print ('E necessario un battletag ex: Nickname-123')

		sys.exit()
	if user != None or user !='':
		#Add user on DB
		print('Generazione grafico in corso...')
		plotUser(user)
		sys.exit()
elif(command=='-plotall'):
	print('Generazione grafici in corso...')
	plotAll()
elif(command=='-startoverlayimg' or command=='-soimg'):
	user=''
	try:
		user=sys.argv[2]
	except:
		helpMsg()
		print ('E necessario un battletag ex: Nickname-123')

		sys.exit()
	if user != None or user !='':
		print ('Attenzione i dati aggiornati in questo modo non saranno inseriti sul db')
		print ('^C Per chiudere la procedura')
		try:
			while True:
				CreateImg(user)
				time.sleep(sleepTime) #prevent to many request

		except KeyboardInterrupt:
			print ('^C Ricevuto!')
			sys.exit()
elif(command=='-startoverlaytxt' or command=='-sotxt'):
	user=''
	try:
		user=sys.argv[2]
	except:
		helpMsg()
		print ('E necessario un battletag ex: Nickname-123')

		sys.exit()
	if user != None or user !='':
		print ('Attenzione i dati aggiornati in questo modo non saranno inseriti sul db')
		print ('^C Per chiudere la procedura')
		try:
			while True:
				CreateTxt(user)
				time.sleep(sleepTime) # prevent to many request
		except KeyboardInterrupt:
			print ('^C Ricevuto!')
			sys.exit()
else:
	print('Comando non riconosciuto\n')
	helpMsg()
