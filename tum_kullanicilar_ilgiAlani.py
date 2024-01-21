import tkinter as tk
import json
from kategoriler import kkategorilerr

# JSON dosyasını oku
with open('kullanicilar.json', 'r', encoding='utf-8') as dosyaa:
    json_dosyasi_veri = json.load(dosyaa)

# Kullanıcıyı kullanıcı adından bul
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
                kelimee_sayiisii[kategorii] = kelimee_sayiisii.get(kategorii, 0) + 1
# döngüler tamamlandıktan sonra, kategorilere göre kelime sayılarını içeren sözlük (kelimee_sayiisii) return ediliyor.
    return kelimee_sayiisii

# Tkinter arayüzü oluştur
arayuzz = tk.Tk()
arayuzz.title("Tüm Kullanıcıların İlgi Alanları")

# Bilgi gösterme alanı
textbox = tk.Text(arayuzz, height=20, width=55)
textbox.grid(row=2, column=0, columnspan=2, padx=4, pady=4)

# İlgi alanlarını gösterme fonksiyonu
def ilgii_alanlarinii_goster():
    # textboxi temizle
    textbox.delete(1.0, tk.END)

    # ciktiyi txt dosyasina yazdir
    with open("kullanici_ilgiAlani.txt", "w", encoding="utf-8") as txtDosyasi:
        # belirtilen kullanıcı sayısı için döngü oluştur
        for i in range(1000):
            kullanicii_adii = json_dosyasi_veri[i]['Username']

            # Her bir kullanıcı için ilgi alanlarını frekanslarıyla hesapla
            kullanici_ilgi_alanlari_listesi = kullanicinin_ilgi_alanlarii(kullanicii_adii, kkategorilerr)

            # İlgili kullanıcının ilgi alanlarını ekrana ve dosyaya yazdır
            textbox.insert(tk.END, f"{kullanicii_adii}'in İlgi Alanları:\n")
            txtDosyasi.write(f"{kullanicii_adii}'in İlgi Alanları:\n")
            for kategorii, frekansss in kullanici_ilgi_alanlari_listesi.items():
                textbox.insert(tk.END, f"'{kategorii}': {frekansss}\n")
                txtDosyasi.write(f"'{kategorii}': {frekansss}\n")
            textbox.insert(tk.END, "\n" + "--"*27 + "\n")
            txtDosyasi.write("\n" + "--"*29 + "\n")

#Arayüz için Buton oluşturma kısmı
tum_kullanicilar_ilgiAlani_button = tk.Button(arayuzz, text="Kullanıcıların ilgi alanlarını bul", command=ilgii_alanlarinii_goster)
tum_kullanicilar_ilgiAlani_button.grid(row=3, column=0, columnspan=2, pady=12)

arayuzz.mainloop()