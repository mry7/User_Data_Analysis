from faker import Faker
import random
import json
from kategoriler import kkategorilerr

ffakee = Faker()

# Tüm kategorileri bir listeye ekle
kategori_listesii = list(kkategorilerr.keys())

def kullanici_bilgileri():
    username = ffakee.user_name()
    full_name = ffakee.name()
    followers_count = ffakee.random_int(min=1, max=100)
    following_count = ffakee.random_int(min=1, max=100)
    language = ffakee.language_name()
    region = ffakee.country()

    # Kullanıcı isimleri oluştur (takipci ve takip edilen icin)
    followers_names = [ffakee.user_name() for _ in range(followers_count)]
    following_names = [ffakee.user_name() for _ in range(following_count)]

    # Rastgele tweet sayısı belirle
    toplam_tweet_sayisii = ffakee.random_int(min=1, max=100)
    
    # Kullanıcı ilgi alanına uygun bir veya birden fazla kategori seç
    kullaniciya_kategori_ata = random.sample(kategori_listesii, i=kullaniciya_atanan_kategori_sayisii)

    # Rastgele kategori sayısı belirle 
    kullaniciya_atanan_kategori_sayisii = min(random.randint(1, 30), len(kategori_listesii))
    
   

    # Rastgele tweet sayısı kadar tweet oluştur
    tweets = []
    #Bu for dongusu kullanicilara belirlenen kategoriler icerisinden bir kategori-ler atamak icin kullanilir
    #Verilen kategorilerden kullaniciya 1-30 arasinda random kategori sayisi atanir ve her bir kategori icin random bir tweet sayisi belirlenir
    for kategorii in kullaniciya_kategori_ata:
        kategorili_tweet = ffakee.random_int(min=1, max=min(100, max(1, toplam_tweet_sayisii)))
        #toplam tweet sayisindan kategorili tweet sayisi cikarilir
        toplam_tweet_sayisii -= kategorili_tweet
        #json dosyasinda olacak tweetin son halini belilrlemek icin bir dongu
        #kategorilerin icerisindeki kelimlerden rastgele secilir ve onlarin sirasi da rastgele belirlenir
        #ardindan her bir tweet icerisine rastgele kelimeler atanir 0-10 arasi kelime (random kelime uretilir ve sirasi rastegele olur)
        tweet_son = [
            ' '.join([
                (f"{random.choice(kkategorilerr[kategorii])} {ffakee.word()}") if random.choice([True, False])
                else (f"{ffakee.word()} {random.choice(kkategorilerr[kategorii])}")
            ] + [ffakee.word() for _ in range(random.randint(0, 10))])
            for _ in range(kategorili_tweet)
        ]
        tweets.extend(tweet_son)

#json dosyasında dondurulen veri tipi
    return {
        "Username": username,
        "Full Name": full_name,
        "Language": language,
        "Region": region,
        "Followers Count": followers_count,
        "Followers": followers_names,
        "Following Count": following_count,
        "Following": following_names,
        "Tweets": tweets
    }

# belirtilen sayıda kullanıcı oluştur
kullanici_verisi_olustur = [kullanici_bilgileri() for _ in range(35000)]

# Oluşturulan veriyi JSON formatında dosyaya yaz
with open('kullanicilar.json', 'w') as dosyaa:
    json.dump(kullanici_verisi_olustur, dosyaa, indent=2)

print("kullanıcı Verileri 'kullanicilar.json' adlı bir dosyaya kaydedildi.")
