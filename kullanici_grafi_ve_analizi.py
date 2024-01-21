import tkinter as tk
from tkinter import messagebox
import json
import random
import networkx as nx
import matplotlib.pyplot as plt

def load_userss_fromm_json(json_file):
    with open(json_file, "r") as f:
        return json.load(f)

#Her kullanıcıyı bir düğüm, takipçi-takip edilen ilişkileri kenar olarak tanımlayan ağ grafiği
def graf_olustur(kullanicilarr):
    A = nx.DiGraph()
    
    # Her kullanıcıyı düğüm olarak ekle
    for kullanici in kullanicilarr:
        A.add_node(kullanici["Username"])

        # Renk bilgisini düğüme ekle
        A.nodes[kullanici["Username"]]["color"] = "#{:06x}".format(random.randint(0, 0xFFFFFF))

        # Takipçi-takip edilen ilişkilerini kenar olarak ekle
#  Her bir kullanıcının "Followers" listesinde bulunan kullanıcılar ile takip edildiği ilişkileri temsil eden kenarları ekler.        
        for takip_eden in kullanici["Followers"]:
            A.add_edge(takip_eden, kullanici["Username"])
# Her bir kullanıcının "Following" listesinde bulunan kullanıcılar ile takip ettiği ilişkileri temsil eden kenarları ekler.            
        for takip_ettigi in kullanici["Following"]:
            A.add_edge(kullanici["Username"], takip_ettigi)

    return A

# Bir kullanıcıdan belirli seviyeye kadar ilişkili diğer kullanıcıları buldurur
# BFS algoritmasını kullanır.
def ayniseviyedekikullanicilari_bul(graph, ilk_kullanici, level):
    explored = set()
    # başlangıç kullanıcısını ve başlangıç durumunu (0) içeren bir kuyruk oluşturulur.
    queue = [(ilk_kullanici, 0)]
    # kuyruk boş olana kadar işlemlere devam eder.
    result = []

    while queue:
        # Kuyruktan bir kullanıcı ve mevcut durum (seviye) çıkarılır.
        user, mevcut_durum = queue.pop(0)
        explored.add(user)

# Bu kullanıcı keşfedildi (explored) olarak işaretlenir ve mevcut durum, belirlenen seviyeye ulaşılmışsa sonuç listesine eklenir.
        if mevcut_durum == level:
            result.append(user)
# Eğer mevcut durum belirlenen seviyeden küçükse, kullanıcının komşuları (neighbors) incelenir. 
        if mevcut_durum < level:
            neighbors = graph.neighbors(user)
            for neighbor in neighbors:
                #  Her bir komşu, daha önce keşfedilmemişse kuyruğa eklenir ve mevcut durum + 1 ile işaretlenir.
                if neighbor not in explored:
                    queue.append((neighbor, mevcut_durum + 1))

    return result

# Kullanıcıları düğümler olarak, takipçi-takip edilen ilişkileri ise kenarlardır
def grafı_gorsellestir(graph):
    plt.figure()
    pos = nx.spring_layout(graph)

    # Düğümlerin renklerini belirle
    dugum_renkleri = [graph.nodes[node].get('color', '#CCCCCC') for node in graph.nodes]
    
    nx.draw(graph, pos, with_labels=True, font_size=7, node_size=900, node_color=dugum_renkleri, font_color="black", font_weight="bold")
    plt.title("Takipçi-Takip Edilen Kullanıcların İlişkileri Grafiği")
    return plt

#Butona tıklandığında seçilen rastgele 10 kişinin grafını çizdirir, analizini yapar
def on_button_click():
    #  seçilmiş 10 kullanıcıdan oluşan bir listeyi (secilmis_kullanicilar) alır
    secilmis_kullanicilar = random.sample(tum_kullanicilar, 10)
    #seçilmiş kullanıcıalr ile grafı oluşturuyor
    B = graf_olustur(secilmis_kullanicilar)
    ilk_kisi = secilmis_kullanicilar[0]["Username"]
    # seçilen kullanıcı ile aynı seviyede (level=1) olan diğer kullanıcılar belirlenir ve (ayni_seviyeli_kullanicilar) listesi oluşturulur.
    ayni_seviyeli_kullanicilar = ayniseviyedekikullanicilari_bul(B, ilk_kisi, level=1)

    plt = grafı_gorsellestir(B)
    plt.show()

    messagebox.showinfo("Sonuç", f"{ilk_kisi} kullanıcı ile seviyesi aynı olan diğer kullanıcılar: {ayni_seviyeli_kullanicilar}")

# Arayüz oluşturuluyor(tkinter)
root = tk.Tk()
root.title("Kullanıcı Analizi")

# JSON dosyasından kullanıcıları yükle
tum_kullanicilar = load_userss_fromm_json(r"C:/Users/meryem/html dersleri/.vscode/deneme/kullanicilar.json")

# Buton oluştur
button = tk.Button(root, text="Analize Başla", command=on_button_click)
button.pack(pady=10)

# Arayüzü başlat
root.mainloop()
