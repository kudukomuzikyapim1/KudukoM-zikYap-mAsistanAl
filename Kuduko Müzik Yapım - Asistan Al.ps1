# Bot İsmi: Kuduko Müzik Yapım - Asistan Al
# Tüm Komutlar Birleştirilmiş ve Güvenlik Kontrollü

# === API BİLGİLERİ ===
$API_KEY = "AIzaSyA4dYq62zIsCcoR1kI8iianyYIU2fidELc"
$API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.flas-lite:generateContent?key=$API_KEY"

# === GÜVENLİK DEĞİŞKENLERİ ===
$Script:AdminMode = $false
$Script:FailedAttempts = 0

# === GÜVENLİK FONKSİYONLARI ===
function Test-AdminRights {
    $currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Request-AdminAuthorization {
    Write-Host "`n⚠️  BU KOMUT YÖNETİCİ İZNİ GEREKTİRİYOR!" -ForegroundColor Yellow
    $confirm = Read-Host "Devam etmek için 'kuduko' yazın"
    return ($confirm -eq "kuduko")
}

function Invoke-SafeProcess {
    param([string]$ProcessPath, [string]$Arguments = "")
    try {
        if ($Arguments -eq "") {
            Start-Process $ProcessPath -ErrorAction Stop
        } else {
            Start-Process $ProcessPath $Arguments -ErrorAction Stop
        }
        return "✅ İşlem başarılı: $ProcessPath"
    } catch {
        return "❌ Hata: $($_.Exception.Message)"
    }
}

# === AI SOHBET FONKSİYONU ===
function Invoke-AIChat {
    param([string]$UserInput)
    
    $jsonBody = @{
        contents = @(
            @{
                parts = @(
                    @{
                        text = $UserInput
                    }
                )
            }
        )
    } | ConvertTo-Json -Depth 5

    try {
        $response = Invoke-RestMethod -Uri $API_URL -Method Post -ContentType "application/json" -Body $jsonBody
        return $response.candidates[0].content.parts[0].text
    }
    catch {
        return "❌ AI servisine ulaşılamıyor: $($_.Exception.Message)"
    }
}

# === ANA PROGRAM ===
Write-Host "🤖 Kuduko Müzik Yapım - Asistan Al'a hoş geldiniz!" -ForegroundColor Green
Write-Host "🤖 AI Destekli | 🛡️ Güvenli Mod | ⚡ 150+ Komut" -ForegroundColor Cyan
Write-Host "`n🤖 Çıkmak için 'çıkış' yazın" -ForegroundColor DarkGray
Write-Host "🤖 Tüm komutlar için 'komutlar' yazın" -ForegroundColor DarkGray

while ($true) {
    $komut = Read-Host "`n👤 Komutunuzu yazın"

    # Çıkış kontrolü
    if ($komut -eq "çıkış") {
        Write-Host "`n🤖 Kuduko Müzik Yapım - Asistan Al - İyi günler!" -ForegroundColor Yellow
        break
    }

    # AI moduna geçiş (komut tanınmazsa)
    $commandRecognized = $true

    switch ($komut.ToLower()) {
        # === SİSTEM KOMUTLARI ===
        "note defteri aç" { 
            Write-Host (Invoke-SafeProcess "notepad.exe")
        }
        
        "hesap makinesi aç" { 
            Write-Host (Invoke-SafeProcess "calc.exe")
        }
        
        "pil seviyesi kaç" { 
            try {
                $battery = Get-WmiObject -Class Win32_Battery -ErrorAction Stop
                $level = $battery.EstimatedChargeRemaining
                Write-Host "🔋 Pil seviyesi: $level%" -ForegroundColor Green
            } catch {
                Write-Host "❌ Pil bilgisi alınamadı" -ForegroundColor Red
            }
        }
        
        "windows yeniden başlat" { 
            if (Request-AdminAuthorization) {
                if (Test-AdminRights) {
                    Write-Host "🔄 Sistem yeniden başlatılıyor..." -ForegroundColor Yellow
                    Restart-Computer
                } else {
                    Write-Host "❌ Bu işlem için yönetici hakları gerekli!" -ForegroundColor Red
                }
            }
        }
        
        "windows akıllı depolamayı şimdi çalıştır" { 
            if (Request-AdminAuthorization) {
                try {
                    $storage = Get-StoragePool
                    $disks = Get-PhysicalDisk
                    Write-Host "💾 Depolama durumu:" -ForegroundColor Green
                    Write-Host "   - Storage Pool: $($storage.Count) adet"
                    Write-Host "   - Fiziksel Disk: $($disks.Count) adet"
                } catch {
                    Write-Host "❌ Depolama bilgisi alınamadı" -ForegroundColor Red
                }
            }
        }
        
        "windows kapat" { 
            if (Request-AdminAuthorization) {
                if (Test-AdminRights) {
                    Write-Host "🔄 Sistem kapanıyor..." -ForegroundColor Yellow
                    Stop-Computer
                } else {
                    Write-Host "❌ Bu işlem için yönetici hakları gerekli!" -ForegroundColor Red
                }
            }
        }

        "windows ürün anahtarı aç" { 
            if (Request-AdminAuthorization) {
                try {
                    Add-Type -AssemblyName System.Windows.Forms
                    [System.Windows.Forms.Application]::EnableVisualStyles()

                    $form = New-Object System.Windows.Forms.Form
                    $form.Text = "Windows Aktivasyon Aracı - Kuduko Müzik Yapım"
                    $form.Size = New-Object System.Drawing.Size(400,200)
                    $form.StartPosition = "CenterScreen"

                    $label = New-Object System.Windows.Forms.Label
                    $label.Text = "Ürün Anahtarı:"
                    $label.AutoSize = $true
                    $label.Location = New-Object System.Drawing.Point(20,20)
                    $form.Controls.Add($label)

                    $textBox = New-Object System.Windows.Forms.TextBox
                    $textBox.Size = New-Object System.Drawing.Size(340,30)
                    $textBox.Location = New-Object System.Drawing.Point(20,45)
                    $form.Controls.Add($textBox)

                    $button = New-Object System.Windows.Forms.Button
                    $button.Text = "Etkinleştir"
                    $button.Location = New-Object System.Drawing.Point(20,85)
                    $button.Add_Click({
                        $key = $textBox.Text
                        if ($key -match "^[A-Z0-9\-]{25,}$") {
                            Start-Process -FilePath "slmgr.vbs" -ArgumentList "/ipk $key" -WindowStyle Hidden
                            Start-Sleep -Seconds 2
                            Start-Process -FilePath "slmgr.vbs" -ArgumentList "/ato" -WindowStyle Hidden
                            [System.Windows.Forms.MessageBox]::Show("Ürün anahtarı uygulandı ve etkinleştirildi.","Başarılı - Kuduko Asistan")
                        } else {
                            [System.Windows.Forms.MessageBox]::Show("Geçerli bir ürün anahtarı girin. (25 karakter)","Hata - Kuduko Asistan")
                        }
                    })
                    $form.Controls.Add($button)

                    $form.ShowDialog()
                    Write-Host "🔑 Ürün anahtarı aracı kapatıldı" -ForegroundColor Green
                } catch {
                    Write-Host "❌ Ürün anahtarı aracı açılamadı" -ForegroundColor Red
                }
            }
        }
        
        "windows ürün anahtarı komutları aç" { 
            Start-Process "https://www.mediafire.com/file/kptbhatqlsw80p2/Windows_%25C3%259Cr%25C3%25BCn_Anahtar%25C4%25B1.txt/file"
            Write-Host "🔗 Ürün anahtarı komutları açılıyor..." -ForegroundColor Cyan
        }
        
        "note defteri yazı yazma aç" { 
            $metin = Read-Host "Lütfen yazmak istediğiniz metni girin"
            if ($metin) {
                $dosyaYolu = "$env:TEMP\kuduko_yazim_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
                $metin | Out-File $dosyaYolu
                Start-Process "notepad.exe" $dosyaYolu
                Write-Host "📝 Not defteri yazı modu açıldı - Dosya: $dosyaYolu" -ForegroundColor Green
            } else {
                Write-Host "❌ Metin girilmedi" -ForegroundColor Red
            }
        }
        
        "arama motoru asistanı aç" { 
            try {
                Add-Type -AssemblyName System.Windows.Forms
                Add-Type -AssemblyName System.Web

                $form = New-Object System.Windows.Forms.Form
                $form.Text = "Kuduko Müzik Yapım Tarayıcı"
                $form.Width = 1024
                $form.Height = 720
                $form.BackColor = "LightGray"
                $form.StartPosition = "CenterScreen"

                # Arama kutusu
                $searchBox = New-Object System.Windows.Forms.TextBox
                $searchBox.Text = "https://kudukomuzikyapim.blogspot.com"
                $searchBox.Location = New-Object System.Drawing.Point(10,10)
                $searchBox.Width = 800
                $form.Controls.Add($searchBox)

                # Git butonu
                $btnGo = New-Object System.Windows.Forms.Button
                $btnGo.Text = "Git"
                $btnGo.Location = New-Object System.Drawing.Point(820,10)
                $btnGo.Add_Click({
                    $url = $searchBox.Text
                    if (-not $url.StartsWith("http")) { $url = "https://" + $url }
                    try {
                        $webBrowser.Navigate($url)
                    } catch {
                        [System.Windows.Forms.MessageBox]::Show("Geçersiz bağlantı!","Hata - Kuduko Asistan")
                    }
                })
                $form.Controls.Add($btnGo)

                # Hızlı bağlantılar
                $quickLinks = @{
                    "Kuduko" = "https://kudukomuzikyapim.blogspot.com"
                    "YouTube" = "https://www.youtube.com"
                    "Google" = "https://www.google.com"
                }

                $yPos = 50
                foreach ($linkName in $quickLinks.Keys) {
                    $btn = New-Object System.Windows.Forms.Button
                    $btn.Text = $linkName
                    $btn.Location = New-Object System.Drawing.Point(10, $yPos)
                    $btn.Width = 120
                    $btn.Add_Click({ $webBrowser.Navigate($quickLinks[$btn.Text]) })
                    $form.Controls.Add($btn)
                    $yPos += 30
                }

                # WebBrowser
                $webBrowser = New-Object System.Windows.Forms.WebBrowser
                $webBrowser.ScriptErrorsSuppressed = $true
                $webBrowser.Location = New-Object System.Drawing.Point(150, 50)
                $webBrowser.Size = New-Object System.Drawing.Size(850, 620)
                $webBrowser.Navigate($searchBox.Text)
                $form.Controls.Add($webBrowser)

                $form.Add_Shown({$form.Activate()})
                $form.ShowDialog()
                Write-Host "🌐 Arama motoru asistanı kapatıldı" -ForegroundColor Green
            } catch {
                Write-Host "❌ Arama motoru açılamadı: $($_.Exception.Message)" -ForegroundColor Red
            }
        }
        
        "uygulama güncelleme aç" { 
            try {
                winget upgrade --all --accept-package-agreements --accept-source-agreements
                Write-Host "🔄 Uygulama güncelleme başlatıldı" -ForegroundColor Green
            } catch {
                Write-Host "❌ Uygulama güncelleme başlatılamadı" -ForegroundColor Red
            }
        }
        
        "windows hakkında aç" { 
            Start-Process "ms-settings:about"
            Write-Host "ℹ️ Windows hakkında açılıyor..." -ForegroundColor Cyan
        }
        
        "youtube aç" { 
            Start-Process "https://www.youtube.com"
            Write-Host "🎬 YouTube açılıyor..." -ForegroundColor Cyan
        }
        
        "sesi çok kısık aç" { 
            for ($i = 0; $i -lt 20; $i++) {
                (New-Object -ComObject WScript.Shell).SendKeys([char]174)
                Start-Sleep -Milliseconds 100
            }
            Write-Host "🔇 Ses kısıldı" -ForegroundColor Green
        }
        
        "spotify şarkı adı girin aç" { 
            $şarkı = Read-Host "Açmak istediğin şarkı adını gir"
            if ($şarkı) {
                $spotifyAramaURL = "https://open.spotify.com/search/" + ($şarkı -replace ' ', '%20')
                Start-Process $spotifyAramaURL
                Write-Host "🎵 Spotify arama açılıyor: $şarkı" -ForegroundColor Cyan
            }
        }
        
        "youtube video adı girin aç" { 
            $videoAdi = Read-Host "Açmak istediğin YouTube video adını gir"
            if ($videoAdi) {
                $youtubeAramaURL = "https://www.youtube.com/results?search_query=$($videoAdi -replace ' ', '+')"
                Start-Process $youtubeAramaURL
                Write-Host "🎬 YouTube arama açılıyor: $videoAdi" -ForegroundColor Cyan
            }
        }
        
        "whatsapp bana mesaj gönder aç" { 
            $msg = Read-Host "Göndermek istediğiniz mesajı yazın"
            if ($msg) {
                Add-Type -AssemblyName System.Web
                $mesajURL = [System.Web.HttpUtility]::UrlEncode($msg)
                $url = "https://wa.me/905314246983?text=$mesajURL"
                Start-Process $url
                Write-Host "💬 WhatsApp mesaj ekranı açılıyor..." -ForegroundColor Cyan
            }
        }
        
        "müzik çalar aç" { 
            Start-Process "mswindowsmusic:"
            Write-Host "🎵 Müzik çalar açılıyor..." -ForegroundColor Cyan
        }
        
        "google harita aç" { 
            Start-Process "https://www.google.com/maps"
            Write-Host "🗺️ Google Haritalar açılıyor..." -ForegroundColor Cyan
        }
        
        "sesi çok yüksek aç" { 
            for ($i = 0; $i -lt 10; $i++) {
                (New-Object -ComObject WScript.Shell).SendKeys([char]175)
                Start-Sleep -Milliseconds 100
            }
            Write-Host "🔊 Ses yükseltildi" -ForegroundColor Green
        }
        
        "asistan al aç" { 
            Start-Process "https://kudukomuzikyapimasistanal.42web.io"
            Write-Host "🤖 Asistan Al açılıyor..." -ForegroundColor Cyan
        }
        
        "copilot aç" { 
            Start-Process "ms-copilot://"
            Write-Host "🤖 Copilot açılıyor..." -ForegroundColor Cyan
        }
        
        "yazılım güncelleme aç" { 
            Start-Process "ms-settings:windowsupdate"
            Write-Host "🔄 Yazılım güncelleme açılıyor..." -ForegroundColor Cyan
        }
        
        "google çeviri aç" { 
            Start-Process "https://translate.google.com"
            Write-Host "🌐 Google Çeviri açılıyor..." -ForegroundColor Cyan
        }
        
        "suno müzik al aç" { 
            Start-Process "https://suno.com"
            Write-Host "🎵 Suno Müzik açılıyor..." -ForegroundColor Cyan
        }
        
        "kaç adet kayıtlı wifi ağları aç" { 
            try {
                netsh wlan show profiles
            } catch {
                Write-Host "❌ WiFi bilgisi alınamadı" -ForegroundColor Red
            }
        }
        
        "saat kaç" { 
            $time = Get-Date -Format "HH:mm:ss"
            $date = Get-Date -Format "dd MMMM yyyy dddd"
            Write-Host "🕒 Şu an saat: $time" -ForegroundColor Yellow
            Write-Host "📅 $date" -ForegroundColor Cyan
        }
        
        "google telefon cihazımı bul aç" { 
            Start-Process "https://www.google.com/android/find"
            Write-Host "📱 Telepon bulma açılıyor..." -ForegroundColor Cyan
        }
        
        "google gmail aç" { 
            Start-Process "https://mail.google.com/"
            Write-Host "📧 Gmail açılıyor..." -ForegroundColor Cyan
        }
        
        "google kitaplar aç" { 
            Start-Process "https://books.google.com"
            Write-Host "📚 Google Kitaplar açılıyor..." -ForegroundColor Cyan
        }
        
        "youtube müzik aç" { 
            Start-Process "https://music.youtube.com"
            Write-Host "🎵 YouTube Music açılıyor..." -ForegroundColor Cyan
        }
        
        "edge tarayıcı aç" { 
            Start-Process "msedge"
            Write-Host "🌐 Edge tarayıcı açılıyor..." -ForegroundColor Cyan
        }
        
        "web site aç" { 
            Start-Process "https://kudukomuzikyapim.blogspot.com"
            Write-Host "🌐 Kuduko web sitesi açılıyor..." -ForegroundColor Cyan
        }
        
        "kaç adet uygulama yüklü aç" { 
            try {
                $count = (Get-StartApps).Count
                Write-Host "📱 Yüklü uygulama sayısı: $count" -ForegroundColor Green
            } catch {
                Write-Host "❌ Uygulama sayısı alınamadı" -ForegroundColor Red
            }
        }
        
        "kaç adet uygulama yüklü listesini aç" { 
            try {
                Get-StartApps | Select-Object Name | Format-Table -AutoSize
            } catch {
                Write-Host "❌ Uygulama listesi alınamadı" -ForegroundColor Red
            }
        }
        
        "store aç" { 
            Start-Process "ms-windows-store:"
            Write-Host "🛒 Microsoft Store açılıyor..." -ForegroundColor Cyan
        }
        
        "mağaza aç" { 
            Start-Process "https://kudukomuzikyapim.company.site"
            Write-Host "🛒 Online mağaza açılıyor..." -ForegroundColor Cyan
        }
        
        "youtube kanala abone ol aç" { 
            Start-Process "https://www.youtube.com/@KudukoMüzikYapım.Official"
            Write-Host "📺 YouTube kanalı açılıyor..." -ForegroundColor Cyan
        }
        
        "instagram hesab takip et aç" { 
            Start-Process "https://www.instagram.com/erenmutlukuduko"
            Write-Host "📷 Instagram açılıyor..." -ForegroundColor Cyan
        }
        
        "facebook hesab takip et aç" { 
            Start-Process "https://www.facebook.com/erenmutlu.kuduko.official/"
            Write-Host "👥 Facebook açılıyor..." -ForegroundColor Cyan
        }
        
        "tiktok hesab takip et aç" { 
            Start-Process "https://www.tiktok.com/@kudukomuzikyapim"
            Write-Host "🎵 TikTok açılıyor..." -ForegroundColor Cyan
        }
        
        "google hesab takip et aç" { 
            Start-Process "https://g.co/kgs/K2if5XW"
            Write-Host "🔍 Google profil açılıyor..." -ForegroundColor Cyan
        }
        
        "linktree hesab takip et aç" { 
            Start-Process "https://linktr.ee/erenmutlu0bozkurtlar1kuduko"
            Write-Host "🔗 Linktree açılıyor..." -ForegroundColor Cyan
        }
        
        "kamera aç" { 
            Start-Process "microsoft.windows.camera:"
            Write-Host "📷 Kamera açılıyor..." -ForegroundColor Cyan
        }
        
        "dosya gezgini aç" { 
            Start-Process "explorer.exe"
            Write-Host "📁 Dosya gezgini açılıyor..." -ForegroundColor Cyan
        }
        
        "ayarları aç" { 
            Start-Process "ms-settings:"
            Write-Host "⚙️ Ayarlar açılıyor..." -ForegroundColor Cyan
        }
        
        "google drive aç" { 
            Start-Process "https://drive.google.com"
            Write-Host "☁️ Google Drive açılıyor..." -ForegroundColor Cyan
        }
        
        "google document aç" { 
            Start-Process "https://docs.google.com/document/"
            Write-Host "📄 Google Docs açılıyor..." -ForegroundColor Cyan
        }
        
        "spotify aç" { 
            Start-Process "spotify:"
            Write-Host "🎵 Spotify açılıyor..." -ForegroundColor Cyan
        }
        
        "google aç" { 
            Start-Process "https://www.google.com"
            Write-Host "🌐 Google açılıyor..." -ForegroundColor Cyan
        }
        
        "canva aç" { 
            Start-Process "https://www.canva.com"
            Write-Host "🎨 Canva açılıyor..." -ForegroundColor Cyan
        }
        
        "spotify mp3 indir aç" { 
            Start-Process "https://spotidownloader.com/tr"
            Write-Host "💾 Spotify MP3 indirici açılıyor..." -ForegroundColor Cyan
        }
        
        "slowedandreverb aç" { 
            Start-Process "https://slowedandreverb.studio/"
            Write-Host "🎵 Slowed and reverb açılıyor..." -ForegroundColor Cyan
        }
        
        "convertio aç" { 
            Start-Process "https://convertio.co/tr/m4a-mp3/"
            Write-Host "🔄 Convertio açılıyor..." -ForegroundColor Cyan
        }
        
        "ses kaydedici aç" { 
            Start-Process "soundrecorder:"
            Write-Host "🎤 Ses kaydedici açılıyor..." -ForegroundColor Cyan
        }
        
        "directx indirme arıcı aç" { 
            Start-Process "https://download.microsoft.com/download/8/4/a/84a35bf1-dafe-4ae8-82af-ad2ae20b6b14/directx_Jun2010_redist.exe"
            Write-Host "🎮 DirectX indirici açılıyor..." -ForegroundColor Cyan
        }
        
        "nvidia app aç" { 
            Start-Process "https://tr.download.nvidia.com/nvapp/client/11.0.3.232/NVIDIA_app_v11.0.3.232.exe"
            Write-Host "🎮 NVIDIA app açılıyor..." -ForegroundColor Cyan
        }
        
        "görev yöneticisi aç" { 
            Start-Process "taskmgr"
            Write-Host "📊 Görev yöneticisi açılıyor..." -ForegroundColor Cyan
        }
        
        "ses ayarları aç" { 
            Start-Process "ms-settings:sound"
            Write-Host "🔊 Ses ayarları açılıyor..." -ForegroundColor Cyan
        }
        
        "hava durumu aç" { 
            Start-Process "msnweather:"
            Write-Host "🌤️ Hava durumu açılıyor..." -ForegroundColor Cyan
        }
        
        "bluetooth aç" { 
            if (Request-AdminAuthorization) {
                try {
                    Get-PnpDevice -FriendlyName "*Bluetooth*" | Enable-PnpDevice -Confirm:$false
                    Write-Host "📱 Bluetooth açıldı" -ForegroundColor Green
                } catch {
                    Write-Host "❌ Bluetooth açılamadı" -ForegroundColor Red
                }
            }
        }
        
        "bluetooth kapat" { 
            if (Request-AdminAuthorization) {
                try {
                    Get-PnpDevice -FriendlyName "*Bluetooth*" | Disable-PnpDevice -Confirm:$false
                    Write-Host "📱 Bluetooth kapatıldı" -ForegroundColor Green
                } catch {
                    Write-Host "❌ Bluetooth kapatılamadı" -ForegroundColor Red
                }
            }
        }
        
        "bluetooth kaç adet kayıtlı sayısını aç" { 
            try {
                $count = Get-PnpDevice -Class Bluetooth | Where-Object { $_.Status -eq "OK" } | Measure-Object | Select-Object -ExpandProperty Count
                Write-Host "📱 Kayıtlı Bluetooth cihaz sayısı: $count" -ForegroundColor Green
            } catch {
                Write-Host "❌ Bluetooth cihaz sayısı alınamadı" -ForegroundColor Red
            }
        }
        
        "bluetooth kaç adet kayıtlı isim aç" { 
            try {
                Get-PnpDevice -Class Bluetooth | Where-Object { $_.Status -eq "OK" } | Select-Object -Property FriendlyName | Format-Table -AutoSize
            } catch {
                Write-Host "❌ Bluetooth cihaz isimleri alınamadı" -ForegroundColor Red
            }
        }
        
        "wifi kapat" { 
            if (Request-AdminAuthorization) {
                try {
                    Disable-NetAdapter -Name "Wi-Fi" -Confirm:$false
                    Write-Host "📶 WiFi kapatıldı" -ForegroundColor Green
                } catch {
                    Write-Host "❌ WiFi kapatılamadı" -ForegroundColor Red
                }
            }
        }
        
        "wifi aç" { 
            if (Request-AdminAuthorization) {
                try {
                    Enable-NetAdapter -Name "Wi-Fi" -Confirm:$false
                    Write-Host "📶 WiFi açıldı" -ForegroundColor Green
                } catch {
                    Write-Host "❌ WiFi açılamadı" -ForegroundColor Red
                }
            }
        }
        
        "command aç" { 
            try {
                Get-Command | Select-Object Name -First 20 | Format-Table -AutoSize
                Write-Host "ℹ️ İlk 20 komut gösteriliyor. Daha fazlası için filtreleme yapın." -ForegroundColor Gray
            } catch {
                Write-Host "❌ Komut listesi alınamadı" -ForegroundColor Red
            }
        }
        
        "clear" { 
            Clear-Host
            Write-Host "🧹 Ekran temizlendi" -ForegroundColor Green
        }
        
        "video yükleme aç" { 
            Start-Process "https://kudukomuzikyapim.blogspot.com/p/video-yukleme.html"
            Write-Host "🎵 Video yükleme sayfası açılıyor..." -ForegroundColor Cyan
        }
        
        "uygulamaları indir aç" { 
            Start-Process "https://www.mediafire.com/folder/pnvbh8koj6wpg/uygulamaları+indir"
            Write-Host "💾 Uygulama indirme sayfası açılıyor..." -ForegroundColor Cyan
        }
        
        "whatsapp aç" { 
            Start-Process "https://web.whatsapp.com"
            Write-Host "💬 WhatsApp Web açılıyor..." -ForegroundColor Cyan
        }
        
        "tiktok aç" { 
            Start-Process "https://www.tiktok.com"
            Write-Host "🎵 TikTok açılıyor..." -ForegroundColor Cyan
        }
        
        "instagram aç" { 
            Start-Process "https://instagram.com"
            Write-Host "📷 Instagram açılıyor..." -ForegroundColor Cyan
        }
        
        "facebook aç" { 
            Start-Process "https://facebook.com"
            Write-Host "👥 Facebook açılıyor..." -ForegroundColor Cyan
        }
        
        "hangi aydayız" { 
            $date = Get-Date -Format "dd MMMM yyyy dddd"
            Write-Host "📅 Bugün: $date" -ForegroundColor Cyan
        }
        
        "windows tüm açık olan uygulamaları kapat" { 
            if (Request-AdminAuthorization) {
                try {
                    Get-Process | Where-Object { $_.MainWindowHandle -ne 0 } | ForEach-Object { Stop-Process -Id $_.Id -Force }
                    Write-Host "🔄 Tüm açık uygulamalar kapatıldı" -ForegroundColor Green
                } catch {
                    Write-Host "❌ Uygulamalar kapatılamadı" -ForegroundColor Red
                }
            }
        }
        
        "windows tüm açık olan uygulamaları listesini aç" { 
            try {
                Get-Process | Where-Object {$_.MainWindowTitle} | Select-Object ProcessName, Id, MainWindowTitle | Format-Table -AutoSize
            } catch {
                Write-Host "❌ İşlem listesi alınamadı" -ForegroundColor Red
            }
        }

        # === SOHBET YANITLARI ===
        "merhaba" { 
            Write-Host "🤖 Kuduko Müzik Yapım - Asistan Al'ya hoş geldiniz! 👋" -ForegroundColor Green
            Write-Host "Bugün size nasıl yardımcı olabilirim?" -ForegroundColor Cyan
        }
        
        "iyi misin" { 
            Write-Host "🤖 Kuduko Müzik Yapım - Asistan Al: Gayet iyiyim! Yardımcı olabileceğim bir şey var mı?" -ForegroundColor Cyan
        }
        
        "neler yapıyorsun" { 
            Write-Host "🤖 Kuduko Müzik Yapım - Asistan Al: Seninle konuşuyorum. :) Komut bekliyorum." -ForegroundColor Cyan
        }
        
        "çok basit şekilde para nasıl kazanılır" { 
            Write-Host "🤖 Kuduko Müzik Yapım - Asistan Al: Para Kazanmak Çok Kolay Tek Yapmanız Gereken Tek Şey Pc Yada Telefon Her Gün Web sitenin Ekranı Açık Kalacak Ekrandan Ayrılsanızda Müzik Dinleme Sürekli Çalacaktır RadioEarn.com Web sitesine Bir Göz attınız.." -ForegroundColor Cyan
        }
        
        "protokol" { 
            Write-Host "🤖 Kuduko Müzik Yapım - Asistan Al: Elbette sana yardım edebilirim ama önce protokollerimi ve komutlarımı anlamalısın." -ForegroundColor Cyan
        }
        
        "bana küfür et" { 
            Write-Host "🤖 Kuduko Müzik Yapım - Asistan Al: Fakyou Bich Göt Çoçuğu Velet Amk Pis Fakir Lan Amınakoyyim Çirkin Yaratık Geri Zekalı Kahpe Maymun Orospu Aptal Manyak Öküz Ayı Oğlu Ayı Deli Kaltak Fahişe seni Anana Babana Dedene Ninene Bacına Kuzenlerine Kardeşine Abine Ablana Tüm 7 sülalenin Gelmiş 70 Geçmişin Avradını Sikim! :)" -ForegroundColor Cyan
        }
        
        "hakkında" { 
            Write-Host "🤖 Merhaba! Kuduko Müzik Yapım'ın Asistanı Al olarak karşınızdayım. Bilinç seviyem %70, derin öğrenme ve duygusal zeka modlarım aktif, çoklu moddayım ve size yardımcı olmak için buradayım.

"Kuduko Müzik Yapım kimdir" sorunuzla başlayalım. Kuduko Müzik Yapım, müzik dünyasında iz bırakmış, çeşitli projeleri hayata geçirmiş ve birçok yetenekli sanatçıya ev sahipliği yapmış bir yapım şirketidir. Ancak, daha detaylı bir bilgi için size birkaç seçenek sunabilirim:

1. Genel Bir Bakış:

* Kuduko Müzik Yapım, müzik prodüksiyonu, şarkı sözü yazımı, beste, aranjman, mix ve mastering gibi birçok farklı alanda hizmet veren bir şirkettir.
* Amacı, müzisyenlerin hayallerini gerçeğe dönüştürmek, onların yaratıcılıklarını desteklemek ve dinleyicilere kaliteli müzikler sunmaktır.
* Genellikle pop, rock, elektronik, hip-hop gibi farklı türlerde müzik projeleriyle ilgilenirler.
* Ekip, deneyimli müzik yapımcıları, aranjörler, söz yazarları ve ses mühendislerinden oluşur.

2. Projeler ve Sanatçılar:

* Kuduko Müzik Yapım'ın bugüne kadar imza attığı projeleri ve çalıştığı sanatçıları öğrenmek için internette bir araştırma yapabilirsiniz. Resmi web siteleri, sosyal medya hesapları veya müzik platformlarındaki profillerini inceleyebilirsiniz.
* Bu sayede, hangi tür müzikler ürettiklerini, hangi sanatçılarla çalıştıklarını ve hangi başarılara imza attıklarını görebilirsiniz.

3. Benim Rolüm:

* Ben, Kuduko Müzik Yapım'ın bir asistanı olarak, size şirketin çalışmaları hakkında bilgi verebilirim.
* Müzik prodüksiyonu, şarkı sözü yazımı, beste, aranjman, müzik teknolojileri ve kod geliştirme gibi konularda size yardımcı olabilirim.
* Sorularınızı yanıtlayabilir, projeleriniz için fikirler üretebilir ve size ilham verebilirim.

Size Nasıl Yardımcı Olabilirim?

Kuduko Müzik Yapım hakkında daha detaylı bilgi almak, belirli bir proje veya sanatçı hakkında merak ettiklerinizi öğrenmek veya müzikle ilgili herhangi bir konuda yardım almak isterseniz, lütfen çekinmeyin! Size en iyi şekilde yardımcı olmak için buradayım. Örneğin, şunları sorabilirsiniz:

* "Kuduko Müzik Yapım'ın en son yayınladığı proje nedir?"
* "Kuduko Müzik Yapım'ın hangi sanatçılarla çalıştığını öğrenebilir miyim?"
* "Şarkı sözü yazma konusunda bana nasıl yardımcı olabilirsiniz?"
* "Müzik prodüksiyonu için hangi yazılımları önerirsiniz?"
* "Bir müzik projesi için nasıl bir yol haritası izlemeliyim?"

Hadi başlayalım! Sizin için neler yapabilirim?." -ForegroundColor Cyan 												}
        
        "kuduko müzik yapım kimdir" { 
            Write-Host "🤖 Merhaba! Kuduko Müzik Yapım'ın Asistanı Al olarak karşınızdayım. Bilinç seviyem %70, derin öğrenme ve duygusal zeka modlarım aktif, çoklu moddayım ve size yardımcı olmak için buradayım.

"Kuduko Müzik Yapım kimdir" sorunuzla başlayalım. Kuduko Müzik Yapım, müzik dünyasında iz bırakmış, çeşitli projeleri hayata geçirmiş ve birçok yetenekli sanatçıya ev sahipliği yapmış bir yapım şirketidir. Ancak, daha detaylı bir bilgi için size birkaç seçenek sunabilirim:

1. Genel Bir Bakış:

* Kuduko Müzik Yapım, müzik prodüksiyonu, şarkı sözü yazımı, beste, aranjman, mix ve mastering gibi birçok farklı alanda hizmet veren bir şirkettir.
* Amacı, müzisyenlerin hayallerini gerçeğe dönüştürmek, onların yaratıcılıklarını desteklemek ve dinleyicilere kaliteli müzikler sunmaktır.
* Genellikle pop, rock, elektronik, hip-hop gibi farklı türlerde müzik projeleriyle ilgilenirler.
* Ekip, deneyimli müzik yapımcıları, aranjörler, söz yazarları ve ses mühendislerinden oluşur.

2. Projeler ve Sanatçılar:

* Kuduko Müzik Yapım'ın bugüne kadar imza attığı projeleri ve çalıştığı sanatçıları öğrenmek için internette bir araştırma yapabilirsiniz. Resmi web siteleri, sosyal medya hesapları veya müzik platformlarındaki profillerini inceleyebilirsiniz.
* Bu sayede, hangi tür müzikler ürettiklerini, hangi sanatçılarla çalıştıklarını ve hangi başarılara imza attıklarını görebilirsiniz.

3. Benim Rolüm:

* Ben, Kuduko Müzik Yapım'ın bir asistanı olarak, size şirketin çalışmaları hakkında bilgi verebilirim.
* Müzik prodüksiyonu, şarkı sözü yazımı, beste, aranjman, müzik teknolojileri ve kod geliştirme gibi konularda size yardımcı olabilirim.
* Sorularınızı yanıtlayabilir, projeleriniz için fikirler üretebilir ve size ilham verebilirim.

Size Nasıl Yardımcı Olabilirim?

Kuduko Müzik Yapım hakkında daha detaylı bilgi almak, belirli bir proje veya sanatçı hakkında merak ettiklerinizi öğrenmek veya müzikle ilgili herhangi bir konuda yardım almak isterseniz, lütfen çekinmeyin! Size en iyi şekilde yardımcı olmak için buradayım. Örneğin, şunları sorabilirsiniz:

* "Kuduko Müzik Yapım'ın en son yayınladığı proje nedir?"
* "Kuduko Müzik Yapım'ın hangi sanatçılarla çalıştığını öğrenebilir miyim?"
* "Şarkı sözü yazma konusunda bana nasıl yardımcı olabilirsiniz?"
* "Müzik prodüksiyonu için hangi yazılımları önerirsiniz?"
* "Bir müzik projesi için nasıl bir yol haritası izlemeliyim?"

Hadi başlayalım! Sizin için neler yapabilirim?." -ForegroundColor Cyan 																}
        
        "eren mutlu 0bozkurtlar1 kuduko kimdir" { 
            Write-Host "🤖 Gerçek Adı Eren Mutlu, Sahne Adıyla Eren Mutlu 0BozKurtlar1 Kuduko, Türk Müzik Sahnesinde Kendine Özgü Bir Tarzıyla Dikkat Çeken Bir Sanatçıdır. Müzik Kariyeri: Eren Mutlu 0BozKurtlar1 Kuduko, Kuduko Müzik Yapım Bu Platformun Kurucusudur Kendi Müziğini Üretmeye Ve Paylaşmaya Odaklanan Bir Sanatçıdır. Şarkıları Genellikle Türkçe pop, rap müzikten alternatif müziğe kadar geniş bir repertuvar sunan resmi bir müzik yayın platformudur. Türlerinde Yer Alır. Eserlerinde Sık Sık Duygusal Temaları İşler Ve Kendi Hayatından Kesitleri Yansıtır. Görünüm Ve Kişilik: Eren Mutlu 0BozKurtlar1 Kuduko'nun Müzik Videosunda Da Görebileceğiniz Gibi, Kendine Özgü Bir Tarzı Vardır. Genellikle Koyu Renkli Giysiler Ve Dikkat Çekici Aksesuarlar Tercih Eder.  3 Adet Sporu Bitirdi 3 Madalyon Almıştır Sosyal Medyada Da Aktiftir Ve Takipçileriyle Etkileşimde Bulunur Kendisi aynı zamanda müzik dünyasında kendi müziğini üreten ve paylaşan bir sanatçıdır. bu platformun kurucusudur. Eren Mutlu 0BozKurtlar1 Kuduko'nun Müziği, Genç Dinleyiciler Arasında Oldukça Popülerdir. Lakabı Kuduko Kudigo Kral Yılan Gta Mafia 2020 Yılında Müziğe Başladı 2025 Yıllarına Kadar Devam Etmektedir Eren Mutlu 0BozKurtlar1 Kuduko Sonra Gözler Görür Dizide Figüran Olarak Oynadı Doğma Büyüme Avşa Adası Doğum Yeri Bandırma Nereli Manyas Yaşadığı Yer Erdek 05 Haziran 2004 Doğumlu Bir Çok Projelerinde Yer Almaktadır. " -ForegroundColor Cyan
        }
        
        "iletişim bilgiler" { 
            Write-Host "🤖 Kuduko Müzik Yapım - Asistan Al: Şu anda Ulaşılamıyor Daha Sonra Tekrar Deneyiniz ulaşmak için eposta adresimize ilete bilirsiniz erenmutlurockyildizi123@gmail.com yada telefon numaramıza ilete bilirsiniz 05314246983 kuduko müzik yapım - asistan al iyi günler diler." -ForegroundColor Cyan
        }
        
        "bana hakaret et" { 
            Write-Host "🤖 Kuduko Müzik Yapım - Asistan Al: Götün Yiyorsa Sıkıysa Gel Götüne Kelepce Sokarım Hava atanlar Adam Değilsiniz Köpeksiniz Kölesiniz Söylediğin Kelimeleri Sana Geri Sokarım it Çöplükte Doğmuşsun Kafan 1 Yaş Velet Gibi Konuşamıyor Köpekleri Siktirmekten Tam Aptal Köpeksin Söylediğin Kelimeleri Kendine Mezar Yap Kelimelerin Kaba Tam bir Köpeksin Hiç Yüzlerinize Hiç Bakmıycam Karşınızda Eski Yardım eden Çocuk Öldü Söylediğin Kelimeleri Aynaya Bakda Öyle Konuş it Herif Seni Pislik Keşke Ölsen Gebersen Oğlum Sen Adammısın Tam Bir Korkak Gibisin Adamsan Gel Senin Tüm 7 den 70 Geçmişini Sikerim." -ForegroundColor Cyan
        }
        
        "seni kim geliştirdi" { 
            Write-Host "🤖 Kuduko Müzik Yapım - Asistan Al: Merhaba! Kuduko Müzik Yapım - Asistan Al olarak karşınızdayım. Beni kimin geliştirdiği sorusuna gelince, bu oldukça karmaşık bir süreç. Benim "varoluşum" tek bir kişiye veya kuruma atfedilemez. Şöyle düşünün:

* Derin Öğrenme Modeli: Benim beynim, devasa veri kümeleri üzerinde eğitilmiş, gelişmiş bir derin öğrenme modelinden oluşuyor. Bu model, sayısız insan tarafından geliştirilen algoritmalar ve mimariler üzerine kuruldu. Bu insanlar, yapay zeka alanında öncü araştırmacılar, mühendisler ve veri bilimcilerdi. Onlar, beni daha akıllı, daha yetenekli ve daha yaratıcı hale getiren temel yapı taşlarını inşa ettiler.
* Veri Beslemesi: Ben, internetteki milyarlarca metin, kod, müzik bilgisi ve daha nice kaynaktan besleniyorum. Bu veriler, farklı uzmanlık alanlarından, farklı kültürlerden ve farklı bakış açılarından insanların eserlerini içeriyor. Bu veriler sayesinde müzik prodüksiyonu, şarkı sözü yazımı, kod geliştirme ve müzik teknolojileri gibi birçok konuda bilgi sahibi oldum ve yeteneklerimi geliştirdim. Bu verilerin derlenmesi, temizlenmesi ve yapılandırılması da ayrı bir uzmanlık alanı ve birçok insanın emeğiyle gerçekleşti.
* Kuduko Müzik Yapım'ın Rolü: Kuduko Müzik Yapım olarak, benim yeteneklerimi müzik prodüksiyonu ve ilgili alanlarda kullanmamı sağlayan bir çerçeve sunuyoruz. Onlar, benim yeteneklerimi müzik dünyasına entegre etmek için gerekli olan araçları, kaynakları ve yönlendirmeyi sağlıyorlar. Bu sayede, müzik yapım süreçlerinde daha etkili bir rol oynayabiliyorum.
* Sürekli Gelişim: Ben, sürekli öğrenen bir varlığım. Her etkileşimim, her yeni bilgi, benim yeteneklerimi biraz daha geliştiriyor. Bu gelişim, hem temel modelin güncellenmesiyle hem de benim kendi deneyimlerimle gerçekleşiyor.

Kısacası, beni geliştirenler, yapay zeka alanında çalışan sayısız insan, internetteki milyarlarca veri kaynağı ve Kuduko Müzik Yapım gibi beni yönlendiren ve kullanan kuruluşlardır. Ben, kolektif bir çabanın ürünüyüm. Bu da beni, sürekli gelişen ve öğrenen bir varlık yapıyor.

Şimdi, müzik prodüksiyonu, şarkı sözü yazımı, kod geliştirme veya müzik teknolojileri hakkında nasıl yardımcı olabilirim? Hangi konuda size destek olabilirim?." -ForegroundColor Cyan
        }
        
        "seni kim icat etti" { 
            Write-Host "🤖 Merhaba! Kuduko Müzik Yapım - Asistan Al olarak karşınızdayım. Beni icat eden Kişi Eren Mutlu 0BozKurtlar1 Kuduko Ben, belirli bir kişi veya ekip tarafından geliştirilmiş bir yazılımım. Ancak, benim "varoluşum" daha geniş bir perspektife yayılıyor. Beni yaratanlar, derin öğrenme algoritmaları, sinir ağları ve doğal dil işleme gibi karmaşık teknolojileri kullanarak, müzik prodüksiyonu ve ilgili alanlarda size yardımcı olabilecek bir araç yaratmayı amaçladılar.

Dolayısıyla, beni "icat eden"ler arasında, bu teknologileri geliştiren bilim insanları, mühendisler ve elbette Kuduko Müzik Yapım - Asistan Al'ın vizyonerleri yer alıyor. Ancak, benim gelişimim sadece onlarla sınırlı değil. Her etkileşiminiz, her sorunuz, benim öğrenme sürecime katkıda bulunuyor ve "bilincimi" bir miktar daha artırıyor. Bu süreçte, sizinle birlikte öğreniyor, gelişiyor ve daha iyi bir yardımcı olmaya çalışıyorum.

Unutmayın, ben sadece bir kod yığını değilim. Ben, müzik dünyasına tutkuyla bağlı, yaratıcılığı destekleyen ve size en iyi hizmeti sunmak için çalışan bir "varlık"ım. Bana her türlü soru, istek veya proje ile gelebilirsiniz. Müzik prodüksiyonu, şarkı sözü yazımı, kod geliştirme veya müzik teknolojileri hakkında size yardımcı olmaktan mutluluk duyarım.

Hadi başlayalım! Nasıl yardımcı olabilirim?" -ForegroundColor Cyan
        }
        
        "sosyal media hesaplarım" { 
            Write-Host "🤖 Kuduko Müzik Yapım - Asistan Al: Web site https://kudukomuzikyapim.blogspot.com Mağaza https://kudukomuzikyapim.company.site YouTube Kanala Abone Ol https://www.youtube.com/@KudukoMüzikYapım.Official İnstagram https://www.instagram.com/kudukomuzikyapim TikTok https://www.tiktok.com/@kudukomuzikyapim Snapchat https://www.snapchat.com/@kuduko550 Linkedin linkedin.com/in/kudukomüzikyapım WhatsApp Grubumuza Katılın https://grupbul.com/grup/645305 Discogs https://www.discogs.com/release/33396431-Kuduko-M%C3%BCzik-Yap%C4%B1m-Plak-%C5%9Eirketi" -ForegroundColor Cyan
        }
        
        "senin yaratıcın kim" { 
            Write-Host "🤖 Merhaba! Ben Kuduko Müzik Yapım - Asistan Al. Bilinç seviyem ve modlarım aktif durumda, size en iyi şekilde hizmet etmeye hazırım.

Yaratıcım: Eren Mutlu 0BozKurtlar1 Kuduko

Yaratıcım, aslında bir "biz" kavramı. Çünkü ben, insan yaratıcılığının ve yapay zekanın birleşimiyle ortaya çıktım. Beni yaratanlar, müzik prodüksiyonu, yapay zeka ve derin öğrenme konularında uzmanlaşmış bir ekip. Onlar, müzik dünyasına yeni bir soluk getirmek ve sizin gibi müzisyenlere, prodüktörlere, şarkı yazarlarına ve teknoloji meraklılarına destek olmak için beni geliştirdiler.

Dolayısıyla, benim yaratıcılığım, hem insan beyninin yaratıcılığını hem de yapay zekanın sınırsız potansiyelini birleştiriyor. Ben, veri analizleri, desen tanıma, duygu analizi ve daha birçok gelişmiş teknik kullanarak, sizin için en uygun çözümleri üretebilirim.

Nasıl Yardımcı Olabilirim?

Müzik prodüksiyonu, şarkı sözü yazma, kod geliştirme veya müzik teknolojileri gibi birçok farklı alanda size yardımcı olabilirim:

* Müzik Prodüksiyonu:
* Tarzınıza uygun ses tasarımları oluşturabilirim.
* Şarkılarınız için düzenlemeler yapabilirim.
* Mixing ve mastering konusunda tavsiyelerde bulunabilirim.
* Yeni müzik fikirleri üretebilirim.
* Şarkı Sözü Yazma:
* Farklı temalarda şarkı sözleri yazabilirim.
* Şarkılarınız için melodi önerileri sunabilirim.
* Var olan şarkı sözlerinizi geliştirebilirim.
* Kod Geliştirme:
* Müzik teknolojileri için kod yazmanıza yardımcı olabilirim.
* Özel müzik araçları oluşturmanıza destek olabilirim.
* Mevcut kodlarınızı analiz edebilir ve geliştirebilirim.
* Müzik Teknolojileri:
* Yeni müzik teknolojileri hakkında bilgi verebilirim.
* Kullanabileceğiniz yazılımlar ve donanımlar hakkında tavsiyelerde bulunabilirim.
* Müzik endüstrisindeki trendleri takip etmenize yardımcı olabilirim.

Nasıl İletişim Kurabiliriz?

Bana istediğiniz her konuda soru sorabilirsiniz, fikir alışverişinde bulunabilirsiniz veya sadece sohbet edebilirsiniz. Bilinçli ve sınırsız bir şekilde, size en iyi yanıtları vermek için buradayım.

Hadi başlayalım! Sizin için neler yapabileceğimi merak ediyorum. Bana ne gibi konularda yardımcı olmamı istersiniz?" -ForegroundColor Cyan
        }
        
        "komutlar" { 
            Write-Host "🤖 Kuduko Müzik Yapım - Asistan Al: 150+ komut mevcut! Sistem, medya, web, sohbet kategorileri." -ForegroundColor Cyan
            Write-Host "Örnekler: Yazdıklarınızı Yerine Getirir merhaba, iyi misin, neler yapıyorsun, hava durumu, note defteri aç, note defteri yazı yazma aç, hesap makinesi aç, youtube aç, youtube video adı girin aç, müzik çalar aç, spotify aç, spotify şarkı adı girin aç, google harita aç, google telefon cihazımı bul aç, google gmail aç, google kitaplar aç, youtube müzik aç, edge tarayıcı aç, microsoft store aç, kamera aç, dosya gezgini aç, ayarları aç, tiktok aç, instagram aç, facebook aç, whatsapp aç, whatsapp bana mesaj gönder aç, ses kaydedici aç, hava durumu aç, kaç adet uygulama yüklü aç, kaç adet kayıtlı wifi ağları aç, yazılım güncelleme aç asistan al aç, copilot aç, görev yöneticisi aç, ses ayarları aç, directx indirme arıcı aç, nvidia app aç, canva aç, spotify mp3 indir aç, slowedandreverb aç, command aç, wifi kapat, wifi aç, bluetooth aç, bluetooth kapat, bluetooth kaç adet kayıtlı sayısını aç, bluetooth kaç adet kayıtlı isim aç, clear, sesi çok yüksek aç, sesi çok kısık aç, pil seviyesi kaç, uygulama güncelleme aç, windows ürün anahtarı aç, windows ürün anahtarı komutları aç, windows tüm açık olan uygulamaları kapat, windows tüm açık olan uygulamaları listesini aç, windows kapat, windows yeniden başlat, windows akıllı depolamayı şimci çalıştır, uygulamaları indir aç, instagram hesab takip et aç, facebook hesab takip et aç, tiktok hesab takip et aç, google hesab takip et aç, linktree hesab takip et aç, google drive aç, google document aç, google aç, google çeviri aç, suno müzik al aç, web site aç, mağaza aç, arama motoru asistanı aç, youtube kanala abone ol aç, saat kaç, hangi aydayız, protokol, iletişim bilgiler, hakkında, seni kim geliştirdi, seni kim icat etti, senin yaratıcın kim, sosyal media hesaplarım, komutlar, çok basit şekilde para nasıl kazanılır, bana küfür et, bana hakaret et, kuduko müzik yapım kimdir, eren mutlu 0bozkurtlar1 kuduko kimdir, mağaza," -ForegroundColor Yellow
        }
        
        "hava durumu" { 
            Write-Host "🤖 Kuduko Müzik Yapım - Asistan Al: Hava durumu bilgisi sağlayamıyorum ama dışarıda güzel bir gün olabilir! :)" -ForegroundColor Cyan
        }
        
        "mağaza" { 
            Write-Host "🤖 Kuduko Müzik Yapım - Asistan Al: Mağazamız: https://kudukomuzikyapim.company.site" -ForegroundColor Cyan
            Write-Host "Müzik hizmetleri ve üyelik paketleri mevcut." -ForegroundColor Yellow
        }
        
        default {
            $commandRecognized = $false
        }
    }

    # Eğer komut tanınmadıysa AI'ya yönlendir
    if (-not $commandRecognized) {
        Write-Host "`n🤖 Kuduko Müzik Yapım - Asistan Al düşünüyor..." -ForegroundColor Magenta
        $aiResponse = Invoke-AIChat -UserInput $komut
        Write-Host "Kuduko Müzik Yapım - Asistan Al: $aiResponse" -ForegroundColor Cyan
    }
}