from flask import Flask, request
import telepot
import urllib3
from Utils.dbUtils import dbHelper
import random
import os
from TelegramBot.Secrets import SECRET,TOKEN,WebHookUrl



def find_jpg_filenames( path_to_dir, suffix=".png" ):
    filenames = os.listdir(path_to_dir)
    return [ path_to_dir+'/'+filename for filename in filenames if filename.endswith( suffix ) ]

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))


bot = telepot.Bot(TOKEN)
bot.setWebhook(WebHookUrl+SECRET, max_connections=1)

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h3>Ciao!</h3>'



AddList=[]

@app.route('/{}'.format(SECRET), methods=["POST"])
def telegram_webhook():
	update = request.get_json()
    #isAdding=False
	if "message" in update:
		try:
			text = update["message"]["text"]
		except:
			text=''
		chat_id = update["message"]["chat"]["id"]
		try:
			username=update["message"]["from"]["username"]
		except:
			username='No_Username'
		if text =="/start" or text=='/start@careerOW_bot':
			bot.sendMessage(chat_id,"Ciao")


	return "OK"


if __name__ == 'main':
    app.run()
