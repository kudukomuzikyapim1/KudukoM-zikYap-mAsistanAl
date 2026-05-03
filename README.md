<img width="608" height="607" alt="Ekran görüntüsü 2025-12-01 143817" src="https://github.com/user-attachments/assets/bab9476a-7bd1-4de7-ad36-ce70e2c869fa" />
📘 KUDUKO MUZİK YAPİM ASİSTAN AL v2.0 - DOKÜMANTASYON
📑 İÇİNDEKİLER
Genel Bakış

Kurulum ve Gereksinimler

Ana Özellikler

Kamera Kontrol Sistemi

Menü Sistemi

Asistan Profilleri

Medya Kontrolü

Ağ Kontrolü

Windows Entegrasyonu

Sistem Bileşenleri

Sesli Komutlar

Sık Karşılaşılan Sorunlar

1. GENEL BAKIŞ
KUDUKO MUZİK YAPİM ASİSTAN AL, gelişmiş bir masaüstü yapay zeka asistanıdır. Windows 11 için optimize edilmiş olup, aşağıdaki temel yeteneklere sahiptir:

Özellik	Açıklama
🎤 Sesli Komut	SpeechRecognition ile ses tanıma
🔊 Sesli Yanıt	pyttsx3 ile metin okuma
📷 Kamera Kontrolü	OpenCV ile fotoğraf çekimi
🎵 Müzik Kontrolü	Windows medya tuşları entegrasyonu
📡 Ağ Yönetimi	Wi-Fi ve Bluetooth kontrolü
💾 Hafıza Sistemi	JSON tabanlı öğrenme ve kayıt
🎭 Çoklu Profil	5 farklı kişilik profili
                                                                                                                                                                 2. KURULUM VE GEREKSİNİMLER
📦 Gerekli Kütüphaneler                                                                                                                                        # Temel kütüphaneler
                                                                                                                                                                pip install tkinter  # (Python ile gelir)

# Sesli komut için
pip install SpeechRecognition

# Sesli yanıt için
pip install pyttsx3

# Kamera için
pip install opencv-python pillow

# Pencere kontrolü için
pip install pygetwindow

# Otomasyon için
pip install pyautogui

# Sistem bilgileri için
pip install psutil                                                                                                                                                                                                                                                                                                                🔧 Sistem Gereksinimleri
Bileşen	Minimum	Önerilen
İşletim Sistemi	Windows 10	Windows 11
Python	3.8+	3.11+
RAM	2 GB	4 GB+
Kamera	720p	1080p+                                                                                                                                                                                                                                                                                                               3. ANA ÖZELLİKLER
🎨 Tema ve Renk Sistemi                                                                                                                                                                                                                                                                                                       BG_DARK = "#0a0e1a"      # Ana arkaplan
BG_CARD = "#0d1525"      # Kart arkaplanı
ACCENT = "#00cfff"       # Neon mavi vurgu
GREEN = "#00ff88"        # Yeşil durum
WARN = "#ff4466"         # Kırmızı uyarı                                                                                                                                                                                                                                                                                            🧠 Asistan Beyni (AssistantBrain)
Asistanın yanıt üretme mantığı:                                                                                                                                                                                                                                                                                                    def respond(self, text):
    t = text.lower()
    
    # Saat sorgusu
    if any(x in t for x in ["saat", "zaman"]):
        return f"🕐 Saat {datetime.datetime.now().strftime('%H:%M:%S')}.", "NLP"
    
    # Fotoğraf çekme
    if any(x in t for x in ["fotoğraf çek", "resim çek"]):
        success, msg, path = self.camera.take_photo()
        return f"✅ {msg}", "KAMERA"
    
    # ... diğer komutlar                                                                                                                                                                                                                                                                                                             4. KAMERA KONTROL SİSTEMİ
📷 CameraController Sınıfı
Bu sınıf, Windows'ta kamera kontrolünü sağlar:

Metod	Açıklama	Dönüş Değeri
start_preview()	Kamera önizlemesini başlatır	(bool, str)
take_photo()	Hızlı fotoğraf çeker	(bool, str, str)
take_photo_with_preview()	Geri sayımlı fotoğraf çeker	(bool, str, str)
stop_preview()	Kamerayı kapatır	None
get_photos_list()	Çekilen fotoğrafları listeler	list[str]                                                                                                                                                                                                                                                                        📸 Fotoğraf Kayıt Yolu                                                                                                                                                                                                                                                                                                 self.photos_dir = Path.home() / "Pictures" / "KUDUKO_MUZIK_YAPIM_ASISTAN_AL_Photos"
# Örnek: C:\Users\Kullanıcı\Pictures\KUDUKO_MUZIK_YAPIM_ASISTAN_AL_Photos\                                                                                                                                                                                                                                                        🖼️ PhotoGalleryWindow Sınıfı
Fotoğraf galerisi penceresi özellikleri:

✅ Önceki/Sonraki gezinti

✅ Klasörü Aç butonu

✅ Yenileme desteği

✅ PIL ile görüntü önizleme

5. MENÜ SİSTEMİ
☰ MenuPopup Sınıfı
Menü penceresi şu bölümleri içerir:                                                                                                                                ┌─────────────────────────────────────┐
│ ☰ MENÜ                          ✕   │
├─────────────────────────────────────┤
│ ⚡ HIZLI İŞLEMLER                    │
│   🎤 Sesli Komut                     │
│   🗑️ Sohbeti Temizle                 │
│   📋 Kopyala                         │
│   💾 Kaydet                          │
├─────────────────────────────────────┤
│ 📷 KAMERA & MEDYA KONTROL            │
│   📷 KAMERA AÇ (ÖNİZLEME)            │
│   📸 FOTOĞRAF ÇEK (HIZLI)            │
│   ⏱️ FOTOĞRAF ÇEK (GERİ SAYIM)       │
│   🔴 KAMERAYI KAPAT                   │
│   📱 WİNDOWS KAMERA UYGULAMASI       │
│   🖼️ FOTOĞRAF GALERİSİ               │
├─────────────────────────────────────┤
│ 🎵 MÜZİK KONTROL                     │
│   ▶️ Başlat  ⏸️ Duraklat              │
│   ⏹️ Durdur   ⏭️ Sonraki              │
├─────────────────────────────────────┤
│ 🤖 ASİSTAN PROFİLİ                   │
│   [KLASİK] [ARKADAŞÇA] [ALAYCI]     │
│   [PROFESYONEL] [SAKİN OLMAK]        │
└─────────────────────────────────────┘                                                                                                                            6. ASİSTAN PROFİLLERİ
🎭 AssistantProfile Sınıfı
5 farklı asistan kişiliği:

Profil	Emoji	Stil	Ses Hızı	Örnek Yanıt
KLASİK	🎩	resmi	160	"Hazırım, efendim."
ARKADAŞÇA	😊	samimi	170	"Hey! Bugün sana nasıl yardımcı olabilirim? ✨"
ALAYCI	😏	alaycı	155	"Yine mi? Pekala, ne istiyorsun? 😄"
PROFESYONEL	💼	iş	150	"Sistemler hazır. Emirlerinizi bekliyorum."
SAKİN OLMAK	🎮	rahat	175	"N'aber? Hazırım, buyur! 🚀"                                                                                                                                                                                                                                                                            💾 Profil Kaydı                                                                                                                                                    # assistant_profile.json
{
    "profile": "ARKADAŞÇA"
}                                                                                                                                                                                                                                                                                                                                 7. MEDYA KONTROLÜ
🎵 MediaController Sınıfı
Windows medya tuşlarını kullanır:

Metod	Sanal Tuş Kodu	Açıklama
play_pause()	0xB3	Oynat/Duraklat
next_track()	0xB0	Sonraki şarkı
previous_track()	0xB1	Önceki şarkı
volume_up()	0xAF	Sesi artır
volume_down()	0xAE	Sesi azalt
Kullanım Örneği:                                                                                                                                                #                                                                                                                                                                   ctypes ile sanal tuş gönderme
ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)  # Tuşa bas
ctypes.windll.user32.keybd_event(0xB3, 0, 2, 0)  # Tuşu bırak                                                                                                                                                                                                                                                                        8. AĞ KONTROLÜ
🌐 NetworkController Sınıfı
Metod	Platform	Açıklama
wifi_on/off()	netsh	Wi-Fi bağlantısını kontrol eder
bluetooth_on/off()	PowerShell	Bluetooth adaptörünü kontrol eder
get_wifi_status()	netsh	Wi-Fi durumunu sorgular
get_bluetooth_status()	PowerShell	Bluetooth durumunu sorgular
PowerShell Komut Örneği:                                                                                                                                        #                                                                                                                                                             Bluetooth kapatma
$adapter = Get-PnpDevice -Class Bluetooth
Disable-PnpDevice -InstanceId $adapter.InstanceId -Confirm:$false                                                                                                                                                                                                                                                                 9. WINDOWS ENTEGRASYONU
🪟 WindowsController Sınıfı
Metod	Açıklama
list_all_installed_apps()	Tüm yüklü uygulamaları listeler
open_app_smart(app_name)	Akıllı uygulama başlatma
music_control(command)	Müzik kontrol komutlarını yönlendirir
Uygulama Bulma Yöntemleri:

Başlat Menüsü (.lnk ve .exe dosyaları)

Windows Registry (Uninstall anahtarları)

Program Files klasörleri

Masaüstü kısayolları

Hızlı Eşleme Örnekleri:                                                                                                                                                                                                                                                                                                     quick_map = {
    "notepad": "notepad.exe",
    "hesap makinesi": "calc.exe",
    "chrome": "chrome.exe",
    "spotify": "Spotify.exe"
}                                                                                                                                                                                                                                                                                                                                 10. SİSTEM BİLEŞENLERİ
📊 Sistem İstatistikleri                                                                                                                                                                                                                                                                                                             # CPU ve RAM izleme (psutil ile)
cpu = psutil.cpu_percent(interval=0.3)
ram = psutil.virtual_memory()
disk = psutil.disk_usage('/')                                                                                                                                                                                                                                                                                                     💾 Hafıza Sistemi (Memory Sınıfı)
Özellik	Açıklama
history	Son 200 konuşma kaydı
learned	Öğrenilen bilgiler (anahtar-değer)
call_count	Toplam kullanıcı etkileşimi sayısı
JSON Kayıt Formatı:                                                                                                                                                                                                                                                                                                                    {
    "history": [["user", "merhaba", "2026-01-15 10:30:00"]],
    "learned": {"python nedir": "Bir programlama dilidir"},
    "calls": 42
}                                                                                                                                                                                                                                                                                                                                    🎨 Animasyon Sistemi
4 farklı animasyon katmanı:

Döner halka - Sistem durumu göstergesi

Dönen kareler - Renkli işlem göstergeleri

Yörüngedeki noktalar - Arka plan aktivitesi

Nabız efekti - Aktif dinleme durumu

11. SESLİ KOMUTLAR
🎤 Desteklenen Komutlar
Kategori	Komut Örnekleri
Sistem	"saat kaç", "tarih", "nasılsın"
Kamera	"kamera aç", "fotoğraf çek", "galeri"
Müzik	"müzik başlat", "sonraki şarkı", "ses aç"
Ağ	"wifi aç", "bluetooth kapat"
Uygulama	"spotify aç", "notepad aç"
Asistan	"tüm uygulamalar", "profil değiştir"                                                                                                                                                                                                                                                                                         🔄 Komut İşleme Akışı Kullanıcı Girişi
       ↓
AssistantBrain.respond()
       ↓
Kelime Eşleme (any() + in)
       ↓
İlgili Metodu Çağır
       ↓
Yanıt ve Modül Etiketi
       ↓
Profil Modifikasyonu
       ↓
Arayüzde Göster + Sesli Yanıt                                                                                                                                                                                                                                                                                                    12. SIK KARŞILAŞILAN SORUNLAR
❌ Hata ve Çözümleri
Hata	Olası Nedeni	Çözüm
"Kamera bulunamadı"	OpenCV eksik	pip install opencv-python
"TTS yüklü değil"	pyttsx3 eksik	pip install pyttsx3
"Wi-Fi kapatılamadı"	Yönetici yetkisi	Yönetici olarak çalıştırın
"Fotoğraf kaydedilemedi"	Dizin izni	Pictures klasörünü kontrol edin
📝 Önemli Notlar
Kamera kullanımı: Önce "kamera aç" komutu vermelisiniz

Bluetooth kontrolü: PowerShell gerektirir

Medya tuşları: Sadece Windows'ta çalışır

Profil değişikliği: Otomatik kaydedilir

📞 İLETİŞİM
Geliştirici: KUDUKO MUZİK YAPİM
Web: https://kudukomuzikyapimasistanal.42web.io
GitHub: https://github.com/kudukomuzikyapim1
Sürüm: 2.0
Telif: © 2026
