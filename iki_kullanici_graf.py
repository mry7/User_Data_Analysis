import tkinter as tk
from tkinter import messagebox
import json
import networkx as nx
import matplotlib.pyplot as plt
import random


#json dosyasından kullanıcıları çekeriz
def jsondan_kullanicilari_yukle(json_file):
    with open(json_file, "r") as file:
        kullanicilar_veri = json.load(file)
    
    kullanicilar = []
    # (kullanicilar_veri) adlı bir liste içindeki her bir (veri) öğesini ele alır.
    for veri in kullanicilar_veri:
        kullanici = {
            # Her bir (veri) öğesinden, "Username" anahtarına karşılık gelen değeri alır
            # ve "Followers" ve "Following" anahtarlarına karşılık gelen değerleri alır
            # Elde edilen bilgilerle bir sözlük oluşturur: "Username", "Followers", "Following".
            "Username": veri["Username"],
            "Followers": veri.get("Followers", []),
            "Following": veri.get("Following", [])
            # Diğer bilgileri ekleyebilirsiniz
        }
        # Oluşturulan sözlüğü kullanicilar adlı liste içine ekler.
        kullanicilar.append(kullanici)
    
    return kullanicilar

#girilen 2 kullanıcı düğüm, diğer ilişkiler kenarları temsil eder
def graf_olustur(users):
    B = nx.DiGraph()

# (users) adlı liste içindeki her bir (kullanıcı) için bir düğüm (node) oluşturur.
    for kullanici in users:
        B.add_node(kullanici["Username"])
        # Her bir düğümün rengini rastgele bir renk olarak atar ve "username" ile eşleştirir.
        B.nodes[kullanici["Username"]]["color"] = "#{:06x}".format(random.randint(0, 0xFFFFFF))

# Her bir kullanıcının "Followers" listesinde bulunan kullanıcılar ile takip edildiği ilişkileri temsil eden kenarları ekler.
        for follower in kullanici["Followers"]:
            B.add_edge(follower, kullanici["Username"])

# Her bir kullanıcının "Following" listesinde bulunan kullanıcılar ile takip ettiği ilişkileri temsil eden kenarları ekler.            
        for following in kullanici["Following"]:
            B.add_edge(kullanici["Username"], following)

# oluşturulan yönlendiirlmiş graf (digraph) nesnesi döndürülüyor.
    return B

#Verilen kullanıcıların takipçilerini bulup kesişimini alarak ortak takipçileri belirler
def ortak_takipçileri_bul(graph, kul1, kul2):
    # graph nesnesinden, kul1 adlı kullanıcının takipçilerini (predecessors) bulur 
    # ve bir küme (set) olarak kul1_takipcileri adlı değişkene atar.
    kul1_takipcileri = set(graph.predecessors(kul1))
    kul2_takipcileri = set(graph.predecessors(kul2))
    # kümeleri arasındaki kesişimi (intersection) alır ve ortak_takipciler adlı değişkene atar.
    ortak_takipciler = kul1_takipcileri.intersection(kul2_takipcileri)

    # ortak_takipciler kümesini bir listeye çevirerek
    return list(ortak_takipciler)

#Oluşturulan grafiği görselleştirir, grafik nesnesini döndürür
def grafi_gosrellestirr(graph, users, ortaklar):
    plt.figure()
    pos = nx.spring_layout(graph)

    # Düğümlerin renklerini belirle
    dugum_renkleri = [graph.nodes[node].get('color', '#CCCCCC') for node in graph.nodes]


    # Ortak takipçileri vurgula
    nx.draw_networkx_nodes(graph, pos, nodelist=ortaklar, node_size=900, node_color='#00FF00', label="Ortak Takipçiler")

    nx.draw(graph, pos, with_labels=True, font_size=7, node_size=900, node_color=dugum_renkleri, font_color="black", font_weight="bold")
    plt.title("Girilen kullanıcıların ilişki grafiği")
    plt.legend()
    return plt

def on_button_click(entry1, entry2):
    isim1 = entry1.get()
    isim2 = entry2.get()

    if isim1 == isim2:
        messagebox.showerror("Hata", "Lütfen farklı iki kullanıcı adı girin.")
        return

    #seçilmiş kişiler
    sec_kisi = [user for user in tüm_kullanicilar if user["Username"] in [isim1, isim2]]

   

    M = graf_olustur(sec_kisi)
    orrtak_takipciler = ortak_takipçileri_bul(M, isim1, isim2)

    plt = grafi_gosrellestirr(M, [isim1, isim2], orrtak_takipciler)
    plt.show()

# Arayüz oluştur
root = tk.Tk()
root.title("Kullanıcı Karşılaştırma Grafiği")

# Kullanıcıları çek(Json'dan)
tüm_kullanicilar = jsondan_kullanicilari_yukle("C:/Users/meryem/html dersleri/.vscode/deneme/kullanicilar.json")

# Kullanıcı adı giriş kutularını oluştur
label1 = tk.Label(root, text="1. Kullanıcının ismi:")
entry1 = tk.Entry(root)
label2 = tk.Label(root, text="2. Kullanıcnın ismi:")
entry2 = tk.Entry(root)

# Butonu oluştur
button = tk.Button(root, text="Grafiği Çizdir", command=lambda: on_button_click(entry1, entry2))

# Arayüzdeki bileşenleri yerleştir
label1.pack()
entry1.pack()
label2.pack()
entry2.pack()
button.pack(pady=10)

# Arayüzü başlat
root.mainloop()
