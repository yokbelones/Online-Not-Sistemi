import sqlite3
import datetime

conn = sqlite3.connect("sinav.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS kullanicilar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kullanici_adi TEXT,
    sifre TEXT,
    rol TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sorular (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    soru TEXT,
    cevap TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sonuclar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kullanici TEXT,
    puan INTEGER
)
""")

conn.commit()


def log_yaz(mesaj):
    with open("log.txt", "a", encoding="utf-8") as f:
        tarih = datetime.datetime.now()
        f.write(f"[{tarih}] {mesaj}\n")


class Kullanici:
    def __init__(self, ad, sifre, rol):
        self.ad = ad
        self.sifre = sifre
        self.rol = rol


class Sistem:
    def kayit(self):
        ad = input("Kullanıcı adı: ")
        sifre = input("Şifre: ")
        rol = input("Rol (öğrenci/öğretmen): ")

        if rol not in ["öğrenci", "öğretmen"]:
            print("Hatalı rol!")
            return

        cursor.execute("INSERT INTO kullanicilar VALUES (NULL,?,?,?)", (ad, sifre, rol))
        conn.commit()

        log_yaz(f"{ad} kayıt oldu")
        print("Kayıt başarılı!")

    def giris(self):
        ad = input("Kullanıcı adı: ")
        sifre = input("Şifre: ")

        cursor.execute("SELECT * FROM kullanicilar WHERE kullanici_adi=? AND sifre=?", (ad, sifre))
        user = cursor.fetchone()

        if not user:
            print("Hatalı giriş!")
            return None

        log_yaz(f"{ad} giriş yaptı")
        print("Giriş başarılı! Rol:", user[3])

        return user

    def soru_ekle(self):
        soru = input("Soru: ")
        cevap = input("Cevap: ")

        cursor.execute("INSERT INTO sorular VALUES (NULL,?,?)", (soru, cevap))
        conn.commit()

        print("Soru eklendi!")

    def sorulari_listele(self):
        cursor.execute("SELECT * FROM sorular")
        sorular = cursor.fetchall()

        if not sorular:
            print("Soru yok")
            return

        for s in sorular:
            print(s[0], "-", s[1])

    def sonuclari_goster(self):
        cursor.execute("SELECT * FROM sonuclar")
        data = cursor.fetchall()

        if not data:
            print("Sonuç yok")
            return

        for d in data:
            print(d[1], "->", d[2])

    def sinava_gir(self, kullanici_adi):
        cursor.execute("SELECT * FROM sorular")
        sorular = cursor.fetchall()

        if not sorular:
            print("Soru yok")
            return

        puan = 0

        for s in sorular:
            print("\nSoru:", s[1])
            cevap = input("Cevap: ")

            if cevap.lower() == s[2].lower():
                puan += 10

        cursor.execute("INSERT INTO sonuclar VALUES (NULL,?,?)", (kullanici_adi, puan))
        conn.commit()

        log_yaz(f"{kullanici_adi} sınava girdi -> {puan}")
        print("Puan:", puan)

    def puan_gor(self, kullanici_adi):
        cursor.execute("SELECT puan FROM sonuclar WHERE kullanici=?", (kullanici_adi,))
        data = cursor.fetchall()

        if not data:
            print("Henüz sınava girilmemiş")
            return

        print("Puan:", data[-1][0])


sys = Sistem()

while True:
    print("\n=== ONLINE SINAV SISTEMI ===")
    print("1- Kayıt")
    print("2- Giriş")
    print("3- Çıkış")

    secim = input("Seçim: ")

    if secim == "1":
        sys.kayit()

    elif secim == "2":
        user = sys.giris()

        if user:
            kullanici_adi = user[1]
            rol = user[3]

            if rol == "öğretmen":
                while True:
                    print("\n--- ÖĞRETMEN PANEL ---")
                    print("1- Soru Ekle")
                    print("2- Soruları Listele")
                    print("3- Sonuçları Gör")
                    print("4- Çıkış")

                    s = input("Seçim: ")

                    if s == "1":
                        sys.soru_ekle()
                    elif s == "2":
                        sys.sorulari_listele()
                    elif s == "3":
                        sys.sonuclari_goster()
                    elif s == "4":
                        break
                    else:
                        print("Hatalı")

            else:
                while True:
                    print("\n--- ÖĞRENCİ PANEL ---")
                    print("1- Sınava Gir")
                    print("2- Puanımı Gör")
                    print("3- Çıkış")

                    s = input("Seçim: ")

                    if s == "1":
                        sys.sinava_gir(kullanici_adi)
                    elif s == "2":
                        sys.puan_gor(kullanici_adi)
                    elif s == "3":
                        break
                    else:
                        print("Hatalı")

    elif secim == "3":
        print("Çıkış yapılıyor...")
        break

    else:
        print("Hatalı seçim")