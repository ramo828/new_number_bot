from command import Command
from main_function import MF
import telepot
import time
import os
# Telegram botunuzun tokenini buraya ekleyin
"""
    Developper: Ramiz Mammadli
"""
mf = MF()
token = os.environ.get("my_token")
bot_init = telepot.Bot(token)
com = Command(bot_init)

def handle(msg):
    content_type = telepot.glance(msg)[0]
    chat_type = telepot.glance(msg)[1]
    chat_id = telepot.glance(msg)[2]
    com.initCommand(
        chat_id=chat_id, 
        chat_type=chat_type, 
        command_type=content_type)
    com.getCommand(msg)
   
bot_init.message_loop(handle)
print('Əmrlər gözlənilir...')

while 1:
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        print('\n Program sonlandı')
        exit()
    except:
        print('Xəta')