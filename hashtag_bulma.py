import json
from tkinter import Tk, Label, Button, Entry, Text, Scrollbar, END

from kategoriler import kkategorilerr

# (kategorii) , oluşturulacak ilgi alanları sözlüğünün hangi kategoriye ait olacağını belirtir.
def Kategorii_bulmaa_fonkk(kategorii):
    # Eğer belirtilen kategori mevcut ise boş (ilgii_alanii_sozlukk) oluştur.
    if kategorii in kkategorilerr:
        ilgii_alanii_sozlukk = {}
       # (kkategorilerr) sözlüğündeki belirtilen (kategorii)ye ait ilgi alanlarının listesini alır.
        for ilgii in kkategorilerr[kategorii]:
            # er bir ilgi alanı için bir anahtar oluşturulup, bu anahtara karşılık gelen değer True olarak atanır. 
            #Bu şekilde, i(ilgii_alanii_sozlukk) sözlüğü oluşturulur.
            ilgii_alanii_sozlukk[ilgii] = True
        return ilgii_alanii_sozlukk
    # Eğer belirtilen kategori mevcut değilse
    else:
        return None


def kullaniciyi_bull(kullanicii_adii):
    for kullaniicii in tumm_kullanicilarr:
        if kullaniicii['Username'] == kullanicii_adii:
            return kullaniicii
    return None


def ilgiiAlaninaa_göree_eslestirmee(kategorii):
    # (Kategorii_bulmaa_fonkk) kullanılarak belirli bir (kategorii)ye ait ilgi alanlarını içeren bir tabloyu alır.
    ilgii_alanii_tablosuu = Kategorii_bulmaa_fonkk(kategorii)
    # Bu liste, ilgi alanlarına sahip olan kullanıcıların kullanıcı adlarını tutacaktır.
    kullanicii_adlarii_listesii = []

    for kullaniicii in tumm_kullanicilarr:
        tweets = kullaniicii['Tweets']
        for tweet in tweets:
            for kelimee in tweet.split():
                # (ilgii_alanii_tablosuu) içindeki her bir ilgi alanı, her bir kelime ile karşılaştırılır.
                # Eğer bir ilgi alanı, kelimenin içinde geçiyorsa, bu kullanıcının kullanıcı adı (kullanicii_adlarii_listesii) listesine eklenir
                # ve break ile döngüden çıkılır
                if any(ilgii.lower() in kelimee.lower() for ilgii in ilgii_alanii_tablosuu):
                    kullanicii_adlarii_listesii.append(kullaniicii['Username'])
                    break
# (kullanicii_adlarii_listesii) Bu liste, bir küme haline getirilip (set), ardından tekrar liste haline getirilerek (list) return edilir.
    return list(set(kullanicii_adlarii_listesii))


def arayuzz_fonk():
    def Bull():
        ilgii_alanii = ilgii_alanii_entry.get()
        ilgii_alaninaa_uygunn_kullanicilar_listesii = ilgiiAlaninaa_göree_eslestirmee(ilgii_alanii)
        textbox.delete(1.0, END)  # Önceki içeriği temizle

        if ilgii_alaninaa_uygunn_kullanicilar_listesii:
            textbox.insert(END, f"{ilgii_alanii.capitalize()} ile ilgili tweet atan kullanıcılar:\n")
            with open("hashtag.txt", "w", encoding="utf-8") as txtDosyasi:
                txtDosyasi.write(f"{ilgii_alanii.capitalize()} ile ilgili tweet atan kullanıcılar:\n")
                for kullaniicii in ilgii_alaninaa_uygunn_kullanicilar_listesii:
                    textbox.insert(END, f"{kullaniicii}\n")
                    txtDosyasi.write(f"{kullaniicii}\n")
                txtDosyasi.write("--" * 27 + "\n")
        else:
            textbox.insert(END, f"{ilgii_alanii.capitalize()} ile ilgili tweet atan kullanıcı bulunamadı.")

    arayuzz = Tk()
    arayuzz.title("İlgi Alanına Göre Eşleştirme Aracı")

    ilgii_alanii_label = Label(arayuzz, text="İlgi Alanı:")
    ilgii_alanii_label.pack()

    ilgii_alanii_entry = Entry(arayuzz)
    ilgii_alanii_entry.pack()

    buttonnn = Button(arayuzz, text="Bul ve Göster", command=Bull)
    buttonnn.pack()

    textbox = Text(arayuzz, height=10, width=40, wrap="word")
    textbox.pack()

    scrollbarr = Scrollbar(arayuzz, command=textbox.yview)
    scrollbarr.pack(side="right", fill="y")
    textbox.config(yscrollcommand=scrollbarr.set)

    arayuzz.mainloop()


if __name__ == "__main__":
    # JSON dosyasını oku
    with open('kullanicilar.json', 'r', encoding='utf-8') as dosyaa:
        tumm_kullanicilarr = json.load(dosyaa)

    # Sadece ilk 100 kullanıcıyı al
    tumm_kullanicilarr = tumm_kullanicilarr[:100]

    arayuzz_fonk()
