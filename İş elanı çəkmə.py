import requests
from bs4 import BeautifulSoup
import pandas as pd
 
liste = []
base = "https://www.hellojob.az/vezifeler"
head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}
response  = requests.get(base,headers=head)
print(response.status_code)
html = BeautifulSoup(response.text,"html.parser")
data = html.find_all("div",class_ = "position-item")
 
for veri in data:
    basliq = veri.find("a").text.strip()
    link = veri.find("a")["href"]
    link_full = f"https://www.hellojob.az{link}"
 
    company = requests.get(link_full,headers=head)
    hmm = BeautifulSoup(company.text,"html.parser")
    malum = hmm.find_all("div",class_ = "position-salary-item position-salary-stat-item")
    
    for big in malum:
        if "Ən aşağı" in big.text:
            asagi = big.find("p", class_="pss-salary").text.strip()
        elif "Orta" in big.text:
            orta = big.find("p", class_="pss-salary").text.strip()
        elif "Ən yüksək" in big.text:
            yuxari = big.find("p", class_="pss-salary").text.strip()
    
    liste.append([basliq.upper(), asagi, orta, yuxari])
 
# Verileri pandas DataFrame'e çevirme
df = pd.DataFrame(liste, columns=["Başlıq", "Ən aşağı", "Orta", "Ən yüksək"])
df.to_excel("hellojob.xlsx",index=False)
