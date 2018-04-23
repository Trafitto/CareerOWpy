from Utils.Scraper import UpdateOverlay
from PIL import Image, ImageDraw, ImageFont,ImageEnhance
from datetime import datetime

#rgb(15, 226, 124)

def textTowrite(battletag):
    user=UpdateOverlay(battletag)
    text=''
    if user!=None:

        text=text+'Actual rank:'+str(user['rank'])+ '     Time played '+str(user['time']) +'\nTotal stat:  '+'\n          w   /t   /l    tot'+'\n           '+str(user['win'])+'/'+str(user['tied'])+'/'+str(user['lost'])+' '+str(user['totGame'])
        text=text+'\nDaily stat:  \n          w   /t   /l    '+'\n           '+str(user['winD'])+'/'+str(user['tiedD'])+'/'+str(user['lostD'])+'\n           Death: '+str(user['deathD'])+' Solo Kill: '+str(user['soloKillD'])+'\n           Elimination: '+str(user['eliminationD'])
        text=text+' Healing Done: '+str(user['healingDoneD'])
    else:
        print('Nessun dato trovato')
    return text
def CreateImg(battletag):

    size=480,480
    im=Image.new("RGB",size,(15, 226, 124,255))


    font=ImageFont.truetype('font\impact.ttf',25)
    d=ImageDraw.Draw(im)
    text=textTowrite(battletag)

    d.text((20,20),text,(255,255,255,255),font=font)



    im.save('Overlay/Overlay-'+battletag+".png")
    startTime = datetime.now()
    print('Overlay aggiornato '+str(startTime))



def CreateTxt(battletag):
    text=textTowrite(battletag)
    out_file = "Overlay/Overlay-"+battletag+".txt"

    with open(out_file, 'w') as f:
        f.write(text)
    f.close()
    startTime = datetime.now()
    print('Overlay aggiornato ' +str(startTime))
