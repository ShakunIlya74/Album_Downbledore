token_api = '1212901280:AAEIKHfwxhf_V6dyPCs-I_RATwucKlXdnII'
import time
import os
import bs4 as bs
import requests
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

users={}
headers={'User-Agent': 'Chrome'}

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, everyone!"+'\n'+"Album Downbledore, yours to command!"+'\n'+"Type /help for S.O.S")

def parsing(update, context):
    global users
    
    users[str(update.effective_chat.id)]=[]
    print(update.message.text)
    album_input = ''
    album_input=update.message.text
    name = list(album_input.split())
    alb = '+'.join(name)
    page = requests.get("https://www.youtube.com/results?search_query={}+album".format(alb), headers=headers)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Searching for singers..')
    print("Searching for singers..")
    li = []
    vip_li = []           
    #links = soup.find_all("a")
    linka = []
    for i in range(5):
        soup = bs.BeautifulSoup(page.content, 'html.parser')
        links = soup.find_all("a")
        linka = [lin.get("href") for lin in links if "playlist" in lin.get("href") or "watch" and "list=" in lin.get("href")]
        if len(linka) > 8:
            break
        #print(linka)
        #time.sleep(5)
    a = 25 if len(linka)>25 else len(linka)
    for i in range(a):
        l = linka[i]
        if "playlist" in l:
            vip_li.append(l)
        elif "watch" and "list=" in l:
            li.append(l)
    if len(vip_li) != 0:
        id_ = vip_li[0].split('list=')[-1].split('&')[0]
        users[str(update.effective_chat.id)].append(id_)
        print("Recording auto-generated album..", id_)  
        context.bot.send_message(chat_id=update.effective_chat.id, text='Recording auto-generated album..')
        
        return id_
        print("Enjoy vibes!")
    elif len(li) != 0:
        id_ = li[0].split('list=')[-1].split('&')[0]
        users[str(update.effective_chat.id)].append(id_)
        print("Recording album..")
        context.bot.send_message(chat_id=update.effective_chat.id, text='Recording album..')
        return id_
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, smt went wrong.. Try again")
        print("Sorry, smt went wrong.. Try again")
        

def song_catcher(plink, number, ide):
    os.system("youtube-dl -o {}\%(title)s-%(uploader)s.%(ext)s -i -x --audio-format opus --playlist-items {} -- {}".format(ide, number, plink))
    time.sleep(5)
    with os.scandir("{}".format(ide)) as muslo:
        for music in muslo:
            songd = music.name
            print(songd)
    return '{}\{}'.format(ide, songd)

def send_track(update, context):
    global users    
    wishes=update.message.text.split()[-1]
    print(wishes)
    
    ide = str(update.effective_chat.id)
    plin = str(users[ide][-1])
    
    for i in range(1, 20):
        song = song_catcher(plin, i, ide)
        print(song)
        if 'opus' in song:           
            context.bot.send_message(chat_id=update.effective_chat.id, text='Uploading...')    
            context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(song, 'rb'))
            os.remove(song)
    print('Enjoy vibes')
    context.bot.send_message(chat_id=update.effective_chat.id, text='Enjoy vibes!')    
def help_(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Send me the name of any music Album (e.g. Beatles Yellow Submarine) then send me /t and few words of thanks (e.g. /t SEND ME THIS ALBUM!!!). When I'll send you the whole album at its best!")

def main():
    updater = Updater("1212901280:AAEIKHfwxhf_V6dyPCs-I_RATwucKlXdnII", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_))
    dp.add_handler(CommandHandler("t", send_track))
    dp.add_handler(MessageHandler(Filters.text, parsing))

    updater.start_polling()
    updater.idle()

print("I'm alive")

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()