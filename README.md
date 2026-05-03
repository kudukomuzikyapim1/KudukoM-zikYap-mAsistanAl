<img width="608" height="607" alt="Ekran görüntüsü 2025-12-01 143817" src="https://github.com/user-attachments/assets/bab9476a-7bd1-4de7-ad36-ce70e2c869fa" />
markdown
# 🎵 KUDUKO MUZİK YAPİM ASİSTAN AL v2.0

<div align="center">

![Version](https://img.shields.io/badge/sürüm-2.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![Platform](https://img.shields.io/badge/platform-Windows%2011-0078d4)
![License](https://img.shields.io/badge/license-MIT-yellow)

**Gelişmiş Yapay Zeka Asistanı | Sesli Komut | Kamera Kontrolü | Medya Yönetimi**

[![GitHub](https://img.shields.io/badge/GitHub-kudukomuzikyapim1-181717?style=for-the-badge&logo=github)](https://github.com/kudukomuzikyapim1)
[![Web](https://img.shields.io/badge/Web-Asistan%20Al-4285F4?style=for-the-badge&logo=googlechrome)](https://kudukomuzikyapimasistanal.42web.io)

</div>

---

## 📋 İçindekiler

- [✨ Özellikler](#-özellikler)
- [📸 Ekran Görüntüleri](#-ekran-görüntüleri)
- [🚀 Hızlı Başlangıç](#-hızlı-başlangıç)
- [📦 Kurulum](#-kurulum)
- [🎮 Kullanım](#-kullanım)
- [🎭 Asistan Profilleri](#-asistan-profilleri)
- [📷 Kamera Sistemi](#-kamera-sistemi)
- [🎵 Medya Kontrolü](#-medya-kontrolü)
- [🌐 Ağ Kontrolü](#-ağ-kontrolü)
- [💾 Hafıza Sistemi](#-hafıza-sistemi)
- [⌨️ Komut Listesi](#️-komut-listesi)
- [🔧 Sorun Giderme](#-sorun-giderme)
- [📁 Dosya Yapısı](#-dosya-yapısı)
- [🤝 Katkıda Bulunma](#-katkıda-bulunma)
- [📞 İletişim](#-iletişim)

---

## ✨ Özellikler

| Özellik | Açıklama | Durum |
|---------|----------|-------|
| 🎤 **Sesli Komut** | SpeechRecognition ile ses tanıma | ✅ Aktif |
| 🔊 **Sesli Yanıt** | pyttsx3 ile metin okuma | ✅ Aktif |
| 📷 **Kamera Kontrolü** | OpenCV ile fotoğraf çekimi | ✅ Aktif |
| 🎵 **Müzik Kontrolü** | Windows medya tuşları entegrasyonu | ✅ Aktif |
| 📡 **Ağ Yönetimi** | Wi-Fi ve Bluetooth kontrolü | ✅ Aktif |
| 💾 **Hafıza Sistemi** | JSON tabanlı öğrenme ve kayıt | ✅ Aktif |
| 🎭 **Çoklu Profil** | 5 farklı kişilik profili | ✅ Aktif |
| 🖼️ **Fotoğraf Galerisi** | Çekilen fotoğrafları görüntüleme | ✅ Aktif |
| 🌐 **Web Entegrasyonu** | WhatsApp Web, YouTube Music | ✅ Aktif |
| 📊 **Sistem İzleme** | CPU, RAM, Disk kullanımı | ✅ Aktif |

---

## 📸 Ekran Görüntüleri
┌─────────────────────────────────────────────────────────────────────────────┐
│ KUDUKO MUZİK YAPİM ASİSTAN AL ☰ MENÜ │
├────────────────────────────────┬────────────────────────────────────────────┤
│ │ │
│ 🎨 Animasyon Alanı │ 💬 Sohbet Alanı │
│ │ │
│ ┌──────────────────────┐ │ [10:30] 👤 KULLANICI: merhaba │
│ │ ◯◯◯◯ │ │ [10:30] 🤖 ASİSTAN: Merhaba efendim! │
│ │ ◯ ◯ │ │ │
│ │ ◯◯◯◯ │ │ [10:31] 👤 KULLANICI: saat kaç │
│ └──────────────────────┘ │ [10:31] 🤖 ASİSTAN: 🕐 10:31:25 │
│ │ │
│ 📊 SİSTEM İSTATİSTİKLERİ │ ┌──────────────────────────────────────┐ │
│ ┌──────────┬──────────┐ │ │ Mesajınızı yazın... [GÖNDER]│ │
│ │ CPU │ RAM │ │ └──────────────────────────────────────┘ │
│ │ 35% │ 42% │ │ │
│ └──────────┴──────────┘ │ 🎤 STT ✓ 🔊 TTS ✓ 📷 CAMERA ✓ │
│ │ │
└────────────────────────────────┴────────────────────────────────────────────┘

text

---

## 🚀 Hızlı Başlangıç

### 1. Depoyu Klonlayın

```bash
git clone https://github.com/kudukomuzikyapim1/kuduko-muzik-yapim-asistan-al.git
cd kuduko-muzik-yapim-asistan-al
2. Gereksinimleri Yükleyin
bash
pip install -r requirements.txt
3. Uygulamayı Başlatın
bash
python assistant.py
📦 Kurulum
Sistem Gereksinimleri
Bileşen	Minimum	Önerilen
İşletim Sistemi	Windows 10	Windows 11
Python	3.8+	3.11+
RAM	2 GB	4 GB+
Disk Alanı	500 MB	1 GB+
Kamera	720p	1080p+ (Opsiyonel)
Mikrofon	Herhangi	USB/Entegre (Opsiyonel)
Gerekli Kütüphaneler
bash
# Temel kütüphaneler (Python ile gelir)
# tkinter, json, os, threading, datetime, math, random, re, pathlib

# Sesli komut için
pip install SpeechRecognition

# Sesli yanıt için
pip install pyttsx3

# Kamera için
pip install opencv-python pillow

# Sistem bilgileri için
pip install psutil

# Pencere kontrolü için
pip install pygetwindow

# Otomasyon için
pip install pyautogui
requirements.txt
txt
SpeechRecognition>=3.10.0
pyttsx3>=2.90
opencv-python>=4.8.0
pillow>=10.0.0
psutil>=5.9.0
pygetwindow>=0.0.9
pyautogui>=0.9.54
🎮 Kullanım
Temel Komutlar
Komut	Açıklama
merhaba	Asistanla selamlaşma
saat kaç	Güncel saati öğrenme
tarih	Bugünün tarihini öğrenme
nasılsın	Asistanın durumunu sorma
teşekkür	Teşekkür etme
güle güle	Vedalaşma
Menü Kullanımı
Sağ üst köşedeki ☰ MENÜ butonuna tıklayın

Açılan pencereden istediğiniz işlemi seçin

Menüden çıkmak için ✕ butonuna veya ESC tuşuna basın

🎭 Asistan Profilleri
Asistanınızın kişiliğini değiştirebilirsiniz:

Profil	Emoji	Stil	Ses Hızı	Örnek Yanıt
KLASİK	🎩	Resmi	160	"Hazırım, efendim. Nasıl yardımcı olabilirim?"
ARKADAŞÇA	😊	Samimi	170	"Hey! Bugün sana nasıl yardımcı olabilirim? ✨"
ALAYCI	😏	Alaycı	155	"Yine mi? Pekala, ne istiyorsun? 😄"
PROFESYONEL	💼	İş	150	"Sistemler hazır. Emirlerinizi bekliyorum."
SAKİN OLMAK	🎮	Rahat	175	"N'aber? Hazırım, buyur! 🚀"
Profil değiştirme: Menüden veya profil değiştir komutuyla

📷 Kamera Sistemi
Özellikler
✅ Windows Kamera uygulaması desteği

✅ Hızlı fotoğraf çekimi

✅ Geri sayımlı fotoğraf çekimi (3 saniye)

✅ Fotoğraf galerisi

✅ Otomatik fotoğraf klasörü oluşturma

Kullanım
bash
# Kamera kontrolü
kamera aç          # Kamera önizlemesini başlat
kamera kapat       # Kamerayı kapat

# Fotoğraf çekme
fotoğraf çek       # Hızlı fotoğraf çek
resim çek          # Aynı işlev

# Galeri
galeri             # Fotoğraf galerisini aç
fotoğraflar        # Galeriyi aç
Fotoğraf Konumu
text
C:\Users\KULLANICI\Pictures\KUDUKO_MUZIK_YAPIM_ASISTAN_AL_Photos\
└── kudukomuzikyapimasistan_photo_20260115_143025.jpg
🎵 Medya Kontrolü
Desteklenen Komutlar
Komut	İşlev
müzik başlat	Müzik çalmaya başlar
müzik duraklat	Müziği duraklatır
müzik durdur	Müziği durdurur
sonraki şarkı	Sonraki parçaya geçer
önceki şarkı	Önceki parçaya döner
şarkıyı baştan oynat	Şarkıyı başa sarar
ses aç	Ses seviyesini artırır
ses kıs	Ses seviyesini azaltır
10 saniye ileri	10 saniye ileri sarar
Not: Windows Medya Tuşları kullanıldığı için çoğu müzik oynatıcıyla çalışır (Spotify, Windows Media Player, vb.)

🌐 Ağ Kontrolü
Wi-Fi Kontrolü
bash
wifi aç           # Wi-Fi bağlantısını açar
wifi kapat        # Wi-Fi bağlantısını kapatır
wifi durumu       # Wi-Fi durumunu gösterir
Bluetooth Kontrolü
bash
bluetooth aç      # Bluetooth adaptörünü açar
bluetooth kapat   # Bluetooth adaptörünü kapatır
bluetooth durumu  # Bluetooth durumunu gösterir
Not: Bluetooth komutları PowerShell gerektirir ve Yönetici yetkisiyle çalışır.

💾 Hafıza Sistemi
Asistan, konuşmaları ve öğrendiklerini JSON dosyalarında saklar:

memory.json
json
{
    "history": [
        ["user", "merhaba", "2026-01-15 10:30:00"],
        ["assistant", "Merhaba efendim!", "2026-01-15 10:30:01"]
    ],
    "learned": {
        "python nedir": "Bir programlama dilidir",
        "açılımı": "KUDUKO MUZİK YAPİM"
    },
    "calls": 42
}
assistant_profile.json
json
{
    "profile": "ARKADAŞÇA"
}
whatsapp_contacts.json
json
{
    "contacts": [
        {"name": "Ahmet", "phone": "5551234567"},
        {"name": "Ayşe", "phone": "5559876543"}
    ]
}
⌨️ Komut Listesi
📋 Tam Komut Listesi
<details> <summary><b>Sistem Komutları (10+ komut)</b></summary>
Komut	Açıklama
saat, saat kaç, zaman	Saati gösterir
tarih, bugün, gün	Tarihi gösterir
nasılsın, durum, nasıl gidiyor	Durumu sorgular
merhaba, selam, hey, naber, hello, hi	Selamlaşır
teşekkür, sağ ol, sağol	Teşekkür eder
güle güle, görüşürüz, bay bay	Vedalaşır
</details><details> <summary><b>Kamera Komutları (10+ komut)</b></summary>
Komut	Açıklama
kamera aç, kamerayı aç	Kamera önizlemesini başlatır
kamera kapat, kamerayı kapat	Kamerayı kapatır
fotoğraf çek, resim çek, fotograf cek	Fotoğraf çeker
galeri, galeriyi aç, fotoğraflar	Galeriyi açar
</details><details> <summary><b>Müzik Komutları (15+ komut)</b></summary>
Komut	Açıklama
müzik başlat, müzik başlat	Müzik başlatır
müzik durdur, müzik stop	Müzik durdurur
müzik duraklat	Müzik duraklatır
sonraki şarkı	Sonraki şarkı
önceki şarkı	Önceki şarkı
şarkıyı baştan oynat, baştan, başa sar	Şarkıyı başlatır
ses aç	Ses açar
ses kıs	Ses kısar
10 saniye ileri, 10sn ileri	İleri sarar
10 saniye geri, 10sn geri	Geri sarar
</details><details> <summary><b>Uygulama Komutları (30+ komut)</b></summary>
Komut	Açıklama
tüm uygulamalar, yüklü uygulamalar	Uygulama listesi
notepad aç	Not Defteri
hesap makinesi aç	Hesap Makinesi
cmd aç, komut istemi aç	Komut İstemi
chrome aç, google chrome aç	Chrome
spotify aç	Spotify
whatsapp aç	WhatsApp
discord aç	Discord
visual studio code aç, vscode aç	VS Code
</details><details> <summary><b>Ağ Komutları (10+ komut)</b></summary>
Komut	Açıklama
wifi aç, wi-fi aç	Wi-Fi açar
wifi kapat, wi-fi kapat	Wi-Fi kapatır
wifi durumu, wi-fi durumu	Wi-Fi durumu
bluetooth aç, bt aç	Bluetooth açar
bluetooth kapat, bt kapat	Bluetooth kapatır
bluetooth durumu, bt durumu	Bluetooth durumu
</details><details> <summary><b>Özel Komutlar (10+ komut)</b></summary>
Komut	Açıklama
zırh, zırh durumu	Zırh durumu
bilim, hesapla, kuantum	Bilim modülü
güvenlik, tehdit, tarama	Güvenlik taraması
taktik	Taktik analiz
youtube music aç, yt music aç	YouTube Music
whatsapp web aç	WhatsApp Web
</details>
🔧 Sorun Giderme
Yaygın Sorunlar ve Çözümleri
<details> <summary><b>❌ "Kamera bulunamadı" hatası</b></summary>
bash
# OpenCV'yi yükleyin
pip install opencv-python

# Kameranın bağlı olduğundan emin olun
# Başka bir uygulamanın kamerayı kullanmadığından emin olun
# Önce "kamera aç" komutunu verin
</details><details> <summary><b>❌ "TTS yüklü değil" hatası</b></summary>
bash
# pyttsx3'ü yükleyin
pip install pyttsx3

# Windows'ta ses sürücülerinizin güncel olduğundan emin olun
</details><details> <summary><b>❌ "Wi-Fi/Bluetooth kapatılamadı" hatası</b></summary>
bash
# Uygulamayı Yönetici olarak çalıştırın
# PowerShell'in çalıştığından emin olun
</details><details> <summary><b>❌ "Fotoğraf kaydedilemedi" hatası</b></summary>
bash
# Pictures klasörüne yazma izniniz olduğundan emin olun
# Önce "kamera aç" komutunu verin
# Yeterli disk alanı olduğundan emin olun
</details><details> <summary><b>❌ "ModuleNotFoundError" hatası</b></summary>
bash
# Tüm gereksinimleri yükleyin
pip install -r requirements.txt

# Python sürümünüzü kontrol edin (3.8+ gerekli)
python --version
</details>
📁 Dosya Yapısı
text
kuduko-muzik-yapim-asistan-al/
│
├── assistant.py              # Ana uygulama dosyası
├── requirements.txt          # Gerekli kütüphaneler
├── README.md                 # Bu dosya
├── komutlar.txt              # Komut listesi
│
├── memory.json               # Hafıza ve öğrenme verileri
├── assistant_profile.json    # Asistan profili ayarları
├── whatsapp_contacts.json    # WhatsApp kişi listesi
│
├── pictures/                 # Fotoğraf klasörü
│   └── KUDUKO_MUZIK_YAPIM_ASISTAN_AL_Photos/
│       └── *.jpg             # Çekilen fotoğraflar
│
└── docs/                     # Dokümantasyon
    ├── API.md
    ├── CONTRIBUTING.md
    └── CHANGELOG.md
🤝 Katkıda Bulunma
Bu depoyu fork edin

Yeni bir branch oluşturun (git checkout -b feature/amazing-feature)

Değişikliklerinizi commit edin (git commit -m 'feat: Add amazing feature')

Branch'inizi push edin (git push origin feature/amazing-feature)

Bir Pull Request açın

Geliştirme Önerileri
🐛 Hata raporları için Issues sayfasını kullanın

💡 Yeni özellik önerilerinizi bekliyoruz

📝 Dokümantasyona katkıda bulunabilirsiniz

📞 İletişim
Platform	Bağlantı
🌐 Web Sitesi	kudukomuzikyapimasistanal.42web.io
🐙 GitHub	github.com/kudukomuzikyapim1
📧 E-posta	kudukomuzikyapim@example.com
📱 WhatsApp	+90 XXX XXX XX XX
📜 Lisans
Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için LICENSE dosyasına bakın.

text
MIT License

Copyright (c) 2026 KUDUKO MUZİK YAPİM

Permission is hereby granted, free of charge, to any person obtaining a copy
...
🙏 Teşekkürler
Python ekibine harika dil için

OpenCV ekibine kamera desteği için

Tüm kullanıcılarımıza destekleri için

<div align="center">
⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!

KUDUKO MUZİK YAPİM ASİSTAN AL | © 2026

Gelişmiş Yapay Zeka Asistanı

</div> ```
Bu README.md dosyası:

✅ Profesyonel görünüm - Rozetler, başlıklar ve emojiler

✅ Kapsamlı içerik - Tüm özellikler detaylı açıklanmış

✅ Kolay gezinti - İçindekiler tablosu ve bağlantılar

✅ Kurulum rehberi - Adım adım kurulum talimatları

✅ Komut listesi - Açılır menülerde düzenlenmiş komutlar

✅ Sorun giderme - Yaygın sorunlar ve çözümleri

✅ Dosya yapısı - Proje organizasyonu

✅ İletişim bilgileri - Tüm bağlantılar
