# arayuz.py
import tkinter as tk
from tkinter import ttk
from graf_cizdir_modul import Graf
import json
import random

# JSON dosyasından veriyi oku
with open('kullanicilar.json', 'r') as json_dosyasi:
    veri = json.load(json_dosyasi)

# Graf sınıfını oluştur
graf = Graf()

# Kullanıcı adlarına random renkleri belirle
renkler = {kullanici['kullanici_adi']: "#{:06x}".format(random.randint(0, 0xFFFFFF)) for kullanici in veri}

# Her kullanıcı için düğüm eklemeyi ve takipçi-takip edilen ilişkilerini kenar olarak eklemeyi dene
for kullanici in veri:
    kullanici_adi = kullanici['kullanici_adi']

    if kullanici_adi not in [dugum.adi for dugum in graf.dugumler]:
        renk = renkler[kullanici_adi]
        graf.dugum_ekle(kullanici_adi, renk)

    for takip_edilenler in kullanici['takip_edilenler']:
        takip_edilen_renk = renkler.get(takip_edilenler, "#{:06x}".format(random.randint(0, 0xFFFFFF)))
        graf.dugum_ekle(takip_edilenler, takip_edilen_renk)
        graf.kenar_ekle(kullanici_adi, takip_edilenler)

    for takipciler in kullanici['takipciler']:
        takipci_renk = renkler.get(takipciler, "#{:06x}".format(random.randint(0, 0xFFFFFF)))
        graf.dugum_ekle(takipciler, takipci_renk)
        graf.kenar_ekle(takipciler, kullanici_adi)

# GUI oluşturma
pencere = tk.Tk()
pencere.title("Kullanıcı İlişkileri Grafi")

# Grafiği çizme fonksiyonu
def graf_goster():
    graf.graf_cizdir(renkler)

# Grafiği çizme butonu
buton_graf_ciz = tk.Button(pencere, text="Grafı Göster", command=graf_goster)
buton_graf_ciz.pack(pady=10)

# Takipçi sayısına göre analiz butonu ve fonksiyonu
def takipci_analiz():
    graf.analizi_goster(veri)

buton_takipci_analiz = tk.Button(pencere, text="Takipçi Sayısına Göre Analiz", command=takipci_analiz)
buton_takipci_analiz.pack(pady=10)

# Pencereyi çalıştırma
pencere.mainloop()
