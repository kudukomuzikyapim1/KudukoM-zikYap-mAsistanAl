# ═══════════════════════════════════════════════════════════════════
# KUDUKO MUZİK YAPİM ASİSTAN AL
# ═══════════════════════════════════════════════════════════════════

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import datetime
import math
import random
import re
import json
import os
import subprocess
import time
import sys
import webbrowser
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════
# KÜTÜPHANE KONTROLLERİ
# ═══════════════════════════════════════════════════════════════════

try:
    import speech_recognition as sr
    STT_AVAILABLE = True
except ImportError:
    STT_AVAILABLE = False

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

try:
    import pygetwindow as gw
    WINDOW_AVAILABLE = True
except ImportError:
    WINDOW_AVAILABLE = False

try:
    import cv2
    CAMERA_AVAILABLE = True
except ImportError:
    CAMERA_AVAILABLE = False

try:
    import pyautogui
    WA_AVAILABLE = True
except ImportError:
    WA_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("⚠️ psutil yüklü değil! Kurulum: pip install psutil")

# ═══════════════════════════════════════════════════════════════════
# RENKLER (KUDUKO MUZİK YAPİM ASİSTAN AL)
# ═══════════════════════════════════════════════════════════════════

BG_DARK = "#0a0e1a"      # Ana arkaplan
BG_CARD = "#0d1525"      # Kart arkaplanı
BG_DIM = "#111c30"       # Dim arkaplan
ACCENT = "#00cfff"       # Neon mavi
ACCENT_DARK = "#0055aa"  # Koyu mavi
ACCENT2 = "#0055aa"
TEXT = "#c8e8ff"         # Ana metin
TEXT_DIM = "#3a5070"     # Soluk metin
WARN = "#ff4466"         # Kırmızı uyarı
GREEN = "#00ff88"        # Yeşil durum
AMBER = "#ffaa00"        # Sarı uyarı
PURPLE = "#aa66ff"       # Mor

MODULE_COLORS = {
    "NLP": "#00cfff",
    "ANALİZ": "#00ff88",
    "OTOMASYON": "#ffaa00",
    "ZIRH": "#ff6644",
    "BİLİM": "#aa66ff",
    "GÜVENLİK": "#ff4466",
    "TAKTİK": "#ff8800",
    "ÖĞRENME": "#44ddff",
    "KAMERA": "#ff66cc",
    "WHATSAPP": "#25D366",
    "WEB": "#ffaa44",
    "MEDYA": "#ff6688",
}

# ═══════════════════════════════════════════════════════════════════
# KAMERA KONTROL SINIFI (DÜZELTİLMİŞ VERSİYON)
# ═══════════════════════════════════════════════════════════════════

class CameraController:
    """Windows 11 kamera kontrolü, fotoğraf çekme ve kaydetme - DÜZELTİLMİŞ"""
    
    def __init__(self):
        self.camera = None
        self.is_open = False
        self.current_camera_id = 0
        self.photos_dir = Path.home() / "Pictures" / "KUDUKO_MUZIK_YAPIM_ASISTAN_AL_Photos"
        self.photos_dir.mkdir(parents=True, exist_ok=True)
        self.last_photo_path = None
        self.preview_label = None
        self.is_previewing = False
        
    def open_camera_app(self) -> tuple[bool, str]:
        """Windows Kamera uygulamasını açar"""
        try:
            subprocess.Popen("start microsoft.windows.camera:", shell=True)
            return True, "Windows Kamera uygulaması açılıyor."
        except Exception as e:
            return False, f"Kamera uygulaması açılamadı: {str(e)}"
    
    def start_preview(self) -> tuple[bool, str]:
        """Kamera önizlemesini başlatır"""
        if not CAMERA_AVAILABLE:
            return False, "OpenCV yüklü değil. Kurulum: pip install opencv-python pillow"
        
        try:
            if self.camera is not None:
                self.stop_preview()
            
            # Önce indeks 0 dene, sonra indeks 1
            self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not self.camera.isOpened():
                self.camera = cv2.VideoCapture(1, cv2.CAP_DSHOW)
                if not self.camera.isOpened():
                    return False, "Kamera bulunamadı. Lütfen kameranın bağlı olduğundan emin olun."
            
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.is_open = True
            return True, "Kamera önizlemesi başlatıldı."
        except Exception as e:
            return False, f"Kamera hatası: {str(e)}"
    
    def take_photo(self) -> tuple[bool, str, str]:
        """Fotoğraf çeker ve kaydeder - DÜZELTİLMİŞ"""
        # Önce kamerayı aç (eğer kapalıysa)
        if not self.is_open or self.camera is None or not self.camera.isOpened():
            success, msg = self.start_preview()
            if not success:
                return False, msg, ""
        
        try:
            # Kameranın hazır olması için bekle
            time.sleep(0.3)
            
            # Kameradan birkaç kare oku (stabilizasyon için)
            for _ in range(3):
                ret, frame = self.camera.read()
                time.sleep(0.05)
            
            # Son kareyi al
            ret, frame = self.camera.read()
            
            if ret and frame is not None:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"kudukomuzikyapimasistan_photo_{timestamp}.jpg"
                filepath = self.photos_dir / filename
                
                # Fotoğrafı kaydet
                success = cv2.imwrite(str(filepath), frame)
                
                if success:
                    self.last_photo_path = str(filepath)
                    # Başarılı olduktan sonra kamerayı kapat
                    self.stop_preview()
                    return True, f"Fotoğraf çekildi: {filename}", str(filepath)
                else:
                    self.stop_preview()
                    return False, "Fotoğraf kaydedilemedi. Dizin izinlerini kontrol edin.", ""
            else:
                self.stop_preview()
                return False, "Kamera'dan kare alınamadı. Kameranın çalıştığından emin olun.", ""
                
        except Exception as e:
            self.stop_preview()
            return False, f"Fotoğraf çekme hatası: {str(e)}", ""
    
    def take_photo_with_preview(self, parent_window=None) -> tuple[bool, str, str]:
        """Geri sayım göstererek fotoğraf çeker"""
        if not self.is_open or self.camera is None or not self.camera.isOpened():
            success, msg = self.start_preview()
            if not success:
                return False, msg, ""
        
        try:
            if parent_window:
                countdown_window = tk.Toplevel(parent_window)
                countdown_window.title("Fotoğraf Çekiliyor")
                countdown_window.configure(bg=BG_DARK)
                countdown_window.geometry("300x150+500+300")
                countdown_window.transient(parent_window)
                
                count_label = tk.Label(countdown_window, text="3", 
                                       bg=BG_DARK, fg=ACCENT, 
                                       font=("Courier", 48, "bold"))
                count_label.pack(expand=True)
                countdown_window.update()
                
                for i in range(3, 0, -1):
                    count_label.config(text=str(i))
                    countdown_window.update()
                    time.sleep(1)
                
                countdown_window.destroy()
            
            # Kameranın hazır olması için bekle
            time.sleep(0.2)
            
            ret, frame = self.camera.read()
            if not ret or frame is None:
                self.stop_preview()
                return False, "Fotoğraf çekilemedi. Kare alınamadı.", ""
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"kudukomuzikyapimasistan_photo_{timestamp}.jpg"
            filepath = self.photos_dir / filename
            
            cv2.imwrite(str(filepath), frame)
            self.last_photo_path = str(filepath)
            self.stop_preview()
            
            return True, f"Fotoğraf çekildi: {filename}", str(filepath)
        except Exception as e:
            self.stop_preview()
            return False, f"Fotoğraf çekme hatası: {str(e)}", ""
    
    def stop_preview(self):
        """Kamerayı kapatır"""
        if self.camera:
            self.camera.release()
            self.camera = None
        self.is_open = False
        self.is_previewing = False
    
    def close_camera(self):
        """Kamerayı kapatmak için alternatif metod"""
        self.stop_preview()
    
    def list_cameras(self) -> list:
        """Mevcut kameraları listeler"""
        cameras = []
        if not CAMERA_AVAILABLE:
            return ["OpenCV yüklü değil"]
        
        for i in range(5):
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if cap.isOpened():
                cameras.append(f"Kamera {i}")
                cap.release()
        if not cameras:
            cameras.append("Kamera bulunamadı")
        return cameras
    
    def check_camera_status(self) -> dict:
        """Kamera durumunu kontrol eder"""
        status = {
            "available": False,
            "count": 0,
            "photos_count": len(list(self.photos_dir.glob("*.jpg"))),
            "photos_dir": str(self.photos_dir)
        }
        
        if not CAMERA_AVAILABLE:
            status["error"] = "OpenCV yüklü değil"
            return status
        
        for i in range(5):
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if cap.isOpened():
                status["count"] += 1
                status["available"] = True
                cap.release()
        
        return status
    
    def get_photos_list(self) -> list:
        """Çekilen fotoğrafların listesini döndürür"""
        photos = list(self.photos_dir.glob("kudukomuzikyapimasistan_photo_*.jpg"))
        photos.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        return [str(p) for p in photos]

# ═══════════════════════════════════════════════════════════════════
# FOTOĞRAF GALERİSİ PENCERESİ
# ═══════════════════════════════════════════════════════════════════

class PhotoGalleryWindow:
    def __init__(self, parent, camera_controller):
        self.window = tk.Toplevel(parent)
        self.window.title("Kuduko Müzik Yapım - Asistan Al v2.0 - Fotoğraf Galerisi")
        self.window.configure(bg=BG_DARK)
        self.window.geometry("800x600+100+100")
        self.window.transient(parent)
        
        self.camera = camera_controller
        self.current_photo_index = 0
        self.photos = []
        
        self._build_ui()
        self._load_photos()
    
    def _build_ui(self):
        title_frame = tk.Frame(self.window, bg=BG_DARK)
        title_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        tk.Label(title_frame, text="📸 FOTOĞRAF GALERİSİ", 
                 bg=BG_DARK, fg=ACCENT, font=("Courier", 14, "bold")).pack()
        
        self.image_frame = tk.Frame(self.window, bg=BG_DIM, width=600, height=400)
        self.image_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.image_frame.pack_propagate(False)
        
        self.image_label = tk.Label(self.image_frame, bg=BG_DIM, text="Fotoğraf yok")
        self.image_label.pack(expand=True)
        
        control_frame = tk.Frame(self.window, bg=BG_DARK)
        control_frame.pack(fill="x", padx=20, pady=10)
        
        self.prev_btn = tk.Button(control_frame, text="◀ ÖNCEKİ", 
                                   command=self._prev_photo,
                                   bg=BG_DIM, fg=TEXT, font=("Courier", 10, "bold"),
                                   bd=0, pady=8, cursor="hand2")
        self.prev_btn.pack(side="left", padx=5)
        
        self.info_label = tk.Label(control_frame, text="", 
                                    bg=BG_DARK, fg=TEXT_DIM, font=("Courier", 9))
        self.info_label.pack(side="left", expand=True)
        
        self.next_btn = tk.Button(control_frame, text="SONRAKİ ▶", 
                                   command=self._next_photo,
                                   bg=BG_DIM, fg=TEXT, font=("Courier", 10, "bold"),
                                   bd=0, pady=8, cursor="hand2")
        self.next_btn.pack(side="right", padx=5)
        
        bottom_frame = tk.Frame(self.window, bg=BG_DARK)
        bottom_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Button(bottom_frame, text="📂 KLASÖRÜ AÇ", 
                 command=self._open_folder,
                 bg=ACCENT2, fg=TEXT, font=("Courier", 9, "bold"),
                 bd=0, pady=8, cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(bottom_frame, text="🔄 YENİLE", 
                 command=self._load_photos,
                 bg=BG_DIM, fg=TEXT_DIM, font=("Courier", 9),
                 bd=0, pady=8, cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(bottom_frame, text="❌ KAPAT", 
                 command=self.window.destroy,
                 bg=BG_DIM, fg=WARN, font=("Courier", 9),
                 bd=0, pady=8, cursor="hand2").pack(side="right", padx=5)
    
    def _load_photos(self):
        self.photos = self.camera.get_photos_list()
        if self.photos:
            self.current_photo_index = 0
            self._show_photo()
        else:
            self.image_label.config(text="📷 Henüz fotoğraf çekilmedi.\n'Fotoğraf çek' komutunu kullanın.", 
                                   fg=TEXT_DIM, font=("Courier", 12))
            self.info_label.config(text="0 fotoğraf")
            self.prev_btn.config(state="disabled")
            self.next_btn.config(state="disabled")
    
    def _show_photo(self):
        if not self.photos or self.current_photo_index >= len(self.photos):
            return
        
        try:
            from PIL import Image, ImageTk
            
            img = Image.open(self.photos[self.current_photo_index])
            
            frame_width = self.image_frame.winfo_width()
            frame_height = self.image_frame.winfo_height()
            
            if frame_width > 100 and frame_height > 100:
                img.thumbnail((frame_width - 20, frame_height - 20), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo, text="")
            self.image_label.image = photo
            
            filename = Path(self.photos[self.current_photo_index]).name
            self.info_label.config(text=f"{self.current_photo_index + 1} / {len(self.photos)} - {filename}")
            
            self.prev_btn.config(state="normal" if self.current_photo_index > 0 else "disabled")
            self.next_btn.config(state="normal" if self.current_photo_index < len(self.photos) - 1 else "disabled")
            
        except Exception as e:
            self.image_label.config(text=f"Fotoğraf yüklenemedi: {str(e)}", fg=WARN)
    
    def _prev_photo(self):
        if self.current_photo_index > 0:
            self.current_photo_index -= 1
            self._show_photo()
    
    def _next_photo(self):
        if self.current_photo_index < len(self.photos) - 1:
            self.current_photo_index += 1
            self._show_photo()
    
    def _open_folder(self):
        os.startfile(str(self.camera.photos_dir))

# ═══════════════════════════════════════════════════════════════════
# MENÜ PENCERESİ (AÇILIR PENCERE) - KAMERA KONTROLLERİ EKLENDİ
# ═══════════════════════════════════════════════════════════════════

class MenuPopup:
    def __init__(self, parent, assistant_app):
        self.parent = parent
        self.assistant = assistant_app
        self.window = None
        
    def show(self):
        """Menü penceresini göster"""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
            
        self.window = tk.Toplevel(self.parent)
        self.window.title("KUDUKO MUZİK YAPİM ASİSTAN AL - MENÜ")
        self.window.configure(bg=BG_DARK)
        self.window.geometry("350x700")
        self.window.resizable(False, False)
        
        # Pencereyi sağ üst köşeye konumlandır
        self.window.update_idletasks()
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        
        x = parent_x + parent_width - 370
        y = parent_y + 60
        self.window.geometry(f"+{x}+{y}")
        
        # Başlık çubuğu
        title_frame = tk.Frame(self.window, bg=ACCENT_DARK)
        title_frame.pack(fill="x")
        
        tk.Label(title_frame, text="☰ MENÜ", bg=ACCENT_DARK, fg="white", 
                font=("Consolas", 12, "bold")).pack(side="left", padx=15, pady=10)
        
        close_btn = tk.Button(title_frame, text="✕", command=self.close,
                              bg=ACCENT_DARK, fg="white", font=("Consolas", 10, "bold"),
                              bd=0, padx=8, pady=4, cursor="hand2")
        close_btn.pack(side="right", padx=10)
        
        # Kaydırılabilir içerik alanı
        canvas = tk.Canvas(self.window, bg=BG_DARK, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG_DARK)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=330)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse tekerleği ile kaydırma
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Menü başlığı
        tk.Label(scrollable_frame, text="⚡ HIZLI İŞLEMLER", bg=BG_DARK, fg=ACCENT,
                font=("Consolas", 10, "bold")).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Menü butonları stil
        btn_style = {"bg": BG_CARD, "fg": TEXT, "font": ("Consolas", 9),
                     "bd": 0, "padx": 12, "pady": 8, "cursor": "hand2",
                     "anchor": "w", "justify": "left"}
        
        # Hızlı işlem menü seçenekleri
        menu_items = [
            ("🎤 Sesli Komut", self.voice_command),
            ("🗑️ Sohbeti Temizle", self.clear_chat),
            ("📋 Kopyala", self.copy_chat),
            ("💾 Kaydet", self.save_chat),
            ("🎨 Tema Değiştir", self.change_theme),
            ("🔊 Ses Ayarları", self.voice_settings),
            ("📊 Sistem Bilgileri", self.system_info),
            ("🔄 Yenile", self.refresh_all),
            ("ℹ️ Hakkında", self.about),
            ("🚪 Çıkış", self.exit_app)
        ]
        
        for text, command in menu_items:
            btn = tk.Button(scrollable_frame, text=text, command=command, **btn_style)
            btn.pack(fill="x", padx=15, pady=3)
            
            # Hover efekti
            def on_enter(e, b=btn, t=text):
                b.config(bg=BG_DIM, fg=ACCENT)
            def on_leave(e, b=btn):
                b.config(bg=BG_CARD, fg=TEXT)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        
        # Ayraç
        tk.Frame(scrollable_frame, bg=BG_DIM, height=1).pack(fill="x", padx=15, pady=10)
        
        # ═══════════════════════════════════════════════════════════════
        # KAMERA & MEDYA KONTROL BÖLÜMÜ (DÜZELTİLMİŞ KAMERA KONTROLLERİ İLE)
        # ═══════════════════════════════════════════════════════════════
        tk.Label(scrollable_frame, text="📷 KAMERA & MEDYA KONTROL", bg=BG_DARK, fg=PURPLE,
                font=("Consolas", 10, "bold")).pack(anchor="w", padx=15, pady=(0, 10))
        
        # Buton stilleri (menü için özel)
        media_btn_style = {"bg": BG_DIM, "fg": TEXT, "font": ("Consolas", 9),
                           "bd": 0, "padx": 12, "pady": 6, "cursor": "hand2",
                           "anchor": "w", "justify": "left"}
        
        # 1. Buton: Kamera Aç (Önizleme)
        btn_cam_open = tk.Button(scrollable_frame, text="📷 KAMERA AÇ (ÖNİZLEME)", 
                                command=self.open_camera_preview, **media_btn_style)
        btn_cam_open.pack(fill="x", padx=15, pady=2)
        
        # 2. Buton: Fotoğraf Çek (Hızlı)
        btn_photo = tk.Button(scrollable_frame, text="📸 FOTOĞRAF ÇEK (HIZLI)", 
                             command=self.take_photo_quick, **media_btn_style)
        btn_photo.pack(fill="x", padx=15, pady=2)
        
        # 3. Buton: Fotoğraf Çek (Geri Sayımlı)
        btn_photo_countdown = tk.Button(scrollable_frame, text="⏱️ FOTOĞRAF ÇEK (GERİ SAYIM)", 
                                       command=self.take_photo_countdown, **media_btn_style)
        btn_photo_countdown.pack(fill="x", padx=15, pady=2)
        
        # 4. Buton: Kamera Kapat
        btn_cam_close = tk.Button(scrollable_frame, text="🔴 KAMERAYI KAPAT", 
                                 command=self.close_camera, **media_btn_style)
        btn_cam_close.pack(fill="x", padx=15, pady=2)
        
        # 5. Buton: Windows Kamera Uygulaması
        btn_cam_app = tk.Button(scrollable_frame, text="📱 WİNDOWS KAMERA UYGULAMASI", 
                               command=self.open_camera_app, **media_btn_style)
        btn_cam_app.pack(fill="x", padx=15, pady=2)
        
        # 6. Buton: Fotoğraf Galerisi
        btn_gallery = tk.Button(scrollable_frame, text="🖼️ FOTOĞRAF GALERİSİ", 
                               command=self.open_gallery, **media_btn_style)
        btn_gallery.pack(fill="x", padx=15, pady=2)
        
        # 7. Buton: Kamera Bilgisi
        btn_cam_info = tk.Button(scrollable_frame, text="ℹ️ KAMERA BİLGİSİ", 
                                command=self.camera_info, **media_btn_style)
        btn_cam_info.pack(fill="x", padx=15, pady=2)
        
        # Ayraç
        tk.Frame(scrollable_frame, bg=BG_DIM, height=1).pack(fill="x", padx=15, pady=10)
        
        # Müzik Kontrol başlığı
        tk.Label(scrollable_frame, text="🎵 MÜZİK KONTROL", bg=BG_DARK, fg=GREEN,
                font=("Consolas", 10, "bold")).pack(anchor="w", padx=15, pady=(0, 10))
        
        # Müzik kontrol butonları - yan yana grid
        music_frame = tk.Frame(scrollable_frame, bg=BG_DARK)
        music_frame.pack(fill="x", padx=15, pady=5)
        
        music_buttons = [
            ("▶️ Başlat", "müzik başlat"),
            ("⏸️ Duraklat", "müzik duraklat"),
            ("⏹️ Durdur", "müzik durdur"),
            ("⏭️ Sonraki", "sonraki şarkı"),
            ("⏮️ Önceki", "önceki şarkı"),
            ("🔄 Baştan", "şarkıyı baştan oynat"),
        ]
        
        for i, (text, cmd) in enumerate(music_buttons):
            row = i // 2
            col = i % 2
            btn = tk.Button(music_frame, text=text, 
                           command=lambda c=cmd: self.assistant._quick_command(c),
                           bg=BG_DIM, fg=TEXT, font=("Consolas", 9),
                           bd=0, padx=10, pady=5, cursor="hand2")
            btn.grid(row=row, column=col, padx=3, pady=3, sticky="ew")
        music_frame.columnconfigure(0, weight=1)
        music_frame.columnconfigure(1, weight=1)
        
        # Ses kontrol
        volume_frame = tk.Frame(scrollable_frame, bg=BG_DARK)
        volume_frame.pack(fill="x", padx=15, pady=5)
        
        tk.Button(volume_frame, text="🔉 Ses Kıs", 
                 command=lambda: self.assistant._quick_command("ses kıs"),
                 bg=BG_DIM, fg=TEXT, font=("Consolas", 9), bd=0, padx=10, pady=5,
                 cursor="hand2").pack(side="left", expand=True, fill="x", padx=(0, 3))
        
        tk.Button(volume_frame, text="🔊 Ses Aç", 
                 command=lambda: self.assistant._quick_command("ses aç"),
                 bg=BG_DIM, fg=TEXT, font=("Consolas", 9), bd=0, padx=10, pady=5,
                 cursor="hand2").pack(side="right", expand=True, fill="x", padx=(3, 0))
        
        # Ayraç
        tk.Frame(scrollable_frame, bg=BG_DIM, height=1).pack(fill="x", padx=15, pady=10)
        
        # Asistan profili
        tk.Label(scrollable_frame, text="🤖 ASİSTAN PROFİLİ", bg=BG_DARK, fg=ACCENT,
                font=("Consolas", 10, "bold")).pack(anchor="w", padx=15, pady=(0, 10))
        
        profile_frame = tk.Frame(scrollable_frame, bg=BG_DARK)
        profile_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        profiles = ["KLASİK", "ARKADAŞÇA", "ALAYCI", "PROFESYONEL", "SAKİN OLMAK"]
        current_profile = self.assistant.assistant_profile.current_profile
        
        for profile in profiles:
            profile_btn = tk.Button(profile_frame, text=profile, 
                                    command=lambda p=profile: self.change_profile(p),
                                    bg=ACCENT_DARK if profile == current_profile else BG_CARD,
                                    fg="white" if profile == current_profile else TEXT_DIM,
                                    font=("Consolas", 8), bd=0, padx=8, pady=4,
                                    cursor="hand2")
            profile_btn.pack(side="left", padx=2)
        
        # Bağlantılar
        tk.Frame(scrollable_frame, bg=BG_DIM, height=1).pack(fill="x", padx=15, pady=10)
        
        tk.Label(scrollable_frame, text="🔗 BAĞLANTILAR", bg=BG_DARK, fg=ACCENT,
                font=("Consolas", 10, "bold")).pack(anchor="w", padx=15, pady=(0, 10))
        
        link_items = [
            ("🌐 GitHub", "https://github.com/kudukomuzikyapim1"),
            ("📘 Dokümantasyon", "https://docs.python.org"),
            ("🤖 Asistan Al", "https://kudukomuzikyapimasistanal.42web.io")
        ]
        
        for text, url in link_items:
            link_btn = tk.Button(scrollable_frame, text=text, 
                                 command=lambda u=url: webbrowser.open(u),
                                 bg=BG_CARD, fg=PURPLE, font=("Consolas", 9),
                                 bd=0, padx=12, pady=6, cursor="hand2", anchor="w")
            link_btn.pack(fill="x", padx=15, pady=2)
        
        # Versiyon bilgisi
        tk.Label(scrollable_frame, text="KUDUKO MUZİK YAPİM ASİSTAN AL | © 2026", 
                bg=BG_DARK, fg=TEXT_DIM, font=("Consolas", 8)).pack(pady=(15, 10))
        
        # Pencere kapanınca event binding'leri temizle
        def on_close():
            canvas.unbind_all("<MouseWheel>")
            self.window.destroy()
            self.window = None
            
        self.window.protocol("WM_DELETE_WINDOW", on_close)
    
    # ═══════════════════════════════════════════════════════════════════
    # KAMERA KONTROL METODLARI (DÜZELTİLMİŞ VERSİYON KULLANILIYOR)
    # ═══════════════════════════════════════════════════════════════════
    
    def open_camera_preview(self):
        """Kamerayı açar ve önizleme başlatır"""
        success, msg = self.assistant.camera_controller.start_preview()
        if success:
            messagebox.showinfo("Kamera", "✅ Kamera açıldı!\n\nARTIK FOTOĞRAF ÇEKEBİLİRSİNİZ!\n\nMenüden 'Fotoğraf Çek' butonuna basın veya\n'fotoğraf çek' komutunu söyleyin.")
        else:
            messagebox.showerror("Kamera Hatası", f"❌ Kamera açılamadı!\n\n{msg}\n\n💡 İpuçları:\n• Kameranın bağlı olduğundan emin olun\n• OpenCV kurulu mu? (pip install opencv-python)\n• Başka bir uygulama kamerayı kullanıyor olabilir")
    
    def take_photo_quick(self):
        """Hızlı fotoğraf çeker"""
        success, msg, path = self.assistant.camera_controller.take_photo()
        if success:
            messagebox.showinfo("Fotoğraf Çekildi!", f"✅ {msg}\n\n📁 Kayıt yeri: {path}")
        else:
            messagebox.showerror("Fotoğraf Çekilemedi", f"❌ {msg}\n\n💡 Önce 'KAMERA AÇ' butonuna basmayı deneyin.")
    
    def take_photo_countdown(self):
        """Geri sayımlı fotoğraf çeker"""
        success, msg, path = self.assistant.camera_controller.take_photo_with_preview(self.window)
        if success:
            messagebox.showinfo("Fotoğraf Çekildi!", f"✅ {msg}\n\n📁 Kayıt yeri: {path}")
        else:
            messagebox.showerror("Fotoğraf Çekilemedi", f"❌ {msg}")
    
    def close_camera(self):
        """Kamerayı kapatır"""
        self.assistant.camera_controller.stop_preview()
        messagebox.showinfo("Kamera", "🔴 Kamera kapatıldı!")
    
    def open_camera_app(self):
        """Windows Kamera uygulamasını açar"""
        success, msg = self.assistant.camera_controller.open_camera_app()
        if success:
            messagebox.showinfo("Windows Kamera", msg)
        else:
            messagebox.showerror("Hata", msg)
    
    def open_gallery(self):
        """Fotoğraf galerisini açar"""
        gallery = PhotoGalleryWindow(self.window, self.assistant.camera_controller)
    
    def camera_info(self):
        """Kamera bilgilerini gösterir"""
        status = self.assistant.camera_controller.check_camera_status()
        info_text = f"""📷 KAMERA BİLGİLERİ

✅ Kamera Bulundu: {'Evet' if status['available'] else 'Hayır'}
📸 Kamera Sayısı: {status['count']}
🖼️ Çekilen Fotoğraf: {status['photos_count']}
📁 Fotoğraf Klasörü: {status['photos_dir']}
🔌 Kamera Aktif mi: {'Evet' if self.assistant.camera_controller.is_open else 'Hayır'}

💡 Komutlar:
• 'kamera aç' - Önizleme başlat
• 'kamera kapat' - Kamerayı kapat
• 'fotoğraf çek' - Fotoğraf çek
• 'galeri' - Fotoğrafları görüntüle"""
        
        if 'error' in status:
            info_text += f"\n\n⚠️ HATA: {status['error']}"
        
        messagebox.showinfo("Kamera Bilgileri", info_text)
    
    # ═══════════════════════════════════════════════════════════════════
    # DİĞER MENÜ METODLARI
    # ═══════════════════════════════════════════════════════════════════
    
    def voice_command(self):
        """Sesli komut penceresi"""
        if STT_AVAILABLE:
            self.close()
            messagebox.showinfo("Sesli Komut", "🎤 Ses tanıma hazır.\n\nKomutunuzu söyleyin...")
        else:
            messagebox.showerror("Hata", "SpeechRecognition kütüphanesi yüklü değil!\n\npip install SpeechRecognition")
    
    def clear_chat(self):
        """Sohbeti temizle"""
        if messagebox.askyesno("Onay", "Tüm sohbet geçmişi silinecek. Devam etmek istiyor musunuz?"):
            self.assistant.conv_text.config(state="normal")
            self.assistant.conv_text.delete(1.0, tk.END)
            self.assistant.conv_text.config(state="disabled")
            self.assistant._add_message("SYSTEM", "Sohbet geçmişi temizlendi.")
    
    def copy_chat(self):
        """Sohbeti panoya kopyala"""
        self.assistant.conv_text.config(state="normal")
        chat_text = self.assistant.conv_text.get(1.0, tk.END)
        self.assistant.conv_text.config(state="disabled")
        
        self.parent.clipboard_clear()
        self.parent.clipboard_append(chat_text)
        messagebox.showinfo("Başarılı", "Sohbet panoya kopyalandı!")
    
    def save_chat(self):
        """Sohbeti dosyaya kaydet"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        if filename:
            self.assistant.conv_text.config(state="normal")
            chat_text = self.assistant.conv_text.get(1.0, tk.END)
            self.assistant.conv_text.config(state="disabled")
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(chat_text)
            messagebox.showinfo("Başarılı", f"Sohbet kaydedildi:\n{filename}")
    
    def change_theme(self):
        """Tema değiştir"""
        colors = [
            ("Mavi (Varsayılan)", "#0a0e1a", "#00cfff"),
            ("Koyu Yeşil", "#0a1a0e", "#00ff88"),
            ("Mor", "#1a0a1a", "#aa66ff"),
            ("Turuncu", "#1a100a", "#ff8800"),
            ("Kırmızı", "#1a0a0a", "#ff4466")
        ]
        
        theme_window = tk.Toplevel(self.window)
        theme_window.title("Tema Seç")
        theme_window.geometry("250x250")
        theme_window.configure(bg=BG_DARK)
        theme_window.transient(self.window)
        theme_window.grab_set()
        
        tk.Label(theme_window, text="🎨 Tema Seçin", bg=BG_DARK, fg=ACCENT,
                font=("Consolas", 12, "bold")).pack(pady=10)
        
        for name, bg, accent in colors:
            btn = tk.Button(theme_window, text=name, bg=bg, fg=accent,
                           font=("Consolas", 10), bd=1, relief="solid",
                           command=lambda b=bg, a=accent: self.apply_theme(b, a, theme_window))
            btn.pack(fill="x", padx=20, pady=3)
    
    def apply_theme(self, bg_color, accent_color, window):
        """Temayı uygula"""
        self.parent.configure(bg=bg_color)
        window.destroy()
        messagebox.showinfo("Tema", f"Tema değiştirildi!\nArkaplan: {bg_color}\nVurgu: {accent_color}")
    
    def voice_settings(self):
        """Ses ayarları"""
        if TTS_AVAILABLE:
            settings_window = tk.Toplevel(self.window)
            settings_window.title("Ses Ayarları")
            settings_window.geometry("300x200")
            settings_window.configure(bg=BG_DARK)
            settings_window.transient(self.window)
            
            tk.Label(settings_window, text="🔊 Ses Hızı", bg=BG_DARK, fg=TEXT,
                    font=("Consolas", 10)).pack(pady=10)
            
            speed_var = tk.IntVar(value=160)
            speed_scale = tk.Scale(settings_window, from_=100, to=250, orient="horizontal",
                                   variable=speed_var, bg=BG_DARK, fg=TEXT,
                                   highlightthickness=0)
            speed_scale.pack(padx=20, fill="x")
            
            def apply_speed():
                self.assistant.tts.engine.setProperty("rate", speed_var.get())
                messagebox.showinfo("Ayarlar", f"Ses hızı {speed_var.get()} olarak ayarlandı")
                settings_window.destroy()
            
            tk.Button(settings_window, text="Uygula", command=apply_speed,
                     bg=ACCENT_DARK, fg="white", font=("Consolas", 10),
                     bd=0, padx=20, pady=8, cursor="hand2").pack(pady=20)
        else:
            messagebox.showerror("Hata", "TTS kütüphanesi yüklü değil!")
    
    def system_info(self):
        """Sistem bilgilerini göster"""
        info = f"""📊 SİSTEM BİLGİLERİ

💻 İşletim Sistemi: {sys.platform}
🐍 Python: {sys.version.split()[0]}
🎤 STT: {'✓ Aktif' if STT_AVAILABLE else '✗ Devre Dışı'}
🔊 TTS: {'✓ Aktif' if TTS_AVAILABLE else '✗ Devre Dışı'}
📷 Kamera: {'✓ Aktif' if CAMERA_AVAILABLE else '✗ Devre Dışı'}
💾 Hafıza: {self.assistant.memory.call_count} kayıt
🎭 Profil: {self.assistant.assistant_profile.current_profile}
🔌 Kamera Aktif: {'Evet' if self.assistant.camera_controller.is_open else 'Hayır'}
"""
        messagebox.showinfo("Sistem Bilgileri", info)
    
    def refresh_all(self):
        """Tüm sistemi yenile"""
        self.assistant._update_system_stats()
        self.assistant._update_weather()
        self.assistant.mem_label.config(text=f"💾 HAFIZA: {self.assistant.memory.call_count}")
        messagebox.showinfo("Yenileme", "Sistem bilgileri yenilendi!")
    
    def about(self):
        """Hakkında penceresi"""
        about_text = """KUDUKO MUZİK YAPİM ASİSTAN AL

🚀 Sürüm 2.0
🤖 Gelişmiş Yapay Zeka Asistanı
🎵 Müzik Kontrolü (Windows Medya Tuşları)
📷 Kamera Desteği (OpenCV ile fotoğraf çekimi)
🌐 Web Entegrasyonu
💾 Hafıza Sistemi
🎭 5 Farklı Asistan Profili

📸 KAMERA ÖZELLİKLERİ:
• Windows Kamera Uygulaması desteği
• Hızlı ve geri sayımlı fotoğraf çekimi
• Fotoğraf galerisi
• Otomatik fotoğraf klasörü oluşturma

KUDUKO MUZİK YAPİM ASİSTAN AL | © 2026"""
        messagebox.showinfo("Hakkında", about_text)
    
    def change_profile(self, profile_name):
        """Asistan profilini değiştir"""
        success, name = self.assistant.assistant_profile.set_profile(profile_name)
        if success:
            messagebox.showinfo("Profil", f"Asistan profili '{name}' olarak değiştirildi!")
            self.close()
            self.show()
    
    def exit_app(self):
        """Uygulamadan çık"""
        if messagebox.askyesno("Çıkış", "KUDUKO MUZİK YAPİM ASİSTAN AL kapatılsın mı?"):
            self.assistant.camera_controller.stop_preview()
            self.parent.quit()
            self.parent.destroy()
    
    def close(self):
        """Menü penceresini kapat"""
        if self.window:
            self.window.destroy()
            self.window = None

# ═══════════════════════════════════════════════════════════════════
# ASİSTAN PROFİLİ
# ═══════════════════════════════════════════════════════════════════

class AssistantProfile:
    PROFILES = {
        "KLASİK": {"name": "KLASİK", "emoji": "🎩", "style": "resmi", "voice_rate": 160, 
                   "greeting": "Hazırım, efendim. Nasıl yardımcı olabilirim?"},
        "ARKADAŞÇA": {"name": "ARKADAŞÇA", "emoji": "😊", "style": "samimi", "voice_rate": 170,
                    "greeting": "Hey! Bugün sana nasıl yardımcı olabilirim? ✨"},
        "ALAYCI": {"name": "ALAYCI", "emoji": "😏", "style": "alaycı", "voice_rate": 155,
                     "greeting": "Yine mi? Pekala, ne istiyorsun? 😄"},
        "PROFESYONEL": {"name": "PROFESYONEL", "emoji": "💼", "style": "iş", "voice_rate": 150,
                        "greeting": "Sistemler hazır. Emirlerinizi bekliyorum."},
        "SAKİN OLMAK": {"name": "SAKİN OLMAK", "emoji": "🎮", "style": "rahat", "voice_rate": 175,
                 "greeting": "N'aber? Hazırım, buyur! 🚀"}
    }
    
    def __init__(self):
        self.current_profile = "CLASSIC"
        self.load()
    
    def load(self):
        try:
            if os.path.exists("assistant_profile.json"):
                with open("assistant_profile.json", "r") as f:
                    data = json.load(f)
                    self.current_profile = data.get("profile", "CLASSIC")
        except: pass
    
    def save(self):
        try:
            with open("assistant_profile.json", "w") as f:
                json.dump({"profile": self.current_profile}, f)
        except: pass
    
    def get_profile(self):
        return self.PROFILES.get(self.current_profile, self.PROFILES["CLASSIC"])
    
    def set_profile(self, name):
        if name.upper() in self.PROFILES:
            self.current_profile = name.upper()
            self.save()
            return True, self.PROFILES[name.upper()]["name"]
        return False, ""
    
    def modify_response(self, response, module):
        profile = self.get_profile()
        if profile["style"] == "resmi":
            if random.random() < 0.3 and not response.endswith("efendim"):
                response = response.replace("?", ", efendim?")
        elif profile["style"] == "samimi":
            if random.random() < 0.4:
                response += random.choice([" ^^", " :)", " ✨"])
        elif profile["style"] == "alaycı":
            if random.random() < 0.3:
                response += random.choice([" (Tabii ki ^^)", " (!)"])
        return response

# ═══════════════════════════════════════════════════════════════════
# HAFIZA SİSTEMİ
# ═══════════════════════════════════════════════════════════════════

class Memory:
    def __init__(self):
        self.history = []
        self.learned = {}
        self.call_count = 0
        self.load()
    
    def add(self, role, text):
        self.history.append((role, text, str(datetime.datetime.now())))
        if len(self.history) > 200:
            self.history = self.history[-200:]
        if role == "user":
            self.call_count += 1
        self.save()
    
    def learn(self, key, val):
        self.learned[key] = val
        self.save()
    
    def save(self):
        try:
            with open("assistant_memory.json", "w", encoding="utf-8") as f:
                json.dump({"history": self.history[-50:], "learned": self.learned, "calls": self.call_count}, f, ensure_ascii=False, indent=2)
        except: pass
    
    def load(self):
        try:
            if os.path.exists("assistant_memory.json"):
                with open("assistant_memory.json", "r", encoding="utf-8") as f:
                    d = json.load(f)
                    self.history = d.get("history", [])
                    self.learned = d.get("learned", {})
                    self.call_count = d.get("calls", 0)
        except: pass

# ═══════════════════════════════════════════════════════════════════
# MEDYA KONTROL
# ═══════════════════════════════════════════════════════════════════

class MediaController:
    @staticmethod
    def play_pause():
        try:
            import ctypes
            ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xB3, 0, 2, 0)
            return True, "⏯️ Müzik durduruldu/başlatıldı"
        except: 
            return False, "Medya kontrolü yapılamadı"
    
    @staticmethod
    def start_music():
        try:
            import ctypes
            ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xB3, 0, 2, 0)
            return True, "▶️ Müzik başlatıldı"
        except: 
            return False, "Müzik başlatılamadı"
    
    @staticmethod
    def pause_music():
        try:
            import ctypes
            ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xB3, 0, 2, 0)
            return True, "⏸️ Müzik duraklatıldı"
        except: 
            return False, "Müzik duraklatılamadı"
    
    @staticmethod
    def stop_music():
        try:
            import ctypes
            ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xB3, 0, 2, 0)
            return True, "⏹️ Müzik durduruldu"
        except: 
            return False, "Müzik durdurulamadı"
    
    @staticmethod
    def next_track():
        try:
            import ctypes
            ctypes.windll.user32.keybd_event(0xB0, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xB0, 0, 2, 0)
            return True, "⏭️ Sonraki şarkı"
        except: 
            return False, "Sonraki şarkıya geçilemedi"
    
    @staticmethod
    def previous_track():
        try:
            import ctypes
            ctypes.windll.user32.keybd_event(0xB1, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xB1, 0, 2, 0)
            return True, "⏮️ Önceki şarkı"
        except: 
            return False, "Önceki şarkıya geçilemedi"
    
    @staticmethod
    def volume_up():
        try:
            import ctypes
            ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xAF, 0, 2, 0)
            return True, "🔊 Ses açıldı"
        except: 
            return False, "Ses açılamadı"
    
    @staticmethod
    def volume_down():
        try:
            import ctypes
            ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xAE, 0, 2, 0)
            return True, "🔉 Ses kısıldı"
        except: 
            return False, "Ses kısılamadı"
    
    @staticmethod
    def seek_forward(seconds=10):
        return True, f"⏩ {seconds} saniye ileri sarma (oynatıcı desteği gerekli)"
    
    @staticmethod
    def seek_backward(seconds=10):
        return True, f"⏪ {seconds} saniye geri sarma (oynatıcı desteği gerekli)"
    
    @staticmethod
    def restart_track():
        return True, "🔁 Şarkı başa sarıldı"

# ═══════════════════════════════════════════════════════════════════
# Wİ-Fİ VE BLUETOOTH KONTROL
# ═══════════════════════════════════════════════════════════════════

class NetworkController:
    @staticmethod
    def wifi_off():
        try:
            subprocess.run('netsh interface set interface "Wi-Fi" admin=disable', 
                          shell=True, capture_output=True, text=True)
            return True, "📡 Wi-Fi kapatıldı."
        except Exception as e:
            try:
                subprocess.run('netsh interface set interface "WLAN" admin=disable', 
                              shell=True, capture_output=True, text=True)
                return True, "📡 Wi-Fi kapatıldı."
            except:
                return False, f"Wi-Fi kapatılamadı: {str(e)}"
    
    @staticmethod
    def wifi_on():
        try:
            subprocess.run('netsh interface set interface "Wi-Fi" admin=enable', 
                          shell=True, capture_output=True, text=True)
            return True, "📡 Wi-Fi açıldı."
        except Exception as e:
            try:
                subprocess.run('netsh interface set interface "WLAN" admin=enable', 
                              shell=True, capture_output=True, text=True)
                return True, "📡 Wi-Fi açıldı."
            except:
                return False, f"Wi-Fi açılamadı: {str(e)}"
    
    @staticmethod
    def bluetooth_off():
        try:
            ps_command = '''
            $adapter = Get-PnpDevice -Class Bluetooth | Where-Object {$_.FriendlyName -like "*Bluetooth*" -and $_.Status -eq "OK"}
            if ($adapter) {
                Disable-PnpDevice -InstanceId $adapter.InstanceId -Confirm:$false
                Write-Output "Bluetooth kapatıldı"
            } else {
                Write-Output "Bluetooth adaptörü bulunamadı veya zaten kapalı"
            }
            '''
            result = subprocess.run(['powershell', '-Command', ps_command], 
                                   capture_output=True, text=True)
            return True, "🔷 Bluetooth kapatıldı."
        except Exception as e:
            return False, f"Bluetooth kapatılamadı: {str(e)}"
    
    @staticmethod
    def bluetooth_on():
        try:
            ps_command = '''
            $adapter = Get-PnpDevice -Class Bluetooth | Where-Object {$_.FriendlyName -like "*Bluetooth*" -and $_.Status -eq "Error"}
            if ($adapter) {
                Enable-PnpDevice -InstanceId $adapter.InstanceId -Confirm:$false
                Write-Output "Bluetooth açıldı"
            } else {
                $activeAdapter = Get-PnpDevice -Class Bluetooth | Where-Object {$_.FriendlyName -like "*Bluetooth*" -and $_.Status -eq "OK"}
                if ($activeAdapter) {
                    Write-Output "Bluetooth zaten açık"
                } else {
                    Write-Output "Bluetooth adaptörü bulunamadı"
                }
            }
            '''
            result = subprocess.run(['powershell', '-Command', ps_command], 
                                   capture_output=True, text=True)
            return True, "🔷 Bluetooth açıldı."
        except Exception as e:
            return False, f"Bluetooth açılamadı: {str(e)}"
    
    @staticmethod
    def get_wifi_status():
        try:
            result = subprocess.run('netsh interface show interface "Wi-Fi"', 
                                   shell=True, capture_output=True, text=True)
            if "Enabled" in result.stdout or "Connected" in result.stdout:
                return "Açık"
            elif "Disabled" in result.stdout:
                return "Kapalı"
            result2 = subprocess.run('netsh interface show interface "WLAN"', 
                                    shell=True, capture_output=True, text=True)
            if "Enabled" in result2.stdout or "Connected" in result2.stdout:
                return "Açık"
            elif "Disabled" in result2.stdout:
                return "Kapalı"
            return "Bilinmiyor"
        except:
            return "Bilinmiyor"
    
    @staticmethod
    def get_bluetooth_status():
        try:
            ps_command = '''
            $adapter = Get-PnpDevice -Class Bluetooth | Where-Object {$_.FriendlyName -like "*Bluetooth*"}
            if ($adapter.Status -eq "OK") { Write-Output "Açık" } 
            elseif ($adapter.Status -eq "Error") { Write-Output "Kapalı" }
            else { Write-Output "Bilinmiyor" }
            '''
            result = subprocess.run(['powershell', '-Command', ps_command], 
                                   capture_output=True, text=True)
            status = result.stdout.strip()
            return status if status else "Bilinmiyor"
        except:
            return "Bilinmiyor"

# ═══════════════════════════════════════════════════════════════════
# WINDOWS KONTROL
# ═══════════════════════════════════════════════════════════════════

class WindowsController:
    @staticmethod
    def list_all_installed_apps():
        apps = set()
        
        try:
            start_menu_paths = [
                os.path.expandvars(r"%ProgramData%\Microsoft\Windows\Start Menu\Programs"),
                os.path.expandvars(r"%AppData%\Microsoft\Windows\Start Menu\Programs"),
                os.path.expandvars(r"%AllUsersProfile%\Microsoft\Windows\Start Menu\Programs")
            ]
            
            for path in start_menu_paths:
                if os.path.exists(path):
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            if file.endswith((".lnk", ".exe")):
                                app_name = os.path.splitext(file)[0]
                                if app_name and len(app_name) > 1:
                                    apps.add(app_name)
            
            try:
                import winreg
                reg_paths = [
                    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                    r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
                ]
                
                for reg_path in reg_paths:
                    try:
                        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ)
                        i = 0
                        while True:
                            try:
                                subkey_name = winreg.EnumKey(key, i)
                                subkey = winreg.OpenKey(key, subkey_name)
                                try:
                                    display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                    if display_name and len(display_name) > 1:
                                        apps.add(display_name)
                                except:
                                    pass
                                winreg.CloseKey(subkey)
                                i += 1
                            except WindowsError:
                                break
                        winreg.CloseKey(key)
                    except:
                        pass
            except ImportError:
                pass
            
            program_files_paths = [
                os.environ.get("ProgramFiles", "C:\\Program Files"),
                os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
            ]
            
            for pf_path in program_files_paths:
                if pf_path and os.path.exists(pf_path):
                    try:
                        for folder in os.listdir(pf_path):
                            folder_path = os.path.join(pf_path, folder)
                            if os.path.isdir(folder_path):
                                for file in os.listdir(folder_path):
                                    if file.endswith(".exe") and not file.startswith("unins"):
                                        app_name = os.path.splitext(file)[0]
                                        if app_name and len(app_name) > 2:
                                            apps.add(app_name)
                                        break
                    except:
                        pass
            
        except Exception as e:
            print(f"Uygulama listeleme hatası: {e}")
        
        return sorted(list(apps))
    
    @staticmethod
    def open_app_smart(app_name):
        app_name_lower = app_name.lower().strip()
        
        quick_map = {
            "notepad": "notepad.exe", "hesap makinesi": "calc.exe", "calculator": "calc.exe",
            "cmd": "cmd.exe", "komut": "cmd.exe", "komut istemi": "cmd.exe",
            "chrome": "chrome.exe", "google chrome": "chrome.exe", "firefox": "firefox.exe",
            "edge": "msedge.exe", "microsoft edge": "msedge.exe",
            "spotify": "Spotify.exe", "paint": "mspaint.exe",
            "word": "WINWORD.EXE", "excel": "EXCEL.EXE", "powerpoint": "POWERPNT.EXE",
            "outlook": "OUTLOOK.EXE", "whatsapp": "WhatsApp.exe",
            "telegram": "Telegram.exe", "discord": "Discord.exe",
            "slack": "slack.exe", "zoom": "Zoom.exe", "teams": "Teams.exe",
            "visual studio code": "Code.exe", "vscode": "Code.exe",
            "pycharm": "pycharm64.exe", "intellij": "idea64.exe",
            "photoshop": "Photoshop.exe", "illustrator": "Illustrator.exe",
            "premiere": "Premiere Pro.exe", "steam": "steam.exe",
            "epic games": "EpicGamesLauncher.exe", "netflix": "netflix.exe",
            "vlc": "vlc.exe", "snipping tool": "SnippingTool.exe",
            "ekran alıntısı": "SnippingTool.exe", "task manager": "taskmgr.exe",
            "görev yöneticisi": "taskmgr.exe", "control panel": "control.exe",
            "denetim masası": "control.exe", "device manager": "devmgmt.msc",
            "aygıt yöneticisi": "devmgmt.msc"
        }
        
        if app_name_lower in quick_map:
            target = quick_map[app_name_lower]
            try:
                subprocess.Popen(target, shell=True)
                return True, f"✅ {app_name} başlatıldı."
            except Exception as e:
                print(f"Hızlı eşleme hatası: {e}")
        
        try:
            subprocess.Popen(f'start "" "{app_name}"', shell=True)
            return True, f"✅ {app_name} başlatılmaya çalışılıyor."
        except Exception as e:
            print(f"Start komutu hatası: {e}")
        
        try:
            subprocess.Popen(f'start "" "{app_name}.exe"', shell=True)
            return True, f"✅ {app_name}.exe başlatılıyor."
        except:
            pass
        
        try:
            result = subprocess.run(f'where "{app_name}.exe"', shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                exe_path = result.stdout.strip().split('\n')[0]
                subprocess.Popen(f'start "" "{exe_path}"', shell=True)
                return True, f"✅ {app_name} bulundu ve başlatıldı."
        except:
            pass
        
        program_files_paths = [
            os.environ.get("ProgramFiles", "C:\\Program Files"),
            os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
        ]
        
        for pf_path in program_files_paths:
            if pf_path and os.path.exists(pf_path):
                try:
                    for folder in os.listdir(pf_path):
                        if app_name_lower in folder.lower():
                            folder_path = os.path.join(pf_path, folder)
                            if os.path.isdir(folder_path):
                                for file in os.listdir(folder_path):
                                    if file.lower().endswith('.exe') and not file.lower().startswith('unins'):
                                        full_path = os.path.join(folder_path, file)
                                        subprocess.Popen(f'start "" "{full_path}"', shell=True)
                                        return True, f"✅ {app_name} Program Files'dan başlatıldı."
                except:
                    pass
        
        desktop_paths = [
            os.path.expandvars(r"%USERPROFILE%\Desktop"),
            os.path.expandvars(r"%PUBLIC%\Desktop")
        ]
        
        for desktop in desktop_paths:
            if os.path.exists(desktop):
                try:
                    for file in os.listdir(desktop):
                        if file.lower().endswith('.lnk') and app_name_lower in file.lower():
                            shortcut_path = os.path.join(desktop, file)
                            subprocess.Popen(f'start "" "{shortcut_path}"', shell=True)
                            return True, f"✅ {app_name} masaüstünden başlatıldı."
                except:
                    pass
        
        return False, f"❌ '{app_name}' açılamadı. Lütfen doğru yazdığınızdan emin olun."
    
    @staticmethod
    def open_app(app_name):
        return WindowsController.open_app_smart(app_name)
    
    @staticmethod
    def music_control(command):
        cmd = command.lower()
        if any(x in cmd for x in ["durdur", "stop"]):
            return MediaController.stop_music()
        elif any(x in cmd for x in ["devam", "resume", "başlat", "baslat", "oynat", "play"]):
            return MediaController.start_music()
        elif any(x in cmd for x in ["duraklat", "pause"]):
            return MediaController.pause_music()
        elif any(x in cmd for x in ["sonraki", "next"]):
            return MediaController.next_track()
        elif any(x in cmd for x in ["önceki", "previous"]):
            return MediaController.previous_track()
        elif "ses aç" in cmd:
            return MediaController.volume_up()
        elif "ses kıs" in cmd:
            return MediaController.volume_down()
        elif "baştan" in cmd or "başa sar" in cmd:
            return MediaController.restart_track()
        elif "10 saniye ileri" in cmd or "10sn ileri" in cmd:
            return MediaController.seek_forward(10)
        elif "10 saniye geri" in cmd or "10sn geri" in cmd:
            return MediaController.seek_backward(10)
        return False, "Müzik komutu anlaşılamadı."
    
    @staticmethod
    def open_gallery():
        try:
            subprocess.Popen("explorer.exe", shell=True)
            return True, "Galeri/Gezgin açılıyor."
        except:
            return False, "Galeri açılamadı."

# ═══════════════════════════════════════════════════════════════════
# WHATSAPP KONTROL
# ═══════════════════════════════════════════════════════════════════

class WhatsAppController:
    def __init__(self):
        self.contacts = []
        self.load()
    
    def load(self):
        try:
            if os.path.exists("whatsapp_contacts.json"):
                with open("whatsapp_contacts.json", "r") as f:
                    data = json.load(f)
                    self.contacts = data.get("contacts", [])
        except: pass
    
    def save(self):
        try:
            with open("whatsapp_contacts.json", "w") as f:
                json.dump({"contacts": self.contacts}, f, indent=2)
        except: pass
    
    def add_contact(self, name, phone):
        self.contacts.append({"name": name, "phone": phone})
        self.save()
        return True, f"{name} eklendi."
    
    def get_contacts(self):
        return self.contacts
    
    def open_web(self):
        webbrowser.open("https://web.whatsapp.com")
        return True, "WhatsApp Web açılıyor."

# ═══════════════════════════════════════════════════════════════════
# UYGULAMA LİSTELEME AÇILIR PENCERESİ
# ═══════════════════════════════════════════════════════════════════

class AppsListPopup:
    def __init__(self, parent):
        self.parent = parent
        self.window = None
        self.apps = []
        self.search_var = None
        self.listbox = None
        
    def show(self, apps):
        self.apps = apps
        
        self.window = tk.Toplevel(self.parent)
        self.window.title("KUDUKO - Tüm Uygulamalar")
        self.window.configure(bg=BG_DARK)
        self.window.geometry("650x750")
        self.window.minsize(500, 400)
        
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - 325
        y = (self.window.winfo_screenheight() // 2) - 375
        self.window.geometry(f"+{x}+{y}")
        
        title_frame = tk.Frame(self.window, bg=BG_DIM)
        title_frame.pack(fill="x")
        
        tk.Label(title_frame, text="📦 YÜKLÜ UYGULAMALAR", 
                bg=BG_DIM, fg=ACCENT, font=("Consolas", 16, "bold")).pack(side="left", padx=15, pady=10)
        
        count_label = tk.Label(title_frame, text=f"Toplam: {len(apps)}", 
                               bg=BG_DIM, fg=TEXT_DIM, font=("Consolas", 10))
        count_label.pack(side="right", padx=15)
        
        close_btn = tk.Button(title_frame, text="✕", command=self.close,
                              bg=BG_DIM, fg=WARN, font=("Consolas", 12, "bold"),
                              bd=0, padx=8, pady=4, cursor="hand2")
        close_btn.pack(side="right", padx=5)
        
        search_frame = tk.Frame(self.window, bg=BG_CARD)
        search_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        tk.Label(search_frame, text="🔍 ARA:", bg=BG_CARD, fg=TEXT, 
                font=("Consolas", 10, "bold")).pack(side="left", padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.filter_apps())
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, 
                                bg=BG_DIM, fg=TEXT, font=("Consolas", 11),
                                insertbackground=ACCENT, bd=0, relief="flat")
        search_entry.pack(side="left", fill="x", expand=True, ipady=8)
        
        info_btn = tk.Button(search_frame, text="ℹ️", command=self.show_help,
                             bg=BG_CARD, fg=ACCENT, font=("Consolas", 10),
                             bd=0, cursor="hand2")
        info_btn.pack(side="right", padx=(10, 0))
        
        list_frame = tk.Frame(self.window, bg=BG_DIM)
        list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        scrollbar = tk.Scrollbar(list_frame, bg=BG_DIM)
        scrollbar.pack(side="right", fill="y")
        
        self.listbox = tk.Listbox(list_frame, bg=BG_DIM, fg=TEXT, 
                                   font=("Consolas", 10), selectbackground=ACCENT_DARK,
                                   selectforeground="white", bd=0, highlightthickness=0,
                                   yscrollcommand=scrollbar.set)
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        self.listbox.bind("<Double-Button-1>", self.on_app_double_click)
        
        bottom_frame = tk.Frame(self.window, bg=BG_CARD)
        bottom_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        open_btn = tk.Button(bottom_frame, text="🚀 SEÇİLİ UYGULAMAYI AÇ", 
                             command=self.open_selected_app,
                             bg=ACCENT_DARK, fg=TEXT, font=("Consolas", 10, "bold"),
                             bd=0, padx=20, pady=8, cursor="hand2")
        open_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        refresh_btn = tk.Button(bottom_frame, text="🔄 YENİLE", 
                                command=self.refresh_apps,
                                bg=BG_DIM, fg=TEXT, font=("Consolas", 10),
                                bd=0, padx=15, pady=8, cursor="hand2")
        refresh_btn.pack(side="right")
        
        self.populate_list(apps)
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.window.bind("<Escape>", lambda e: self.close())
    
    def populate_list(self, apps):
        self.listbox.delete(0, tk.END)
        for app in apps:
            self.listbox.insert(tk.END, f"📱 {app}")
    
    def filter_apps(self):
        search_term = self.search_var.get().lower()
        if not search_term:
            self.populate_list(self.apps)
        else:
            filtered = [app for app in self.apps if search_term in app.lower()]
            self.populate_list(filtered)
    
    def on_app_double_click(self, event):
        selection = self.listbox.curselection()
        if selection:
            app_name = self.listbox.get(selection[0]).replace("📱 ", "")
            self.open_app(app_name)
    
    def open_selected_app(self):
        selection = self.listbox.curselection()
        if selection:
            app_name = self.listbox.get(selection[0]).replace("📱 ", "")
            self.open_app(app_name)
        else:
            messagebox.showinfo("Bilgi", "Lütfen bir uygulama seçin!")
    
    def open_app(self, app_name):
        clean_name = app_name.replace("📱 ", "").strip()
        success, msg = WindowsController.open_app_smart(clean_name)
        
        if success:
            messagebox.showinfo("✅ Başarılı", msg)
            self.close()
        else:
            answer = messagebox.askyesno(
                "⚠️ Uygulama Açılamadı", 
                f"{msg}\n\nManuel olarak aramak ister misiniz?\n(Program Files klasörünü açar)"
            )
            if answer:
                subprocess.Popen('explorer "C:\\Program Files"', shell=True)
    
    def refresh_apps(self):
        self.window.config(cursor="watch")
        self.window.update()
        
        def scan():
            new_apps = WindowsController.list_all_installed_apps()
            self.window.after(0, lambda: self.update_apps(new_apps))
        
        threading.Thread(target=scan, daemon=True).start()
    
    def update_apps(self, new_apps):
        self.apps = new_apps
        self.populate_list(self.apps)
        self.window.config(cursor="")
        messagebox.showinfo("Yenilendi", f"Toplam {len(new_apps)} uygulama bulundu!")
    
    def show_help(self):
        help_text = """🔍 Uygulama Listesi Yardım

• Uygulamaları aramak için arama kutusunu kullanın
• Bir uygulamayı açmak için çift tıklayın veya seçip "AÇ" butonuna basın
• "YENİLE" butonu ile uygulama listesini güncelleyin
• Uygulama isimleri Başlat Menüsü, Registry ve Program Files'dan alınır

💡 İpucu: Asistan'a "tüm uygulamalar" yazarak bu pencereyi açabilirsiniz!"""
        
        messagebox.showinfo("Yardım", help_text)
    
    def close(self):
        if self.window:
            self.window.destroy()
            self.window = None

# ═══════════════════════════════════════════════════════════════════
# ASİSTAN BEYİNİ (YANIT BANKASI)
# ═══════════════════════════════════════════════════════════════════

class AssistantBrain:
    def __init__(self, memory, win_controller, camera_controller, assistant_profile):
        self.memory = memory
        self.win = win_controller
        self.camera = camera_controller
        self.profile = assistant_profile
        self.wa = WhatsAppController()
        self.cached_apps = None
        self.popup = None
        self.parent_window = None
    
    def set_parent_window(self, parent):
        self.parent_window = parent
    
    def respond(self, text):
        t = text.lower()
        
        # SAAT komutu
        if any(x in t for x in ["saat", "zaman"]):
            return f"🕐 Saat {datetime.datetime.now().strftime('%H:%M:%S')}.", "NLP"
        
        # ZIRH komutu
        if any(x in t for x in ["zırh", "zırh durumu", "zirh"]):
            return "🛡️ Zırh hazır. Tüm sistemler nominal. Savunma protokolleri aktif.", "ZIRH"
        
        # TÜM UYGULAMALAR komutu
        if any(x in t for x in ["tüm uygulamalar", "tum uygulamalar", "yüklü uygulamalar", "yuklu uygulamalar"]):
            def get_and_show():
                apps = WindowsController.list_all_installed_apps()
                self.cached_apps = apps
                if apps and self.parent_window:
                    self.popup = AppsListPopup(self.parent_window)
                    self.popup.show(apps)
                    return f"✅ Toplam {len(apps)} uygulama bulundu.", "OTOMASYON"
                else:
                    return "❌ Uygulama listesi alınamadı.", "OTOMASYON"
            
            result = get_and_show()
            return result
        
        # FOTOĞRAF ÇEK komutu (DÜZELTİLMİŞ)
        if any(x in t for x in ["fotoğraf çek", "resim çek", "fotograf cek", "foto cek", "fotograf çek"]):
            success, msg, path = self.camera.take_photo()
            if success and path:
                return f"✅ {msg}\n📁 Kayıt: {path}", "KAMERA"
            else:
                return f"❌ {msg}\n\n💡 İpuçları:\n• Önce 'kamera aç' komutunu verin\n• Kameranın bağlı olduğundan emin olun\n• OpenCV kurulu mu? (pip install opencv-python)\n• Başka bir uygulama kamerayı kullanıyor olabilir", "KAMERA"
        
        # SPOTIFY komutu
        if "spotify" in t and ("aç" in t or "oynat" in t):
            success, msg = self.win.open_app_smart("spotify")
            return msg, "MEDYA"
        
        # YT MUSIC / YouTube Music komutu
        if "youtube music" in t or "yt music" in t or "youtube müzik" in t:
            webbrowser.open("https://music.youtube.com")
            return "🎧 YouTube Music açılıyor.", "WEB"
        
        # WHATSAPP komutu
        if "whatsapp" in t:
            if any(x in t for x in ["aç", "web"]):
                success, msg = self.wa.open_web()
                return msg, "WHATSAPP"
            elif "ekle" in t:
                match = re.search(r'ekle\s+(\w+)\s+(\d+)', t)
                if match:
                    success, msg = self.wa.add_contact(match.group(1), match.group(2))
                    return msg, "WHATSAPP"
            return "WhatsApp komutları: 'whatsapp aç', 'whatsapp ekle Ahmet 5551234567'", "WHATSAPP"
        
        # KAMERA AÇ komutu
        if any(x in t for x in ["kamera aç", "kamerayı aç"]):
            success, msg = self.camera.start_preview()
            if success:
                return "✅ " + msg + "\n\nARTIK FOTOĞRAF ÇEKEBİLİRSİNİZ!\n'fotoğraf çek' komutunu kullanın.", "KAMERA"
            else:
                return "❌ " + msg, "KAMERA"
        
        # KAMERA KAPAT komutu
        if any(x in t for x in ["kamera kapat", "kamerayı kapat"]):
            self.camera.stop_preview()
            return "📷 Kamera kapatıldı.", "KAMERA"
        
        # Wi-Fi komutları
        if any(x in t for x in ["wifi kapat", "wi-fi kapat", "wifi yi kapat"]):
            success, msg = NetworkController.wifi_off()
            return msg, "OTOMASYON"
        
        if any(x in t for x in ["wifi aç", "wi-fi aç", "wifi yi aç"]):
            success, msg = NetworkController.wifi_on()
            return msg, "OTOMASYON"
        
        if "wifi durumu" in t or "wi-fi durumu" in t:
            status = NetworkController.get_wifi_status()
            return f"📡 Wi-Fi durumu: {status}", "OTOMASYON"
        
        # Bluetooth komutları
        if any(x in t for x in ["bluetooth kapat", "bluetooth u kapat", "bt kapat"]):
            success, msg = NetworkController.bluetooth_off()
            return msg, "OTOMASYON"
        
        if any(x in t for x in ["bluetooth aç", "bluetooth u aç", "bt aç"]):
            success, msg = NetworkController.bluetooth_on()
            return msg, "OTOMASYON"
        
        if "bluetooth durumu" in t or "bt durumu" in t:
            status = NetworkController.get_bluetooth_status()
            return f"🔷 Bluetooth durumu: {status}", "OTOMASYON"
        
        # MÜZİK KONTROL komutları
        if any(x in t for x in ["müzik", "şarkı", "oynat", "durdur", "sonraki", "önceki", "ses", "baştan", "ileri", "geri", "duraklat", "başlat", "baslat"]):
            success, msg = self.win.music_control(text)
            return msg, "MEDYA"
        
        # GALERİ komutu
        if any(x in t for x in ["galeri", "galeriyi aç", "fotoğraflar"]):
            if self.parent_window:
                gallery = PhotoGalleryWindow(self.parent_window, self.camera)
                return "📸 Fotoğraf galerisi açılıyor.", "KAMERA"
            else:
                return "Galeri penceresi açılamadı.", "KAMERA"
        
        for key, val in self.memory.learned.items():
            if key in t:
                return val, "ÖĞRENME"
        
        if any(x in t for x in ["merhaba", "selam", "hey", "naber", "hello", "hi"]):
            return random.choice(["Merhaba efendim!", "Selam! Size nasıl yardımcı olabilirim?", "Hoş geldiniz!"]), "NLP"
        
        if any(x in t for x in ["tarih", "bugün", "gün"]):
            return f"📅 Bugün {datetime.datetime.now().strftime('%d %B %Y')}.", "NLP"
        
        if any(x in t for x in ["nasılsın", "durum", "nasıl gidiyor"]):
            return "Tüm sistemler nominal, efendim!", "NLP"
        
        if any(x in t for x in ["bilim", "hesapla", "kuantum"]):
            return "Kuantum hesaplama modülü aktif. İşlem yapılıyor.", "BİLİM"
        
        if any(x in t for x in ["güvenlik", "tehdit", "tarama"]):
            return "Güvenlik taraması başlatıldı. Tehdit yok.", "GÜVENLİK"
        
        if "taktik" in t:
            return "Taktik analiz modülü hazır. Stratejik durum değerlendirmesi yapılıyor.", "TAKTİK"
        
        if any(x in t for x in ["teşekkür", "sağ ol", "sağol"]):
            return "Rica ederim, efendim!", "NLP"
        
        if any(x in t for x in ["güle güle", "görüşürüz", "bay bay"]):
            return "Güle güle, efendim!", "NLP"
        
        return random.choice([
            "Anlıyorum, efendim. Biraz daha açıklar mısınız?",
            "Bu konuda size nasıl yardımcı olabilirim?",
            "İşlem yapılıyor. Lütfen bekleyin.",
            "Komutu anlayamadım. Lütfen tekrar dener misiniz?"
        ]), "NLP"

# ═══════════════════════════════════════════════════════════════════
# TTS MOTORU
# ═══════════════════════════════════════════════════════════════════

class TTSEngine:
    def __init__(self):
        self.engine = None
        if TTS_AVAILABLE:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 160)
            except: pass
    
    def speak(self, text):
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except: pass

# ═══════════════════════════════════════════════════════════════════
# ANA UYGULAMA - KUDUKO MUZİK YAPİM ASİSTAN AL
# ═══════════════════════════════════════════════════════════════════

class CyberAssistantApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KUDUKO MUZİK YAPİM ASİSTAN AL")
        self.root.configure(bg=BG_DARK)
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Animasyon değişkenleri
        self.angle = 0
        self.ring2_angle = 0
        self.pulse = 0
        self.pulse_dir = 1
        self.square_angle = 0
        self.dot_angle = 0
        
        self.cpu_history = [0] * 60
        self.ram_history = [0] * 60
        self.start_time = datetime.datetime.now()
        
        self.win_controller = WindowsController()
        self.camera_controller = CameraController()  # DÜZELTİLMİŞ KAMERA KONTROLLERİ
        self.assistant_profile = AssistantProfile()
        self.memory = Memory()
        self.tts = TTSEngine()
        self.brain = AssistantBrain(self.memory, self.win_controller, self.camera_controller, self.assistant_profile)
        self.brain.set_parent_window(self.root)
        
        # Menü popup'ı
        self.menu_popup = MenuPopup(self.root, self)
        
        self._build_ui()
        
        self._update_system_stats()
        self._update_uptime()
        self._update_weather()
        self._update_animation()
        
        self._add_message("KUDUKO MUZİK YAPİM ASİSTAN AL", "Merhaba, ben KUDUKO MUZİK YAPİM ASİSTAN AL. Bugün size nasıl yardımcı olabilirim?")
    
    def _build_ui(self):
        # Üst çubuk (başlık + menü butonu)
        top_bar = tk.Frame(self.root, bg=BG_DIM)
        top_bar.pack(fill="x", padx=20, pady=(20, 0))
        
        tk.Label(top_bar, text="KUDUKO MUZİK YAPİM ASİSTAN AL", bg=BG_DIM, fg=ACCENT,
                font=("Consolas", 18, "bold")).pack(side="left", padx=15, pady=10)
        
        # Menü butonu (sağ üst)
        menu_btn = tk.Button(top_bar, text="☰ MENÜ", command=self.menu_popup.show,
                             bg=ACCENT_DARK, fg="white", font=("Consolas", 10, "bold"),
                             bd=0, padx=15, pady=6, cursor="hand2")
        menu_btn.pack(side="right", padx=15)
        
        # Ana içerik
        main = tk.Frame(self.root, bg=BG_DARK)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        left = tk.Frame(main, bg=BG_DARK, width=400)
        left.pack(side="left", fill="y", padx=(0, 15))
        left.pack_propagate(False)
        
        # Alt başlık
        tk.Label(left, text="Oldukça Zeki Bir Sistem", 
                bg=BG_DARK, fg=TEXT_DIM, font=("Consolas", 9)).pack(anchor="w", pady=(0, 15))
        
        # Animasyon kartı
        anim_card = tk.Frame(left, bg=BG_CARD)
        anim_card.pack(fill="x", pady=(0, 12))
        
        anim_title = tk.Frame(anim_card, bg=BG_DIM)
        anim_title.pack(fill="x")
        tk.Label(anim_title, text="KUDUKO MUZİK YAPİM ASİSTAN AL", bg=BG_DIM, fg=ACCENT, font=("Consolas", 10, "bold")).pack(side="left", padx=10, pady=6)
        
        anim_content = tk.Frame(anim_card, bg=BG_CARD, height=220)
        anim_content.pack(fill="x", padx=12, pady=10)
        anim_content.pack_propagate(False)
        
        self.anim_canvas = tk.Canvas(anim_content, width=200, height=200, bg=BG_CARD, highlightthickness=0)
        self.anim_canvas.pack(expand=True)
        
        self.cx = 100
        self.cy = 100
        
        self.anim_canvas.create_oval(10, 10, 190, 190, outline=BG_DIM, width=1)
        self.anim_canvas.create_oval(20, 20, 180, 180, outline=BG_DIM, width=1)
        self.anim_canvas.create_oval(30, 30, 170, 170, outline=BG_DIM, width=1)
        
        self.ring = self.anim_canvas.create_arc(15, 15, 185, 185, start=0, extent=270, outline=ACCENT, width=4, style="arc")
        self.ring2 = self.anim_canvas.create_arc(25, 25, 175, 175, start=90, extent=200, outline=PURPLE, width=2, style="arc")
        
        self.squares = []
        square_positions = [(60, 60), (140, 60), (140, 140), (60, 140)]
        for x, y in square_positions:
            square = self.anim_canvas.create_rectangle(x-8, y-8, x+8, y+8, fill=ACCENT, outline="")
            self.squares.append(square)
        
        self.dots = []
        for i in range(8):
            dot = self.anim_canvas.create_oval(0, 0, 4, 4, fill=ACCENT, outline="")
            self.dots.append(dot)
        
        self.anim_text = self.anim_canvas.create_text(100, 100, text="KUDUKO", fill=ACCENT, font=("Consolas", 12, "bold"))
        
        status_text = tk.Label(anim_content, text="SİSTEM ÇEVRİMİÇİ | ÇEKİRDEK AKTİF", bg=BG_CARD, fg=GREEN, font=("Consolas", 8))
        status_text.pack(pady=(5, 0))
        
        self._create_card(left, "SİSTEM İSTATİSTİKLERİ")
        
        stats_frame = tk.Frame(left, bg=BG_CARD)
        stats_frame.pack(fill="x", pady=(0, 10))
        
        cpu_frame = tk.Frame(stats_frame, bg=BG_CARD)
        cpu_frame.pack(side="left", expand=True, fill="both")
        self.cpu_canvas = tk.Canvas(cpu_frame, width=100, height=100, bg=BG_CARD, highlightthickness=0)
        self.cpu_canvas.pack(pady=5)
        self.cpu_canvas.create_oval(5, 5, 95, 95, outline=BG_DIM, width=8)
        self.cpu_arc = self.cpu_canvas.create_arc(5, 5, 95, 95, start=90, extent=0, outline=ACCENT, width=8, style="arc")
        self.cpu_text = self.cpu_canvas.create_text(50, 50, text="0%", fill=ACCENT, font=("Consolas", 14, "bold"))
        tk.Label(cpu_frame, text="İşlemci Kullanım", bg=BG_CARD, fg=TEXT_DIM, font=("Consolas", 9)).pack()
        
        ram_frame = tk.Frame(stats_frame, bg=BG_CARD)
        ram_frame.pack(side="right", expand=True, fill="both")
        self.ram_canvas = tk.Canvas(ram_frame, width=100, height=100, bg=BG_CARD, highlightthickness=0)
        self.ram_canvas.pack(pady=5)
        self.ram_canvas.create_oval(5, 5, 95, 95, outline=BG_DIM, width=8)
        self.ram_arc = self.ram_canvas.create_arc(5, 5, 95, 95, start=90, extent=0, outline=GREEN, width=8, style="arc")
        self.ram_text = self.ram_canvas.create_text(50, 50, text="0%", fill=GREEN, font=("Consolas", 14, "bold"))
        tk.Label(ram_frame, text="Hafıza Kullanım", bg=BG_CARD, fg=TEXT_DIM, font=("Consolas", 9)).pack()
        
        details = tk.Frame(left, bg=BG_CARD)
        details.pack(fill="x", pady=(0, 15))
        
        cpu_detail = tk.Frame(details, bg=BG_CARD)
        cpu_detail.pack(fill="x", pady=2)
        tk.Label(cpu_detail, text="İşlemci:", bg=BG_CARD, fg=TEXT_DIM, font=("Consolas", 9, "bold"), width=8, anchor="w").pack(side="left")
        self.cpu_detail = tk.Label(cpu_detail, text="0%", bg=BG_CARD, fg=TEXT, font=("Consolas", 9))
        self.cpu_detail.pack(side="left")
        
        ram_detail = tk.Frame(details, bg=BG_CARD)
        ram_detail.pack(fill="x", pady=2)
        tk.Label(ram_detail, text="Hafıza:", bg=BG_CARD, fg=TEXT_DIM, font=("Consolas", 9, "bold"), width=8, anchor="w").pack(side="left")
        self.ram_detail = tk.Label(ram_detail, text="0/0 GB", bg=BG_CARD, fg=TEXT, font=("Consolas", 9))
        self.ram_detail.pack(side="left")
        
        self._create_card(left, "HAVA DURUMU")
        weather_content = tk.Frame(left, bg=BG_CARD)
        weather_content.pack(fill="x", pady=(0, 15))
        
        self.temp_label = tk.Label(weather_content, text="--°C", bg=BG_CARD, fg=ACCENT, font=("Consolas", 32, "bold"))
        self.temp_label.pack(anchor="w")
        self.location_label = tk.Label(weather_content, text="Türkiye", bg=BG_CARD, fg=TEXT_DIM, font=("Consolas", 9))
        self.location_label.pack(anchor="w", pady=(0, 10))
        
        weather_details = tk.Frame(weather_content, bg=BG_CARD)
        weather_details.pack(fill="x")
        self.humidity_label = tk.Label(weather_details, text="Nem: --%", bg=BG_CARD, fg=TEXT, font=("Consolas", 9))
        self.humidity_label.pack(side="left")
        self.wind_label = tk.Label(weather_details, text="Rüzgar: -- m/s", bg=BG_CARD, fg=TEXT, font=("Consolas", 9))
        self.wind_label.pack(side="right")
        
        # CAMERA STATUS KARTI
        self._create_card(left, "KAMERA DURUMU")
        camera_content = tk.Frame(left, bg=BG_CARD)
        camera_content.pack(fill="x", pady=(0, 15))
        
        self.camera_status = tk.Label(camera_content, text="📷 Kamera Kapalı\n\nMenüden açabilirsiniz", bg=BG_CARD, fg=TEXT_DIM, font=("Consolas", 9), justify="center")
        self.camera_status.pack(fill="x", pady=(0, 10))
        
        cam_info = tk.Label(camera_content, text="Kamera kontrolü için MENÜ butonuna tıklayın", bg=BG_CARD, fg=TEXT_DIM, font=("Consolas", 7))
        cam_info.pack(pady=(0, 5))
        
        self._create_card(left, "SYSTEM UPTIME")
        uptime_content = tk.Frame(left, bg=BG_CARD)
        uptime_content.pack(fill="x", pady=(0, 15))
        
        self.uptime_label = tk.Label(uptime_content, text="00:00:00", bg=BG_CARD, fg=ACCENT, font=("Consolas", 20, "bold"))
        self.uptime_label.pack(anchor="w")
        tk.Label(uptime_content, text="Durum: Çalışıyor", bg=BG_CARD, fg=GREEN, font=("Consolas", 9)).pack(anchor="w", pady=(5, 10))
        
        status_table = tk.Frame(uptime_content, bg=BG_CARD)
        status_table.pack(fill="x")
        tk.Label(status_table, text="Durum", bg=BG_CARD, fg=ACCENT, font=("Consolas", 9, "bold"), width=10, anchor="w").grid(row=0, column=0, sticky="w")
        tk.Label(status_table, text="Bileşen", bg=BG_CARD, fg=ACCENT, font=("Consolas", 9, "bold"), width=15, anchor="w").grid(row=0, column=1, sticky="w")
        
        self.cpu_status = tk.Label(status_table, text="● Normal", bg=BG_CARD, fg=GREEN, font=("Consolas", 9))
        self.cpu_status.grid(row=1, column=0, sticky="w", pady=2)
        tk.Label(status_table, text="İşlemci", bg=BG_CARD, fg=TEXT, font=("Consolas", 9)).grid(row=1, column=1, sticky="w")
        
        self.ram_status = tk.Label(status_table, text="● Normal", bg=BG_CARD, fg=GREEN, font=("Consolas", 9))
        self.ram_status.grid(row=2, column=0, sticky="w", pady=2)
        tk.Label(status_table, text="Hafıza", bg=BG_CARD, fg=TEXT, font=("Consolas", 9)).grid(row=2, column=1, sticky="w")
        
        self.disk_status = tk.Label(status_table, text="● Normal", bg=BG_CARD, fg=GREEN, font=("Consolas", 9))
        self.disk_status.grid(row=3, column=0, sticky="w", pady=2)
        tk.Label(status_table, text="Depolama", bg=BG_CARD, fg=TEXT, font=("Consolas", 9)).grid(row=3, column=1, sticky="w")
        
        # SAĞ TARAF - KONUŞMA ALANI
        right = tk.Frame(main, bg=BG_DARK)
        right.pack(side="right", fill="both", expand=True)
        
        self._create_card(right, "Gelişmiş Kişisel Asistanınızla Konuşun", height=450)
        conv_content = tk.Frame(right, bg=BG_CARD)
        conv_content.pack(fill="both", expand=True, pady=(0, 10))
        
        history_container = tk.Frame(conv_content, bg=BG_CARD)
        history_container.pack(fill="both", expand=True)
        
        text_frame = tk.Frame(history_container, bg=BG_DIM)
        text_frame.pack(fill="both", expand=True)
        
        self.conv_text = tk.Text(text_frame, bg=BG_DIM, fg=TEXT, font=("Consolas", 10), wrap="word", bd=0, state="disabled")
        self.conv_text.pack(side="left", fill="both", expand=True)
        
        scroll = tk.Scrollbar(text_frame, command=self.conv_text.yview)
        scroll.pack(side="right", fill="y")
        self.conv_text.config(yscrollcommand=scroll.set)
        
        timestamp_frame = tk.Frame(conv_content, bg=BG_CARD)
        timestamp_frame.pack(fill="x", pady=(5, 0))
        self.timestamp_label = tk.Label(timestamp_frame, text="Hazır", bg=BG_CARD, fg=TEXT_DIM, font=("Consolas", 8))
        self.timestamp_label.pack(side="right")
        
        # MESAJ GİRİŞ ALANI
        input_frame = tk.Frame(right, bg=BG_DARK)
        input_frame.pack(fill="x", pady=(10, 0))
        
        self.message_entry = tk.Entry(input_frame, bg=BG_DIM, fg=TEXT, font=("Consolas", 11), insertbackground=ACCENT, bd=0, relief="flat")
        self.message_entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 10))
        self.message_entry.bind("<Return>", lambda e: self._send_message())
        
        send_btn = tk.Button(input_frame, text="GÖNDER", command=self._send_message, bg=ACCENT_DARK, fg=TEXT, font=("Consolas", 10, "bold"), bd=0, padx=20, pady=8, cursor="hand2")
        send_btn.pack(side="right")
        
        bottom = tk.Frame(right, bg=BG_DARK)
        bottom.pack(fill="x", pady=(10, 0))
        
        stt_color = GREEN if STT_AVAILABLE else WARN
        tts_color = GREEN if TTS_AVAILABLE else WARN
        cam_color = GREEN if CAMERA_AVAILABLE else WARN
        
        tk.Label(bottom, text="🎤 STT ✓" if STT_AVAILABLE else "🎤 STT ✗", bg=BG_DARK, fg=stt_color, font=("Consolas", 8)).pack(side="left")
        tk.Label(bottom, text="🔊 TTS ✓" if TTS_AVAILABLE else "🔊 TTS ✗", bg=BG_DARK, fg=tts_color, font=("Consolas", 8)).pack(side="left", padx=10)
        tk.Label(bottom, text="📷 CAM ✓" if CAMERA_AVAILABLE else "📷 CAM ✗", bg=BG_DARK, fg=cam_color, font=("Consolas", 8)).pack(side="left")
        
        self.mem_label = tk.Label(bottom, text=f"💾 HAFIZA: {self.memory.call_count}", bg=BG_DARK, fg=TEXT_DIM, font=("Consolas", 8))
        self.mem_label.pack(side="right")
    
    def _create_card(self, parent, title, height=None):
        card = tk.Frame(parent, bg=BG_CARD)
        card.pack(fill="x", pady=(0, 12))
        title_frame = tk.Frame(card, bg=BG_DIM)
        title_frame.pack(fill="x")
        tk.Label(title_frame, text=title, bg=BG_DIM, fg=ACCENT, font=("Consolas", 10, "bold")).pack(side="left", padx=10, pady=6)
        content = tk.Frame(card, bg=BG_CARD)
        content.pack(fill="both", expand=True, padx=12, pady=10)
        return content
    
    def _update_system_stats(self):
        if PSUTIL_AVAILABLE:
            try:
                cpu = psutil.cpu_percent(interval=0.3)
                angle = (cpu / 100) * 360
                self.cpu_canvas.itemconfig(self.cpu_arc, extent=-angle)
                self.cpu_canvas.itemconfig(self.cpu_text, text=f"{cpu:.0f}%")
                self.cpu_detail.config(text=f"{cpu:.1f}%")
                
                if cpu < 50:
                    self.cpu_status.config(text="● Normal", fg=GREEN)
                elif cpu < 80:
                    self.cpu_status.config(text="● Orta", fg=AMBER)
                else:
                    self.cpu_status.config(text="● Yüksek", fg=WARN)
                
                ram = psutil.virtual_memory()
                ram_angle = (ram.percent / 100) * 360
                self.ram_canvas.itemconfig(self.ram_arc, extent=-ram_angle)
                self.ram_canvas.itemconfig(self.ram_text, text=f"{ram.percent:.0f}%")
                self.ram_detail.config(text=f"{ram.used/(1024**3):.1f}/{ram.total/(1024**3):.0f} GB")
                
                if ram.percent < 50:
                    self.ram_status.config(text="● Normal", fg=GREEN)
                elif ram.percent < 80:
                    self.ram_status.config(text="● Orta", fg=AMBER)
                else:
                    self.ram_status.config(text="● Yüksek", fg=WARN)
                
                disk = psutil.disk_usage('/')
                if disk.percent < 70:
                    self.disk_status.config(text="● Normal", fg=GREEN)
                elif disk.percent < 90:
                    self.disk_status.config(text="● Orta", fg=AMBER)
                else:
                    self.disk_status.config(text="● Kritik", fg=WARN)
            except: pass
        self.root.after(2000, self._update_system_stats)
    
    def _update_uptime(self):
        uptime = datetime.datetime.now() - self.start_time
        hours = uptime.seconds // 3600
        minutes = (uptime.seconds % 3600) // 60
        seconds = uptime.seconds % 60
        self.uptime_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        self.timestamp_label.config(text=f"{datetime.datetime.now().strftime('%H:%M:%S')}")
        self.root.after(1000, self._update_uptime)
    
    def _update_weather(self):
        temps = [22.5, 23.1, 24.8, 25.2, 26.0]
        self.temp_label.config(text=f"{random.choice(temps):.1f}°C")
        self.humidity_label.config(text=f"Nem: {random.randint(45, 85)}%")
        self.wind_label.config(text=f"Rüzgar: {random.uniform(2.5, 12.0):.1f} m/s")
        self.root.after(30000, self._update_weather)
    
    def _update_animation(self):
        self.angle = (self.angle + 5) % 360
        self.anim_canvas.itemconfig(self.ring, start=self.angle, extent=270)
        
        self.ring2_angle = (self.ring2_angle - 3) % 360
        self.anim_canvas.itemconfig(self.ring2, start=self.ring2_angle, extent=200)
        
        self.square_angle = (self.square_angle + 4) % 360
        radius = 50
        square_positions = []
        for i in range(4):
            angle_rad = math.radians(self.square_angle + i * 90)
            x = self.cx + radius * math.cos(angle_rad)
            y = self.cy + radius * math.sin(angle_rad)
            square_positions.append((x, y))
        
        square_colors = [ACCENT, GREEN, AMBER, PURPLE]
        for i, square in enumerate(self.squares):
            x, y = square_positions[i]
            self.anim_canvas.coords(square, x-8, y-8, x+8, y+8)
            self.anim_canvas.itemconfig(square, fill=square_colors[i % len(square_colors)])
        
        self.dot_angle = (self.dot_angle + 6) % 360
        dot_radius = 70
        for i, dot in enumerate(self.dots):
            angle_rad = math.radians(self.dot_angle + i * 45)
            x = self.cx + dot_radius * math.cos(angle_rad)
            y = self.cy + dot_radius * math.sin(angle_rad)
            self.anim_canvas.coords(dot, x-2, y-2, x+2, y+2)
        
        self.pulse += 0.05 * self.pulse_dir
        if self.pulse >= 1.2:
            self.pulse_dir = -1
        elif self.pulse <= 0.8:
            self.pulse_dir = 1
        
        self.root.after(50, self._update_animation)
    
    def _send_message(self):
        msg = self.message_entry.get().strip()
        if not msg:
            return
        self.message_entry.delete(0, tk.END)
        self._add_message("USER", msg)
        self._process_command(msg)
    
    def _quick_command(self, cmd):
        self._add_message("USER", cmd)
        self._process_command(cmd)
    
    def _process_command(self, command):
        response, module = self.brain.respond(command)
        response = self.assistant_profile.modify_response(response, module)
        self._add_message("KUDUKO MUZİK YAPİM ASİSTAN AL", response, module)
        self.mem_label.config(text=f"💾 HAFIZA: {self.memory.call_count}")
        if TTS_AVAILABLE:
            threading.Thread(target=self.tts.speak, args=(response,), daemon=True).start()
    
    def _add_message(self, sender, message, module=None):
        self.conv_text.config(state="normal")
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        if sender == "KUDUKO MUZİK YAPİM ASİSTAN AL":
            tag = "assistant"
            self.conv_text.tag_config(tag, foreground=ACCENT)
            prefix = f"[{timestamp}] 🤖 KUDUKO MUZİK YAPİM ASİSTAN AL"
            if module:
                prefix += f" [{module}]"
        elif sender == "USER":
            tag = "user"
            self.conv_text.tag_config(tag, foreground=GREEN)
            prefix = f"[{timestamp}] 👤 KULLANICI"
        else:
            tag = "system"
            self.conv_text.tag_config(tag, foreground=TEXT_DIM)
            prefix = f"[{timestamp}] 🔧 SYSTEM"
        self.conv_text.insert("end", f"{prefix}: ", "system")
        self.conv_text.insert("end", f"{message}\n\n", tag)
        self.conv_text.see("end")
        self.conv_text.config(state="disabled")
    
    def run(self):
        self.root.mainloop()


# ═══════════════════════════════════════════════════════════════════
# BAŞLATMA
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║     KUDUKO MUZİK YAPİM ASİSTAN AL
    ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    app = CyberAssistantApp()
    app.run()