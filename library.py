import requests
import json
from itertools import permutations
from  tqdm import tqdm
from os import system


class Ehtimal:
    def __init__(self):
        self.nomreler = []

    def olasiliklari_hesapla(self):
        # 000'dan 999'a kadar olan tüm rakamları içeren bir liste oluştur
        self.nomreler = ['{:03d}'.format(i) for i in range(1000)]

    def getList(self):
        return self.nomreler

class AutoKey:
    def __init__(self, username, password):
        self.r = requests.Session()
        self.payload = {
        'username':username,
        'password':password
         }

        
    def getKey(self):
        res = self.r.post("https://public-api.azerconnect.az/api/authenticate", json=self.payload)
        key = str(json.loads(res.content)['id_token'])
        #print("myRealKey: ", key)
        return key
    

class Nar:
    def __init__(self):
        self.autoKey = AutoKey("824-0038", "samir9995099")
        self.url = "https://public-api.azerconnect.az/msazfposapptrans/api/msisdn-search"

    def narParams(self,page, number="xxxxxxx", prefix='70'):                                      # Local Function
        num = [
        number[0],                                            # Split part1                                  
        number[1],number[2],                                  # Split part2 
        number[3],number[4],                                  # Split part3
        number[5],number[6]]                                  # Split part4
        params = {"prefix":prefix,
            "a1":num[0].replace("x", ""),
            "a2":num[1].replace("x", ""),
            "a3":num[2].replace("x", ""),
            "a4":num[3].replace("x", ""),
            "a5":num[4].replace("x", ""),
            "a6":num[5].replace("x", ""),
            "a7":num[6].replace("x", ""),
            "prestigeLevel":"GENERAL",
            "size":2000,
            "page":page }
        return params
    
    def conNar(self, page, index = 0, prefix = '70'):
        try:
            params = self.narParams(page,prefix=prefix, number=f"xxxx{index}")
            r = requests.get(self.url,params=params,headers=self.setHeader(f"Bearer {self.autoKey.getKey()}"), timeout=3600)
        except requests.ConnectionError as e:
            print("İnternet bağlantınızda problem var! İnterneti yoxlayıb yenidən cəhd edin\n")
            print(str(e))            
        except requests.Timeout as e:
            print("Zaman aşımı! Məlumatlar serverdən alına bilmir!")
            print(str(e))
        except requests.RequestException as e:
            print("Ümumi xəta")
            print(str(e))
        except KeyboardInterrupt:
            print("Program dəyandırıldı")
        return r
    
    def loadNarData(self,page, index, prefix = '70'):
        narNumber = ""
        narCounter = 0
        narTwo = ""
        r = self.conNar(page, index=index, prefix=prefix)
        if(len(r.text) > 7):
            narData = json.loads(r.text)
        elif(r.status_code != 200):
            print("Key xətalıdır")
            exit(1)
        else:
            return ""
        for nar in narData:
            narTwo = (nar["msisdn"])
            narNumber = narNumber+narTwo[3:]+"\n"
            narCounter=narCounter+1
        return narNumber
    
    def setHeader(self, key):
        headers = {'content-type': 'application/json',         # Content type json
        'Accept':'application/json, text/plain, */*',          # Accept type json
        'Accept-Encoding':'gzip, deflate, br',                 # Encoding gzip compressed data
        'Accept-Language':'tr-TR,tr;q=0.9,az-TR;q=0.8,az;q=0.7,en-US;q=0.6,en;q=0.5',
        'Authorization': key,
        'Connection':'keep-alive'}
        return headers
    
class Work:
    def __init__(self):
        self.eht = Ehtimal()
        self.nar = Nar()

    def find_differences(self, new, old, prefix):
        # new'de bulunan ancak old'de bulunmayan öğeleri bulun
        differences = []

        for item in tqdm(new, desc=f"Checking Differences {prefix}"):
            if item not in old:
                differences.append(item)
        
        return differences

    def bol_liste(self, liste, parca_sayisi):
        # Listenin uzunluğunu hesapla
        liste_uzunlugu = len(liste)

        # Her bir parçada minimum eleman sayısını ve fazla elemanı hesapla
        parca_uzunlugu = liste_uzunlugu // parca_sayisi
        fazla_eleman = liste_uzunlugu % parca_sayisi

        bolunmus_liste = []
        baslangic = 0

        for i in range(parca_sayisi):
            bitis = baslangic + parca_uzunlugu + (1 if i < fazla_eleman else 0)
            bolunmus_liste.append(liste[baslangic:bitis])
            baslangic = bitis

        return bolunmus_liste

    def parcala(self, input_list, list_part, index):
        return self.bol_liste(liste=input_list, parca_sayisi=list_part)[index]

    def all_number_data(self, calc:str, prefix = "70"):
        self.eht.olasiliklari_hesapla()
        counter_page = 0
        number_list = ""
        number_temp_list = ""
        with tqdm(total=1000, desc="\nİlerleme") as pbar:
            while True:
                print(f"Prefix: {prefix}\n")
                print(f"Seriya: XXXX{calc}\n")
                print(f"Səhifə sayı: {counter_page}\n")
                number_temp_list = self.nar.loadNarData(counter_page,calc, prefix=prefix)
                if(not number_temp_list):
                    print(f"Nömrə sayı: {str(len(number_list))[:-1]}\n")
                    break
                else:
                    for number in tqdm(number_temp_list.split("\n"), desc=f"\n{counter_page} səhifədəki nömrələr"):
                        if(len(number) > 2):
                            number_list += number+"\n"
                counter_page+=1
                pbar.update(1)  # İlerlemeyi güncelle
                system("clear")
        return number_list
