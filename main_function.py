from library import Work, Ehtimal
from tqdm import tqdm
from os import system
import concurrent.futures
from pyee import EventEmitter
import os

work = Work()
ehtimal = Ehtimal()
narNumber = []
defaultPrefix = ""
new77 = []
new70 = []

ehtimal.olasiliklari_hesapla()
data_counter = 0
status = False
status_calculate = False


def load_count(count:int):
    global data_counter
    data_counter = count


def setPrefix(prefix:str):
    defaultPrefix = prefix

def load_status(_status:bool):
    global status
    status=_status


def calc_status(_status:bool):
    global status_calculate
    status_calculate =_status

def replace_old():
    system("mv 70.txt 70_old.txt")
    system("mv 77.txt 77_old.txt")


def load(prefix = "70"):
    load_status(True)
    file_name = ""
    pref = ""
    if(prefix == "70"):
        file_name = "70.txt"
        pref = "70"
    else:
        file_name = "77.txt"
        pref = "77"
    nomre_sayi = 0  # Yerel değişken olarak tanımla
    system(f"rm {file_name}")
    for calc in tqdm(ehtimal.getList(), desc="\nEhtimal edilən prefixlər"):
        temp_number = work.all_number_data(calc=calc, prefix=pref)
        nomre_sayi += len(temp_number)
        with open(file_name, 'a+') as dosya:
            for all_number in tqdm(temp_number.splitlines(), desc="\nSəhifədəki bütün nömrələr"):
                dosya.write(str(all_number) + '\n')
        load_count(calc)
    print(f"Tapılan ümumi nömrə sayı: {str(nomre_sayi)[:-1]}\n")
    load_status(False)
    return nomre_sayi  # Sonucu geri döndür

def task(id):
    if id == 0:
        result = load("70")
    else:
        result = load("77")
    return result

def run():
    # ThreadPoolExecutor ile iş parçacıkları oluştur
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 2 farklı görevi iş parçacıkları aracılığıyla çalıştır
        results = list(executor.map(task, range(0, 2)))

    # Her görevin sonucu
    for result in results:
        print(result)



def _calc_task(id):
    if id == 0:
        result = calculate("70")
    else:
        result = calculate("77")
    return result

def calc_run():
    # ThreadPoolExecutor ile iş parçacıkları oluştur
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 2 farklı görevi iş parçacıkları aracılığıyla çalıştır
        results = list(executor.map(_calc_task, range(0, 2)))

    # Her görevin sonucu
    for result in results:
        print(result)



def calculate(prefix="70", part = 0):

    new_save_070 = open("70_new.txt","w")
    new_save_077 = open("77_new.txt","w")

    global new70, new77
    calc_status(True)

    # if os.path.exists("70_new.txt") and os.path.exists("77_new.txt"):
    #     os.remove("70_new.txt")
    #     os.remove("77_new.txt")


    if prefix == "70":
        print("70")
        new = open("70.txt","r")
        old = open("70_old.txt","r")
    else:
        print("77")
        new = open("77.txt","r")
        old = open("77_old.txt","r")
    new_list = new.readlines()
    old_list = old.readlines()
    if(prefix == "70"):
        new70 = work.find_differences(new_list, old_list)
    else:
        new77 = work.find_differences(new_list, old_list)
    for y0, y77 in zip(new70,new77):
        new_save_070.write(y0)
        new_save_077.write(y77)
        print(f"Yeni 070: {y0}")
        print(f"Yeni 077: {y77}")

    calc_status(False)

