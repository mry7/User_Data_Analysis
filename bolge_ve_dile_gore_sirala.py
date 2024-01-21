import json
import tkinter as tk
from kategoriler import kkategorilerr

# JSON dosyasını oku
with open('kullanicilar.json', 'r', encoding='utf-8') as dosyaa:
    json_dosyasi_veri = json.load(dosyaa)

# Kullanıcının ilgi alanlarını frekanslarıyla belirleyen fonksiyon
def kullanici_ilgi_alanlari(kullaniicii):
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
                if kategorii in kelimee_sayiisii:
                    kelimee_sayiisii[kategorii] += 1
                else:
                    kelimee_sayiisii[kategorii] = 1
# döngüler tamamlandıktan sonra, kategorilere göre kelime sayılarını içeren sözlük (kelimee_sayiisii) return ediliyor.
    return kelimee_sayiisii

#Kategori bulma fonksiyonu
#Bu fonksiyon, verilen bir kelimenin (kelimee) hangi kategoriye (kategorii) ait olduğunu belirlemek için kullanılır. 
#(kkategorilerr) içinde dolaşarak (bir_kategori_Listesindeki_Kelimeler)de bulunup bulunmadığını kontrol eder.
#Eğer bulunursa ilgili kategori adını(kategorii) döndürür, bulunmazsa None değerini döndürür.
def kullanicinin_kategorisini_bul(kelimee, kkategorilerr):
    for kategorii, bir_kategori_Listesindeki_Kelimeler in kkategorilerr.items():
        if kelimee in bir_kategori_Listesindeki_Kelimeler:
            return kategorii
    return None
#___________________________________________________________________________________________________________

# Belirli bir bölgedeki kullanıcıların ilgi alanlarını hesapla
def bolgeyee_ait_ilgi_alanlarii(bolgee):
    # Sadece belirli bir bölgedeki kullanıcıları al
    #(json_dosyasi_veri)de bulunan kullanıcıları filtreleyerek, sadece belirtilen bölgedeki kullanıcıları içeren 
    #bir liste olan (bolgedekii_kullnaicii) listesini oluşturur.
    bolgedekii_kullnaicii = [kullaniicii for kullaniicii in json_dosyasi_veri if kullaniicii.get("Region") == bolgee]

    # Eğer belirtilen bölgede hiç kullanıcı bulunamazsa mesaj veriyor
    if not bolgedekii_kullnaicii:
        print(f"{bolgee} Bölgesinde hiç kullanıcı bulunamadı.")
        return None

    # Eğer belirtilen bölgede kullanıcılar bulunursa, bu kullanıcıların ilgi alanlarını birleştirerek toplam ilgi alanlarını hesaplar.
    tum_kullanicilarin_ilgiAlani = [kullanici_ilgi_alanlari(kullaniicii) for kullaniicii in bolgedekii_kullnaicii]

    # Ortak ilgi alanlarını topla
    # Bu sözlük, her kategori için toplam ilgi sayılarını tutar.
    toplamm_ilgii_alanlarii = {}

# (tum_kullanicilarin_ilgiAlani) listesinde döngü yapılırken, her bir kullanıcının ilgi alanlarındaki 
    # kategoriler ve sayıları (toplamm_ilgii_alanlarii) sözlüğüne eklenir.
    for kullanicii_ilgiAlanii in tum_kullanicilarin_ilgiAlani:
        for kategorii, sayiii in kullanicii_ilgiAlanii.items():
            if kategorii in toplamm_ilgii_alanlarii:
                toplamm_ilgii_alanlarii[kategorii] += sayiii
            else:
                toplamm_ilgii_alanlarii[kategorii] = sayiii

    return toplamm_ilgii_alanlarii
#___________________________________________________________________________________________________________

# Dil bazında kullanıcıları filtrele
def dile_gore_filtrelee(dill):
    return [kullaniicii for kullaniicii in json_dosyasi_veri if kullaniicii.get("Language") == dill]
    # Sadece belirli bir dildeki kullanıcıları al
    #(json_dosyasi_veri)de bulunan kullanıcıları filtreleyerek, sadece belirtilen dildeki kullanıcıları içeren 
    #bir liste olan (bu_dildeki_kullanicilar) listesini oluşturur.
    # Belirli bir dildeki ilgi alanlarını hesapla
def dilee_ait_ilgi_alanlarii(dill):
    # Sadece belirli bir dildeki kullanıcıları al
    bu_dildeki_kullanicilar = [kullaniicii for kullaniicii in json_dosyasi_veri if kullaniicii.get("Language") == dill]

    # Eğer belirtilen dilde hiç kullanıcı bulunamazsa mesaj veriyor
    if not bu_dildeki_kullanicilar:
        print(f"{dill} Dilinde hiç kullanıcı bulunamadı.")
        return None

    # Her bir kullanıcının ilgi alanlarını birleştir
    # Eğer belirtilen dilde kullanıcılar bulunursa, bu kullanıcıların ilgi alanlarını birleştirerek toplam ilgi alanlarını hesaplar.
    tum_kullanicilarin_ilgiAlani = [kullanici_ilgi_alanlari(kullaniicii) for kullaniicii in bu_dildeki_kullanicilar]

    # Ortak ilgi alanlarını topla
    # Bu sözlük, her kategori için toplam ilgi sayılarını tutar.
    toplamm_ilgii_alanlarii = {}

# (tum_kullanicilarin_ilgiAlani) listesinde döngü yapılırken, her bir kullanıcının ilgi alanlarındaki 
    # kategoriler ve sayıları (toplamm_ilgii_alanlarii) sözlüğüne eklenir.
    for kullanicii_ilgiAlanii in tum_kullanicilarin_ilgiAlani:
        for kategorii, sayiii in kullanicii_ilgiAlanii.items():
            if kategorii in toplamm_ilgii_alanlarii:
                toplamm_ilgii_alanlarii[kategorii] += sayiii
            else:
                toplamm_ilgii_alanlarii[kategorii] = sayiii

    return toplamm_ilgii_alanlarii
#___________________________________________________________________________________________________________

# Belirli bir bölge ve dile göre ilgi alanlarını hesapla
def BolgeveDil():
    #girişler
    bolgee = entry_bolgee.get()
    dill = entry_dill.get()
    # (bolgeyee_ait_ilgi_alanlarii) fonksiyonu kullanılarak, belirtilen bölgedeki kullanıcıların ilgi alanları alınıyor
    # ve (ilgii_alanlarii_bolgee) adlı bir değişkene atanıyor.
    ilgii_alanlarii_bolgee = bolgeyee_ait_ilgi_alanlarii(bolgee)
    # (dilee_ait_ilgi_alanlarii) fonksiyonu kullanılarak, belirtilen bölgedeki kullanıcıların ilgi alanları alınıyor
    # ve (ilgii_alanlarii_dill) adlı bir değişkene atanıyor.
    ilgii_alanlarii_dill = dilee_ait_ilgi_alanlarii(dill)

    #  belirli bir bölge ve dil için ilgi alanları bulunmuşsa (ortakk_ilgii_alanlarii) kümesi oluşturuluyor. 
    if ilgii_alanlarii_bolgee is not None and ilgii_alanlarii_dill is not None:
        # Her iki filtre için ortak ilgi alanlarını bul
        ortakk_ilgii_alanlarii = set(ilgii_alanlarii_bolgee.keys()) & set(ilgii_alanlarii_dill.keys())

        listboxx_ilgi_alanlarii.delete(0, tk.END)  # Liste kutusunu temizle

        # Frekansa göre ilgi alanlarını sırala (en yüksek sayidan en düşük sayıya doğru)
        ilgii_alanlarinii_siralaa = sorted([(kategorii, ilgii_alanlarii_bolgee[kategorii] + ilgii_alanlarii_dill[kategorii]) for kategorii in ortakk_ilgii_alanlarii], key=lambda x: x[1], reverse=True)

        for kategorii, sayiii in ilgii_alanlarinii_siralaa:
            listboxx_ilgi_alanlarii.insert(tk.END, f"{kategorii}: {sayiii} kişide tekrarlanmış.")
#___________________________________________________________________________________________________________
# Tkinter arayüzü oluştur
arayuzz = tk.Tk()
arayuzz.title("Kullanıcı Bilgileri İstatistikleri")

# Dil ve Bölge giriş kutuları
label_bolgee = tk.Label(arayuzz, text="Bölge:")
entry_bolgee = tk.Entry(arayuzz)
label_bolgee.grid(row=0, column=0, padx=6, pady=6)
entry_bolgee.grid(row=0, column=1, padx=6, pady=6)

label_dill = tk.Label(arayuzz, text="Dil:")
entry_dill = tk.Entry(arayuzz)
label_dill.grid(row=1, column=0, padx=6, pady=6)
entry_dill.grid(row=1, column=1, padx=6, pady=6)

# Liste kutusu oluştur
listboxx_ilgi_alanlarii = tk.Listbox(arayuzz, width=55, height=15)
listboxx_ilgi_alanlarii.grid(row=2, column=0, columnspan=2, pady=12)
#___________________________________________________________________________________________________________

# Belirli bir bölgedeki ilgi alanlarını ekrana yazdır
def Bolge():
    bolgee = entry_bolgee.get()
    ilgii_alanlarii = bolgeyee_ait_ilgi_alanlarii(bolgee)

    if ilgii_alanlarii is not None:
        listboxx_ilgi_alanlarii.delete(0, tk.END)  # Liste kutusunu temizle

        # Frekansa göre ilgi alanlarını sırala
        ilgii_alanlarinii_siralaa = sorted(ilgii_alanlarii.items(), key=lambda x: x[1], reverse=True)

        for kategorii, sayiii in ilgii_alanlarinii_siralaa:
            listboxx_ilgi_alanlarii.insert(tk.END, f"{kategorii}: {sayiii} kişide tekrarlanmış.")
#___________________________________________________________________________________________________________

# Belirli bir dile göre ilgi alanlarını ekrana yazdır
def Dil():
    dill = entry_dill.get()
    ilgii_alanlarii = dilee_ait_ilgi_alanlarii(dill)

    if ilgii_alanlarii is not None:
        listboxx_ilgi_alanlarii.delete(0, tk.END)  # Liste kutusunu temizle

        # Frekansa göre ilgi alanlarını sırala
        ilgii_alanlarinii_siralaa = sorted(ilgii_alanlarii.items(), key=lambda x: x[1], reverse=True)

        for kategorii, sayiii in ilgii_alanlarinii_siralaa:
            listboxx_ilgi_alanlarii.insert(tk.END, f"{kategorii}: {sayiii} kişide tekrarlanmış.")
#___________________________________________________________________________________________________________

# Belirli bir bölge ve dile göre ilgi alanlarını ekrana yazdır
def BolgeveDil():
    bolgee = entry_bolgee.get()
    dill = entry_dill.get()
    ilgii_alanlarii_bolgee = bolgeyee_ait_ilgi_alanlarii(bolgee)
    ilgii_alanlarii_dill = dilee_ait_ilgi_alanlarii(dill)

    if ilgii_alanlarii_bolgee is not None and ilgii_alanlarii_dill is not None:
        # Her iki filtre için ortak ilgi alanlarını bul
        ortakk_ilgii_alanlarii = set(ilgii_alanlarii_bolgee.keys()) & set(ilgii_alanlarii_dill.keys())

        listboxx_ilgi_alanlarii.delete(0, tk.END)  # Liste kutusunu temizle

        # Frekansa göre ilgi alanlarını sırala
        ilgii_alanlarinii_siralaa = sorted([(kategorii, ilgii_alanlarii_bolgee[kategorii] + ilgii_alanlarii_dill[kategorii]) for kategorii in ortakk_ilgii_alanlarii], key=lambda x: x[1], reverse=True)

        for kategorii, sayiii in ilgii_alanlarinii_siralaa:
            listboxx_ilgi_alanlarii.insert(tk.END, f"{kategorii}: {sayiii} kişide tekrarlanmış.")
#___________________________________________________________________________________________________________

# Butonları oluştur
bolgee_buttonn = tk.Button(arayuzz, text="Bölgedeki Kullanıcıların İlgi Alanlarını Göster", command=Bolge)
bolgee_buttonn.grid(row=3, column=0, columnspan=2, pady=12)

dill_buttonn = tk.Button(arayuzz, text="Dile Göre İlgi Alanlarını Göster", command=Dil)
dill_buttonn.grid(row=4, column=0, columnspan=2, pady=12)

BolgeeVeDill_buttonn = tk.Button(arayuzz, text="Bölge ve Dil İlgi Alanlarını Göster", command=BolgeveDil)
BolgeeVeDill_buttonn.grid(row=5, column=0, columnspan=2, pady=12)

arayuzz.mainloop()