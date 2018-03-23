from Utils.Scraper import UpdateOverlay
from PIL import Image, ImageDraw, ImageFont,ImageEnhance
from datetime import datetime

#rgb(15, 226, 124)

def CreateImg(battletag):

    size=480,480
    im=Image.new("RGB",size,(15, 226, 124,255))


    font=ImageFont.truetype('font\impact.ttf',25)
    d=ImageDraw.Draw(im)
    user=UpdateOverlay(battletag)
    if user!=None:

        text='Actual rank:'+user['rank']+ '     Time played '+user['time'] +'\n'+'w  /t  /l   tot'+'\n'+user['win']+'/'+user['tied']+'/'+user['lost']+' '+user['totGame']


        d.text((20,20),text,(255,255,255,255),font=font)



        im.save('Overlay/Overlay-'+user['name']+".png")
        startTime = datetime.now()
        print('Overlay aggiornato '+str(startTime))
    else:
        print('Nessun dato trovato')

def CreateTxt(battletag):

    user=UpdateOverlay(battletag)
    if user!=None:
        out_file = "Overlay/Overlay-"+user['name']+".txt"
        text='Actual rank:'+user['rank']+ '     Time played '+user['time'] +'\n'+'w  /t  /l   tot'+'\n'+user['win']+'/'+user['tied']+'/'+user['lost']+' '+user['totGame']
        with open(out_file, 'w') as f:
            f.write(text)
        f.close()
        startTime = datetime.now()
        print('Overlay aggiornato ' +str(startTime))
    else:
        print('Nessun dato trovato')
