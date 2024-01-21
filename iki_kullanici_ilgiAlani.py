import json
import tkinter as tk
from kategoriler import kkategorilerr


# JSON dosyasını oku
with open('kullanicilar.json', 'r', encoding='utf-8') as dosyaa:
    json_dosyasi_veri = json.load(dosyaa)

# Kullanıcı bulma fonksiyonu
def kullaniciyi_bull(kullanicii_adii):
    for kullaniicii in json_dosyasi_veri:
        if kullaniicii['Username'] == kullanicii_adii:
            return kullaniicii
    return None

#Kategori bulma fonksiyonu
#Bu fonksiyon, verilen bir kelimenin (kelimee) hangi kategoriye (kategorii) ait olduğunu belirlemek için kullanılır. 
#(kkategorilerr) içinde dolaşarak (bir_kategori_Listesindeki_Kelimeler)de bulunup bulunmadığını kontrol eder.
#Eğer bulunursa ilgili kategori adını(kategorii) döndürür, bulunmazsa None değerini döndürür.
def kullanicinin_kategorisini_bul(kelimee, kkategorilerr):
    for kategorii, bir_kategori_Listesindeki_Kelimeler in kkategorilerr.items():
        if kelimee in bir_kategori_Listesindeki_Kelimeler:
            return kategorii
    return None

# Kullanıcının ilgi alanlarını frekanslarıyla belirleyen fonksiyon
def kullanicinin_ilgi_alanlarii(kullanicii_adii, kkategorilerr):
    kullaniicii = kullaniciyi_bull(kullanicii_adii)

    if kullaniicii is None:
        print("Kullanıcı bulunamadı!")
        return None

    tweetlerrr = kullaniicii['Tweets']

    # Tweetlerdeki kelimelerin frekansını kategori bazında hesapla
    # Boş bir sözlük oluşturulur bu sözlük, her kategorideki kelime sayılarını tutar
    kelimee_sayiisii = {}
    # (tweetlerrr) listesindeki her bir tweet için döngü başlatılır.
    # ve (kelimee) bakarak . kelimenin hangi (kategorii)ye ait olduğu bulunmaya çalışılır
    for tweet in tweetlerrr:
        for kelimee in tweet.split():
            kategorii = kullanicinin_kategorisini_bul(kelimee, kkategorilerr)
            if kategorii:
                # Sözlüğe kategori ekleme veya güncelleme
                kelimee_sayiisii[kategorii] = kelimee_sayiisii.get(kategorii, 0) + 1
# döngüler tamamlandıktan sonra, kategorilere göre kelime sayılarını içeren sözlük (kelimee_sayiisii) return ediliyor.
    return kelimee_sayiisii

# BFS ile ortak ilgi alanlarına sahip diğer kullanıcıları bulma
def digerr_kullanicilarii_bull(baslangic_kullanicisi, kkategorilerr, tumm_kullanicilarr):
    kumee = set()
    ziyaret_edilen_kullanici_listesi = [baslangic_kullanicisi]
    baslangic_kullniciyla_ortak_ilgi_kumesi = set()

    while ziyaret_edilen_kullanici_listesi:
        suankii_kullanicii = ziyaret_edilen_kullanici_listesi.pop(0)
        # Eğer (suankii_kullanicii) zaten ziyaret edilmişse, döngüye devam et.
        if suankii_kullanicii in kumee:
            continue
        # (kumee) kümesine (suankii_kullanicii) ekleniyor.
        kumee.add(suankii_kullanicii)
        # (kullanicinin_ilgi_alanlarii) fonksiyonu kullanılarak (suankii_kullanicii)'nin ilgi alanları alınıyor.
        suanki_ilgi_alani = kullanicinin_ilgi_alanlarii(suankii_kullanicii, kkategorilerr)

        for kullaniicii in tumm_kullanicilarr:
            # Eğer kullanıcı (suankii_kullanicii) değilse ve daha önce ziyaret edilmemişse
            if kullaniicii['Username'] != suankii_kullanicii and kullaniicii['Username'] not in kumee:
                digerlerin_ilgi_alani = kullanicinin_ilgi_alanlarii(kullaniicii['Username'], kkategorilerr)
                # İki kullanıcının ilgi alanları arasında ortak olanları bulmak için set'ler kullanılıyor.
                ortakk_ilgii = set(suanki_ilgi_alani.keys()).intersection(digerlerin_ilgi_alani.keys())
                # Eğer ortak ilgi alanları varsa, diğer kullanıcı baslangic_kullniciyla_ortak_ilgi_kumesi kümesine ekleniyor 
                # ve ziyaret_edilen_kullanici_listesi'ne ekleniyor.
                if ortakk_ilgii:
                    baslangic_kullniciyla_ortak_ilgi_kumesi.add(kullaniicii['Username'])
                    ziyaret_edilen_kullanici_listesi.append(kullaniicii['Username'])
                    # döngüsü tamamlandığında, (baslangic_kullniciyla_ortak_ilgi_kumesi) return ediliyor. 
                    # Bu küme, başlangıç kullanıcısı ile ortak ilgi alanlarına sahip diğer kullanıcıları içerir.
    return baslangic_kullniciyla_ortak_ilgi_kumesi

# Tkinter arayüzü oluştur
arayuzz = tk.Tk()
arayuzz.title("Kullanıcı İlgi Alanları")

# Kullanıcı adı giriş kutuları
label_kullaniicii1 = tk.Label(arayuzz, text="1. Kullanıcı Adı:")
entry_kullaniicii1 = tk.Entry(arayuzz)
label_kullaniicii2 = tk.Label(arayuzz, text="2. Kullanıcı Adı:")
entry_kullaniicii2 = tk.Entry(arayuzz)

label_kullaniicii1.grid(row=0, column=0, padx=6, pady=6)
entry_kullaniicii1.grid(row=0, column=1, padx=6, pady=6)
label_kullaniicii2.grid(row=1, column=0, padx=6, pady=6)
entry_kullaniicii2.grid(row=1, column=1, padx=6, pady=6)

# Bilgi gösterme alanı
textbox = tk.Text(arayuzz, height=25, width=60)
textbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# İlgi alanlarını gösterme fonksiyonu
def ilgii_alanlarinii_goster():
    kullaniicii1 = entry_kullaniicii1.get()
    kullaniicii2 = entry_kullaniicii2.get()

    # Her bir kullanıcı için ilgi alanlarını frekanslarıyla belirle
    ilgi_alanlarii_kullaniicii1 = kullanicinin_ilgi_alanlarii(kullaniicii1, kkategorilerr)
    ilgi_alanlarii_kullaniicii2 = kullanicinin_ilgi_alanlarii(kullaniicii2, kkategorilerr)


 # Dosyaya yazdır
    with open("ortak_ilgi_alanlari.txt", "w", encoding="utf-8") as dosyaa:
        dosyaa.write(f"{kullaniicii1}'in İlgi Alanları:\n")
        for kategorii, frekansss in ilgi_alanlarii_kullaniicii1.items():
            dosyaa.write(f"'{kategorii}': {frekansss}\n")

        dosyaa.write(f"\n{kullaniicii2}'nin İlgi Alanları:\n")
        for kategorii, frekansss in ilgi_alanlarii_kullaniicii2.items():
            dosyaa.write(f"'{kategorii}': {frekansss}\n")

        ortak_ilgii_alanlarii = set(ilgi_alanlarii_kullaniicii1.keys()).intersection(ilgi_alanlarii_kullaniicii2.keys())
        dosyaa.write("\nOrtak İlgi Alanları:\n")
        for kategorii in ortak_ilgii_alanlarii:
            frekansss1 = ilgi_alanlarii_kullaniicii1.get(kategorii, 0)
            frekansss2 = ilgi_alanlarii_kullaniicii2.get(kategorii, 0)
            dosyaa.write(f"'{kategorii}': {frekansss1} - {frekansss2}\n")

    # İlk kullanıcının ilgi alanlarını ekrana yazdır
    textbox.delete(1.0, tk.END)
    textbox.insert(tk.END, f"{kullaniicii1}'in İlgi Alanları:\n")
    for kategorii, frekansss in ilgi_alanlarii_kullaniicii1.items():
        textbox.insert(tk.END, f"'{kategorii}': {frekansss}\n")

    # İkinci kullanıcının ilgi alanlarını ekrana yazdır
    textbox.insert(tk.END, f"\n{kullaniicii2}'nin İlgi Alanları:\n")
    for kategorii, frekansss in ilgi_alanlarii_kullaniicii2.items():
        textbox.insert(tk.END, f"'{kategorii}': {frekansss}\n")

    # İki kullanıcının ortak ilgi alanlarını bul
    ortak_ilgii_alanlarii = set(ilgi_alanlarii_kullaniicii1.keys()).intersection(ilgi_alanlarii_kullaniicii2.keys())

    # Ortak ilgi alanlarını ekrana yazdır
    textbox.insert(tk.END, "\nOrtak İlgi Alanları:\n")
    for kategorii in ortak_ilgii_alanlarii:
        frekansss1 = ilgi_alanlarii_kullaniicii1.get(kategorii, 0)
        frekansss2 = ilgi_alanlarii_kullaniicii2.get(kategorii, 0)
        textbox.insert(tk.END, f"'{kategorii}': {frekansss1} - {frekansss2}\n")


# BFS ile ortak ilgi alanlarına sahip diğer kullanıcıları gösterme fonksiyonu
def digerr_kullanicilarii_goster():
    kullaniicii1 = entry_kullaniicii1.get()
    kullaniicii2 = entry_kullaniicii2.get()

    # belirtilen sayıda kullanıcıyı al
    belirtilen_kullanici_kadar = json_dosyasi_veri[:200]

    # Ortak ilgi alanlarına sahip diğer kullanıcıları bul
    diger_kullanicilarr = digerr_kullanicilarii_bull(kullaniicii1, kkategorilerr, belirtilen_kullanici_kadar)

    textbox.delete(1.0, tk.END)
    textbox.insert(tk.END, f" Ortak İlgi Alanlarına Sahip Diğer Kullanıcılar:\n")

    for kullaniicii in diger_kullanicilarr:
        textbox.insert(tk.END, f"\n{kullaniicii}\n")

# Buton oluştur
iki_kullanici_buttonu = tk.Button(arayuzz, text="İlgi Alanlarını Göster", command=ilgii_alanlarinii_goster)
iki_kullanici_buttonu.grid(row=3, column=0, columnspan=2, pady=12)

# Buton to find and display other users with common interests
diger_kullanicilar_buttonu = tk.Button(arayuzz, text="Ortak İlgi Alanlarına Sahip Diğer Kullanıcıları Göster", command=digerr_kullanicilarii_goster)
diger_kullanicilar_buttonu.grid(row=4, column=0, columnspan=2, pady=12)

arayuzz.mainloop()