from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from main_function import run, calc_run, replace_old
import main_function
import threading
import asyncio
import logging
import time
import sys
import os


if __name__ == "__main__":

    token = os.environ.get("my_token")
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Loglama için bir logger oluşturun
    logger = logging.getLogger(__name__)

    async def help_h(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(f'Salam {update.effective_user.first_name}\nNömrələri yükləmək üçün /list yazıb əməlliyatın bitməsini gözləyin. Bir neçə dəqiqədən bir sizə bitiş sayğacı göstəriləcək. Sayğac 999 olduqda tamamlanır. Hesablama, yəni yeni nömrələri tapmaq üçün /calculate yazın. Yeni yüklədiyiniz listi işləmisinizsə köhnə datanı yeni ilə əvəzləyə bilərsiniz. Bunun üçün /replace yazmaq kifayetdir. Əğər heç bir bildirş gəlmirsə və siz o an hansı prosesin getdiyini və ya getmediyini bilmirsinizsə o zaman /check yazaraq o an aktiv prosesi, və prosesin hansı mərhələdə olduğunu görə bilərsiniz. Əməliyyatlar biraz zaman ala bilər. Bunun üçün biraz səbrli olun. Əməliyyatlar bitdikdən sonra sizə bildiriş göndərəcəyik. Uğurlar')
        
    # 1. Boş Komut
    async def make_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if main_function.calc_status == False:
            await update.message.reply_text("Nömrə listəsi hazirlanir")
            logger.info("Uzun süren işlem başladı")
            # Uzun süren işlemi farklı bir thread'de çalıştır
            thread = threading.Thread(target=run)
            thread.start()
            while main_function.status:
                if main_function.status == False:
                    await update.message.reply_text(f"List hazırlama bitdi. Əməliyyat {main_function.gecen_sure} tamamlandı")
                await time.sleep(62)
                print(main_function.data_counter)
                await update.message.reply_text(str(main_function.data_counter))
                
            logger.info("Uzun süren işlem tamamlandı")
        else:
            await update.message.reply_text("Hesablama davam edir")

        
    async def replace(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Yeni köhnə datalar ilə dəyişdi.")
        replace_old()
        
    
    async def get(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Datalar yüklənir. Biraz gözləyin..")
        if(os.path.exists("70_new.txt") and os.path.exists("77_new.txt")):
            await update.message.reply_document(document=open("70_new.txt", "rb"))
            await update.message.reply_document(document=open("77_new.txt", "rb"))
        else:
            await update.message.reply_text("Fayllar tapılmadı.")
        


    async def numbers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if(os.path.exists("70_new.txt") and os.path.exists("77_new.txt")):
            file = open("70_new.txt", "r")
            file1 = open("77_new.txt", "r")
            data = file.read()
            data1 = file1.read()
            await update.message.reply_text(f"070 Prefix: \n{data}\n077 Prefix: \n{data1}\n")
        else:
            await update.message.reply_text("Yeni nömrələr yoxdur!")


    async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if(main_function.status):
            await update.message.reply_text(f"Yüklənmə davam edir...\n {main_function.data_counter}")

            time.sleep(1)
            await update.message.reply_text(f"{main_function.data_counter}")
        elif(main_function.status_calculate):
            await update.message.reply_text("Hesablanma davam edir...")
        else:
            await update.message.reply_text("Aktiv heç bir əməliyyat yoxdur")




    async def calculate_func(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if main_function.status ==  False:
            await update.message.reply_text("Hesablama aparılır...")
            logger.info("Uzun süren işlem başladı")
            # Uzun süren işlemi farklı bir thread'de çalıştır
            thread1 = threading.Thread(target=calc_run)
            thread1.start()
            while main_function.status_calculate:
                if  main_function.status_calculate == False:
                    await update.message.reply_text(f"Hesablama bitdi. Hesabalama {main_function.gecen_sure1} tamamlandı")
                time.sleep(62)
                await update.message.reply_text("Hesablama davam edir...")
            time.sleep(5)
        
            time.sleep(1)
            logger.info("Uzun süren işlem tamamlandı")
            if(os.path.exists("70_new.txt") and os.path.exists("77_new.txt")):
                await update.message.reply_document(document=open("70_new.txt", "rb"))
                await update.message.reply_document(document=open("77_new.txt", "rb"))
            else:
                await update.message.reply_text("Fayllar tapılmadı.")

        else:
            await update.message.reply_text("Yükləmə davam edir...")


    app = ApplicationBuilder().token(token=token).build()

    app.add_handler(CommandHandler("help", help_h))
    app.add_handler(CommandHandler("calculate", calculate_func))
    app.add_handler(CommandHandler("list", make_list))
    app.add_handler(CommandHandler("replace", replace))
    app.add_handler(CommandHandler("numbers", numbers))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CommandHandler("get", get))


    app.run_polling()
