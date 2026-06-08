# actions/open_app.py

import subprocess
import os

def open_app(app_name: str) -> str:
    """Windows'ta uygulama açar"""
    app_name_lower = app_name.lower()
    
    # Spotify için özel yol
    if "spotify" in app_name_lower:
        # Windows 11'de Spotify için olası yollar
        spotify_paths = [
            os.path.expandvars(r"%LOCALAPPDATA%\Spotify\Spotify.exe"),
            os.path.expandvars(r"%APPDATA%\Spotify\Spotify.exe"),
            r"C:\Program Files\WindowsApps\SpotifyAB.SpotifyMusic_*",
        ]
        
        for path in spotify_paths:
            try:
                if "*" in path:
                    # Wildcard ile arama
                    import glob
                    matches = glob.glob(path)
                    if matches:
                        subprocess.Popen([matches[0]])
                        return f"Spotify açılıyor: {matches[0]}"
                elif os.path.exists(path):
                    subprocess.Popen([path])
                    return f"Spotify açılıyor: {path}"
            except:
                continue
        
        # Normal start komutu ile dene
        subprocess.Popen(["start", "spotify:"], shell=True)
        return "Spotify başlatılıyor..."
    
    # Diğer uygulamalar için normal işlem
    try:
        subprocess.Popen(["start", app_name], shell=True)
        return f"{app_name} açılıyor..."
    except Exception as e:
        return f"{app_name} açılamadı: {str(e)}"

"""
Uygulama açma — Windows Start-Process / URI desteği ile çalışır.
KUDUKOMUZİKYAPİMASİSTANAL tarafından yapılmıştır — @KUDUKOMUZİKYAPİMASİSTANAL
"""

import os
import subprocess

from actions.windows_utils import open_uri, open_windows_app


# Kısa isimden uygulama yoluna eşleme
APP_ALIASES = {
    "edge":        "Microsoft Edge",
    "chrome":      "Google Chrome",
    "firefox":     "Firefox",
    "terminal":    "Terminal",
    "iterm":       "iTerm",
    "iterm2":      "iTerm",
    "explorer":    "File Explorer",
    "spotify":     "Spotify",
    "vscode":      "Visual Studio Code",
    "vs code":     "Visual Studio Code",
    "code":        "Visual Studio Code",
    "xcode":       "Xcode",
    "notion":      "Notion",
    "slack":       "Slack",
    "discord":     "Discord",
    "whatsapp":    "WhatsApp",
    "telegram":    "Telegram",
    "zoom":        "zoom.us",
    "mail":        "Mail",
    "calendar":    "Calendar",
    "takvim":      "Calendar",
    "notes":       "Notes",
    "notlar":      "Notes",
    "music":       "Music",
    "müzik":       "Music",
    "photos":      "Photos",
    "fotoğraflar": "Photos",
    "maps":        "Maps",
    "haritalar":   "Maps",
    "calculator":  "Calculator",
    "hesap makinesi": "Calculator",
    "system preferences": "System Preferences",
    "system settings": "System Settings",
    "ayarlar":     "System Settings",
    "activity monitor": "Activity Monitor",
    "aktivite monitörü": "Activity Monitor",
    "preview":     "Preview",
    "önizleme":    "Preview",
    "textedit":    "TextEdit",
    "numbers":     "Numbers",
    "pages":       "Pages",
    "keynote":     "Keynote",
    "figma":       "Figma",
    "postman":     "Postman",
    "docker":      "Docker",
    "sequel pro":  "Sequel Pro",
    "tableplus":   "TablePlus",
    "notepad":     "Notepad",
    "not defteri": "Notepad",
    "cmd":         "Command Prompt",
    "powershell":  "PowerShell",
    "explorer":    "File Explorer",
    "dosya gezgini": "File Explorer",
}


def open_app(app_name: str) -> str:
    """Uygulamayı açar, başarı/hata mesajı döndürür."""
    if not app_name:
        return "Uygulama adı belirtilmedi."

    normalized = app_name.lower().strip()
    resolved   = APP_ALIASES.get(normalized, app_name)

    if os.name == "nt":
        ok, detail = open_windows_app(resolved)
        if ok:
            return detail
        ok, detail2 = open_uri(resolved)
        if ok:
            return f"{app_name} acildi."
        return detail or detail2

    try:
        result = subprocess.run(
            ["open", "-a", resolved],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return f"{resolved} açıldı."
        else:
            # Spotlight ile dene
            result2 = subprocess.run(
                ["open", resolved],
                capture_output=True, text=True, timeout=10
            )
            if result2.returncode == 0:
                return f"{app_name} açıldı."
            return f"'{app_name}' bulunamadı veya açılamadı."
    except subprocess.TimeoutExpired:
        return f"'{app_name}' açılırken zaman aşımı."
    except Exception as e:
        return f"Hata: {e}"