"""
    Developper: Ramiz Mammadli
"""
from main_function import MF
import threading
import datetime
import time
import ext
import os

class Command:
    def __init__(self, bot):
        self.bot = bot
        self.work = Work(bot)
        self.mf = MF()
    def initCommand(self, command_type, chat_id, chat_type):
        self.command_type = command_type
        self.chat_id = chat_id
        self.chat_type = chat_type
        self.work.init(chat_id)
      
    def getCommand(self, command):
        if(self.command_type == 'document'):
            self.documentFile(command["document"])
        elif(self.command_type == 'text'):
            print(f"Command: {command['text']}")
            self.set_command(command["text"])

    def set_command(self, command):
        if(self.filter(command) == "/start" or self.filter(command) == "/help"):
            self.bot.sendMessage(self.chat_id, ext.msg)
        elif(self.filter(command) == "/replace"):
            self.bot.sendMessage(self.chat_id, "Yüklənmiş datalar köhnə olaraq qeyd edildi")
            self.mf.replace_old()
        elif(self.filter(command) == "/numbers"):
            self.work.numbers()
        elif(self.filter(command) == "/getlist"):
            self.work.getList()
        elif(self.filter(command) == "/list"):
            self.work.makeList()
        elif(self.filter(command) == "/calculate"):
            self.work.calculate()
        else:
            self.bot.sendMessage(self.chat_id, str("Əmr yanlışdır!"))

    def textFile(self, file):
        pass
    def documentFile(self, file):
        print(file)
    def imageFile(self, file):
        pass
    def soundFile(self, file):
        pass
    def filter(self, inp = ""):
        return inp.lower()
   
class Work:
    def __init__(self, bot):
        self.bot = bot
        self.mf = MF()
    def init(self, chat_id):
        self.chat_id = chat_id

    def print(self, msg:str):
        self.bot.sendMessage(self.chat_id, msg)
    def sendDocument(self, document):
        self.bot.sendDocument(self.chat_id, document=document)


    def numbers(self):
        if(os.path.exists("70_new.txt") and os.path.exists("77_new.txt")):
            file = open("70_new.txt", "r")
            file1 = open("77_new.txt", "r")
            data = file.read()
            data1 = file1.read()
            self.print(f"070 Prefix: \n{data}\n077 Prefix: \n{data1}\n")
        else:
            self.print("Yeni nömrələr yoxdur!")

    def getList(self):
        self.print("Datalar yüklənir biraz gözləyin")
        if(os.path.exists("70_new.txt") and os.path.exists("77_new.txt")):
            self.sendDocument(document=open("70_new.txt"))
            self.sendDocument(document=open("77_new.txt"))
        else:
            self.print("Fayllar tapılmadı.")

    def makeList(self):
        self.print("Datalar yüklənir biraz gözləyin")
        thread = threading.Thread(target=self.mf.run)
        thread1 = threading.Thread(target=self.log)
        thread.start()
        thread1.start()
        thread.join()
        thread1.join()
        self.print("Datalar yükləndi")


    
    def log(self):
         while True:
            if(str(self.mf.data_counter) == "999" and self.mf.data_counter1 == "999"):
                print("Durdu")
                self.print("Yükləmə tamamlandı")
                break
            time.sleep(60)
            self.print(f"-------------------------------\n070: {self.mf.data_counter}")
            self.print(f"077: {self.mf.data_counter1}")

    def calculate(self):
        self.print("Hesablama başladılır...")
        if(os.path.exists("70.txt") and os.path.exists("77.txt")):
            if(os.path.exists("70_old.txt") and os.path.exists("77_old.txt")):
                
                thread = threading.Thread(target=self.mf.calc_run)
                thread.start()
                thread.join()
                if(os.path.exists("70_new.txt") and os.path.exists("77_new.txt")):
                    self.sendDocument(document=open("70_new.txt", "rb"))
                    self.sendDocument(document=open("77_new.txt", "rb"))
                else:
                    print("Fayllar tapılmadı.")
            else:
                self.print("Siz dataları köhnə data olaraq qeyd etməlisiniz. Bunun üçün /replace əmrini çalışdırın.")
        else:
            self.print("Köhnə datalar ilə qarşılaşdırılacaq yeni data yoxdur. Yeni data yükləmək üçün /list yazıb gözləyin")
      

