from library import Worker, Ehtimal
from tqdm import tqdm
from os import system
import concurrent.futures
import time
import os

class MF:

    def __init__(self):

        self.ehtimal = Ehtimal()
        self.narNumber = []
        self.defaultPrefix = ""
        self.new77 = []
        self.new70 = []
        self.ehtimal.olasiliklari_hesapla()
        self.data_counter = 0
        self.data_counter1 = 0
        self.status = False
        self.status_calculate = False
        self.gecen_sure = ""
        self.gecen_sure1 = ""
        self.work = Worker()

    def load_count(self, count:int, prefix = "70"):
        if(prefix == "70"):
            self.data_counter = count
        else:
            self.data_counter1 = count


    def setPrefix(self, prefix:str):
        self.defaultPrefix = prefix

    def load_status(self, _status:bool):
        self.status=_status

    def getStatus(self,):
        return self.status

    def getCalcStatus(self ):
        return self.status_calculate

    def calc_status(self, _status:bool):
        self.status_calculate =_status

    def replace_old(self):
        system("mv 70.txt 70_old.txt")
        system("mv 77.txt 77_old.txt")

    def load(self, prefix = "70"):
        # self.message("Basladiq")
        self.load_status(True)
        self.baslangic_zamani = time.time()
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
        for calc in tqdm(self.ehtimal.getList(), desc="\nEhtimal edilən prefixlər"):
            temp_number = self.work.all_number_data(calc=calc, prefix=pref)
            nomre_sayi += len(temp_number)
            with open(file_name, 'a+') as dosya:
                for all_number in tqdm(temp_number.splitlines(), desc="\nSəhifədəki bütün nömrələr"):
                    dosya.write(str(all_number) + '\n')
            self.load_count(calc, prefix=pref)
        print(f"Tapılan ümumi nömrə sayı: {str(nomre_sayi)[:-1]}\n")
        self.load_status(False)
        self.bitis_zamani = time.time()
        self.gecen_sure = self.bitis_zamani - self.baslangic_zamani
        return nomre_sayi  # Sonucu geri döndür

    def task(self, id):
        if id == 0:
            result = self.load("70")
        else:
            result = self.load("77")
        return result

    def run(self):
        # ThreadPoolExecutor ile iş parçacıkları oluştur
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 2 farklı görevi iş parçacıkları aracılığıyla çalıştır
            results = list(executor.map(self.task, range(0, 2)))

        # Her görevin sonucu
        for result in results:
            print(result)



    def _calc_task(self, id):
        if id == 0:
            result = self.calculate("70")
        else:
            result = self.calculate("77")
        return result

    def calc_run(self):
        # ThreadPoolExecutor ile iş parçacıkları oluştur
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 2 farklı görevi iş parçacıkları aracılığıyla çalıştır
            results = list(executor.map(self._calc_task, range(0, 2)))

        # Her görevin sonucu
        for result in results:
            print(result)



    def calculate(self, prefix="70", part = 0):
        new_save_070 = open("70_new.txt","w")
        new_save_077 = open("77_new.txt","w")
        self.calc_status(True)
        self.baslangic_zamani = time.time()


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
            self.new70 = self.work.find_differences(new_list, old_list, prefix)
        else:
            self.new77 = self.work.find_differences(new_list, old_list, prefix)
        for y0, y77 in zip(self.new70,self.new77):
            new_save_070.write(y0)
            new_save_077.write(y77)
            print(f"Yeni 070: {y0}")
            print(f"Yeni 077: {y77}")
        self.bitis_zamani = time.time()
        self.gecen_sure1 = self.bitis_zamani - self.baslangic_zamani
        self.calc_status(False)

