#!/usr/bin/env python3
"""
KUDUKOMUZİKYAPİMASİSTANAL Windows — Gercek zamanli sesli yardimci cekirdegi
KUDUKOMUZİKYAPİMASİSTANAL tarafından yapılmıştır — @KUDUKOMUZİKYAPİMASİSTANAL
Windows ortamina uyarlanmis calisma akisi
"""

import asyncio
import datetime
import threading
import traceback
import os
import re
import subprocess
import sys
import time
import sqlite3
import shutil
from pathlib import Path

import pyaudio  # type: ignore[reportMissingModuleSource]
from google import genai  # type: ignore[reportMissingImports]
from google.genai import types  # type: ignore[reportMissingImports]

from app_config import get_app_config_value
from ui import JarvisUI
from memory.memory_manager import load_memory, update_memory, delete_memory, format_memory_for_prompt
from actions.open_app import open_app
from actions.sys_info  import sys_info
from actions.calendar import get_calendar_events, add_calendar_event, delete_calendar_event
from actions.reminders import get_reminders, add_reminder
from actions.browser   import browser_control
from actions.shell     import shell_run
from actions.whatsapp  import send_whatsapp_message, save_whatsapp_contact, call_whatsapp
from actions.media     import play_media
from actions.weather   import get_weather_summary
from actions.screen_vision import analyze_screen
from actions.youtube_stats import get_youtube_channel_report

# WEB SUNUCUSU IMPORTLARI - Güncellenmiş
from web_server import start_web_server, command_queue, response_queue, set_web_status

# ===== WHATSAPP MESAJ OKUYUCU =====
class WhatsAppMessageReader:
    """WhatsApp mesajlarını okuyan ve sesli bildiren sınıf"""
    
    def __init__(self, ui):
        self.ui = ui
        self.last_message_id = None
        self.running = False
        self.monitor_thread = None
        self.sent_messages = set()
        self.whatsapp_db_paths = self._find_whatsapp_databases()
        
    def _find_whatsapp_databases(self):
        possible_paths = []
        local_app_data = os.environ.get('LOCALAPPDATA', '')
        if local_app_data:
            wa_paths = [
                os.path.join(local_app_data, 'WhatsApp', 'databases'),
                os.path.join(local_app_data, 'WhatsAppDesktop', 'databases'),
                os.path.join(local_app_data, 'Programs', 'WhatsApp', 'databases'),
            ]
            for path in wa_paths:
                if os.path.exists(path):
                    possible_paths.extend([os.path.join(path, f) for f in os.listdir(path) if f.endswith('.db')])
            
            chrome_data = os.path.join(local_app_data, 'Google', 'Chrome', 'User Data', 'Default', 'databases')
            if os.path.exists(chrome_data):
                for root, dirs, files in os.walk(chrome_data):
                    for file in files:
                        if file.endswith('.db') and ('whatsapp' in file.lower() or 'wa' in file.lower()):
                            possible_paths.append(os.path.join(root, file))
        return possible_paths
    
    def _get_wa_db_connection(self):
        for db_path in self.whatsapp_db_paths:
            try:
                temp_path = os.path.join(os.environ.get('TEMP', ''), f'wa_chat_{int(time.time())}.db')
                shutil.copy2(db_path, temp_path)
                conn = sqlite3.connect(temp_path)
                conn.row_factory = sqlite3.Row
                return conn, temp_path
            except Exception as e:
                print(f"WhatsApp DB bağlantı hatası ({db_path}): {e}")
                continue
        return None, None
    
    def _get_last_messages(self):
        conn, temp_path = self._get_wa_db_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            tables = ['messages', 'chat', 'message', 'wa_messages', 'chat_messages']
            messages = []
            
            for table in tables:
                try:
                    cursor.execute(f"""
                        SELECT 
                            id, 
                            message_text, 
                            sender_name, 
                            timestamp,
                            is_from_me
                        FROM {table} 
                        ORDER BY timestamp DESC 
                        LIMIT 10
                    """)
                    rows = cursor.fetchall()
                    if rows:
                        for row in rows:
                            messages.append({
                                'id': row['id'],
                                'text': row['message_text'],
                                'sender': row['sender_name'] or ('Ben' if row['is_from_me'] else 'WhatsApp'),
                                'timestamp': row['timestamp'],
                                'is_from_me': row['is_from_me']
                            })
                        break
                except:
                    continue
            
            conn.close()
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
            return messages
        except Exception as e:
            print(f"WhatsApp mesaj okuma hatası: {e}")
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
            return []
    
    def start_monitoring(self):
        if self.running:
            return
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.ui.write_log("WhatsApp: Mesaj izleme başlatıldı.")
    
    def stop_monitoring(self):
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        self.ui.write_log("WhatsApp: Mesaj izleme durduruldu.")
    
    def _monitor_loop(self):
        while self.running:
            try:
                messages = self._get_last_messages()
                for msg in messages:
                    msg_key = f"{msg['id']}_{msg['timestamp']}"
                    if not msg.get('is_from_me', False) and msg_key not in self.sent_messages:
                        self.sent_messages.add(msg_key)
                        sender = msg.get('sender', 'Birisi')
                        text = msg.get('text', '')
                        if text and text.strip():
                            log_msg = f"📱 WhatsApp - {sender}: {text}"
                            self.ui.write_log(log_msg)
                            speak_text = f"WhatsApp\'tan {sender} mesaj gönderdi: {text}"
                            self._speak_message(speak_text)
                            self.ui.on_text_command(f"WhatsApp\'tan {sender} şu mesajı geldi: {text}")
                
                time.sleep(3)
                if len(self.sent_messages) > 100:
                    self.sent_messages = set(list(self.sent_messages)[-100:])
            except Exception as e:
                print(f"WhatsApp izleme hatası: {e}")
                time.sleep(5)
    
    def _speak_message(self, text):
        try:
            import win32com.client
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(text)
        except ImportError:
            try:
                import pyttsx3
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
            except:
                print(f"Seslendirme hatası: {text}")
    
    def read_recent_messages(self, count=5):
        messages = self._get_last_messages()
        unread_messages = [m for m in messages if not m.get('is_from_me', False)]
        if not unread_messages:
            return "WhatsApp'ta okunmamış mesaj bulunamadı."
        result = f"Son {min(count, len(unread_messages))} WhatsApp mesajı:\n"
        for msg in unread_messages[:count]:
            sender = msg.get('sender', 'Birisi')
            text = msg.get('text', '')
            result += f"- {sender}: {text}\n"
        return result

# ===== SİSTEM KOMUTLARI =====
systemCommands = {
    'merhaba': '<strong>KUDUKOMUZİKYAPİMASİSTANAL</strong>\'a hoş geldiniz! <br>Bugün size nasıl yardımcı olabilirim?',
    'selam': '<strong>KUDUKOMUZİKYAPİMASİSTANAL</strong>: Selam! Size nasıl yardımcı olabilirim?',
    'saat kaç': lambda: f"<strong>KUDUKOMUZİKYAPİMASİSTANAL</strong>: Şu an saat: {datetime.datetime.now().strftime('%H:%M:%S')}",
    'tarih ne': lambda: f"<strong>KUDUKOMUZİKYAPİMASİSTANAL</strong>: Bugün: {datetime.datetime.now().strftime('%A, %d %B %Y')}",
    'iyi misin': '<strong>KUDUKOMUZİKYAPİMASİSTANAL</strong>: Gayet iyiyim! Yardımcı olabileceğim bir şey var mı?',
    'neler yapıyorsun': '<strong>KUDUKOMUZİKYAPİMASİSTANAL</strong>: Seninle konuşuyorum. :) Komut bekliyorum.',
    'komutlar': f'''<strong>KUDUKOMUZİKYAPİMASİSTANAL</strong>: 150+ komut mevcut! Sistem, medya, web, sohbet kategorileri.<br><br>
                <strong>Örnek Komutlar:</strong><br>
                • asistan al aç<br>• youtube aç<br>• spotify aç<br>• google aç<br>
                • whatsapp aç<br>
                • saat kaç<br> • sosyal media hesaplarım<br> • hakkında<br> • seni kim geliştirdi<br> • seni kim icat etti<br> • senin yaratıcın kim<br> • kuduko müzik yapım kimdir<br> • eren mutlu 0bozkurtlar1 kuduko kimdir<br> <br>• bana hakaret et<br><br>• bana küfür et<br><br>• iletişim bilgiler<br><br>• neler yapıyorsun<br><br>• iyi misin<br><br>• merhaba<br><br>• javascript kodu göster<br><br>
                <strong>WhatsApp Komutları:</strong><br>
                • whatsapp mesajlarını oku<br>• whatsapp takip et<br>• whatsapp izlemeyi durdur<br>• son whatsapp mesajlarını oku<br>
                <em>Web arayüzünde sistem komutları çalışmaktadır.</em>''',
    'hakkında': f'''<strong>KUDUKOMUZİKYAPİMASİSTANAL</strong>: Kuduko Müzik Yapım & Dağıtım Kanalı...''',
    'seni kim geliştirdi': f'''<strong>KUDUKOMUZİKYAPİMASİSTANAL</strong>: Merhaba! Kuduko Müzik Yapım - Asistan Al olarak karşınızdayım. Beni Geliştiren Kişi Eren Mutlu 0BozKurtlar1 Kuduko...''',
    'bana hakaret et': f'''<strong>KUDUKOMUZİKYAPİMASİSTANAL</strong>: Götün Yiyorsa Sıkıysa Gel...''',
    'iletişim bilgiler': f'''<strong>KUDUKOMUZİKYAPİMASİSTANAL</strong>: Şu anda Ulaşılamıyor...''',
    'seni kim icat etti': f'''Merhaba! <strong>Kuduko Müzik Yapım - Asistan Al</strong> olarak karşınızdayım...''',
    'sosyal media hesaplarım': f'''<strong>KUDUKOMUZİKYAPİMASİSTANAL</strong>: 
    <strong>Web site:</strong> <a href="https://kudukomuzikyapimdijitalmuzikplatform.42web.io" target="_blank">https://kudukomuzikyapimdijitalmuzikplatform.42web.io</a><br> 
    <strong>asistan al aç:</strong> <a href="https://kudukomuzikyapimasistanal.42web.io" target="_blank">https://kudukomuzikyapimasistanal.42web.io</a><br>...''',
    'senin yaratıcın kim': f'''Merhaba! Ben <strong>Kuduko Müzik Yapım - Asistan Al</strong>...''',
    'kuduko müzik yapım kimdir': f'''<strong>KUDUKOMUZİKYAPİMASİSTANAL</strong>: Kuduko Müzik Yapım...''',
    'eren mutlu 0bozkurtlar1 kuduko kimdir': f'''<strong>KUDUKOMUZİKYAPİMASİSTANAL</strong>: Gerçek Adı Eren Mutlu...''',
    'bana küfür et': f'''<strong>KUDUKOMUZİKYAPİMASİSTANAL</strong>: Fakyou Bich...''',
    'javascript kodu göster': f'''<strong>KUDUKOMUZİKYAPİMASİSTANAL</strong>: İşte size örnek bir JavaScript kodu:<br><br>
<pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:8px; overflow-x:auto; font-family:monospace;">
<span style="color:#569cd6">function</span> <span style="color:#dcdcaa">merhabaDunya</span>() {{
    <span style="color:#569cd6">let</span> <span style="color:#9cdcfe">mesaj</span> = <span style="color:#ce9178">"Merhaba Dünya!"</span>;
    <span style="color:#dcdcaa">console</span>.<span style="color:#dcdcaa">log</span>(mesaj);
    <span style="color:#569cd6">return</span> mesaj;
}}
merhabaDunya();
</pre>''',
    'whatsapp mesajlarını oku': lambda: "WhatsApp mesaj takibi başlatılıyor...",
    'whatsapp takip et': lambda: "WhatsApp mesaj takibi başlatılıyor...",
    'whatsapp izlemeyi durdur': lambda: "WhatsApp mesaj takibi durduruluyor...",
    'son whatsapp mesajlarını oku': None,
}

def process_system_command(text: str, wa_reader=None) -> str:
    text_lower = text.lower().strip()
    
    if 'son whatsapp mesajlarını oku' in text_lower or 'son whatsapp mesajları' in text_lower:
        if wa_reader:
            return wa_reader.read_recent_messages(5)
        return "WhatsApp okuyucu başlatılmamış."
    
    if 'whatsapp mesajlarını oku' in text_lower or 'whatsapp takip et' in text_lower:
        if wa_reader:
            wa_reader.start_monitoring()
            return "WhatsApp mesaj takibi başlatıldı."
        return "WhatsApp okuyucu başlatılamadı."
    
    if 'whatsapp izlemeyi durdur' in text_lower:
        if wa_reader:
            wa_reader.stop_monitoring()
            return "WhatsApp mesaj takibi durduruldu."
        return "WhatsApp okuyucu başlatılmamış."
    
    for cmd_key, cmd_value in systemCommands.items():
        if cmd_key in text_lower and cmd_value is not None:
            if callable(cmd_value):
                return cmd_value()
            return cmd_value
    return None

# ── Paths ───────────────────────────────────────────────────────────────────
BASE_DIR        = Path(__file__).resolve().parent
PROMPT_PATH     = BASE_DIR / "core" / "prompt.txt"

CONTROL_TOKEN_RE = re.compile(r"<ctrl\d+>", re.IGNORECASE)
LIVE_MODEL = "models/gemini-2.5-flash-native-audio-latest"

# ── Audio ───────────────────────────────────────────────────────────────────
FORMAT           = pyaudio.paInt16
CHANNELS         = 1
SEND_SAMPLE_RATE = 16000
RECV_SAMPLE_RATE = 24000
CHUNK_SIZE       = 1024
pya              = pyaudio.PyAudio()

# ── Tool tanımları (kısaltılmış) ──────────────────────────────────────────
TOOL_DECLARATIONS = [
    {"name": "handle_system_command", "description": "Sistem komutlarını işler...", "parameters": {"type": "OBJECT", "properties": {"command": {"type": "STRING"}}, "required": ["command"]}},
    {"name": "open_app", "description": "Windows'ta uygulama açar", "parameters": {"type": "OBJECT", "properties": {"app_name": {"type": "STRING"}}, "required": ["app_name"]}},
    {"name": "close_app", "description": "Uygulama kapatır", "parameters": {"type": "OBJECT", "properties": {"app_name": {"type": "STRING"}, "force": {"type": "BOOLEAN"}}, "required": ["app_name"]}},
    # ... diğer tool tanımları mevcut kodunuzdaki gibi devam edecek
]

def get_api_key() -> str:
    return str(get_app_config_value("gemini_api_key", "") or "")

def load_system_prompt() -> str:
    try:
        return PROMPT_PATH.read_text(encoding="utf-8")
    except Exception:
        return "Sen KUDUKOMUZİKYAPİMASİSTANAL'sin — Windows'ta çalışan kişisel AI asistanı."

# ── Fonksiyonlar ──────────────────────────────────────────────────────────
def close_app(app_name: str, force: bool = False) -> str:
    try:
        cmd = f'taskkill /f /im "{app_name}.exe"' if force else f'taskkill /im "{app_name}.exe"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return f"{app_name} başarıyla kapatıldı."
        return f"{app_name} kapatılırken hata: {result.stderr or 'Uygulama bulunamadı'}"
    except Exception as e:
        return f"Hata: {e}"

def close_all_apps(except_list: list = None) -> str:
    try:
        if except_list is None:
            except_list = []
        exceptions = except_list + ["explorer", "taskmgr", "python", "cmd", "powershell", "conhost"]
        result = subprocess.run('tasklist /FO CSV /NH', shell=True, capture_output=True, text=True)
        closed_apps = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            parts = line.strip('"').split('","')
            if not parts:
                continue
            proc_name = parts[0]
            proc_base = proc_name.lower().replace('.exe', '')
            is_exception = any(exc.lower() == proc_base for exc in exceptions)
            if is_exception:
                continue
            try:
                subprocess.run(f'taskkill /im "{proc_name}"', shell=True, capture_output=True, text=True, timeout=2)
                closed_apps.append(proc_name)
            except:
                pass
        if closed_apps:
            return f"✅ {len(closed_apps)} uygulama kapatıldı"
        return "🔍 Kapatılacak uygulama bulunamadı."
    except Exception as e:
        return f"❌ Hata: {e}"

def wifi_control(action: str) -> str:
    action = action.lower().strip()
    try:
        if action == "on":
            subprocess.run('netsh interface set interface "Wi-Fi" admin=enabled', shell=True)
            return "WiFi açıldı."
        elif action == "off":
            subprocess.run('netsh interface set interface "Wi-Fi" admin=disabled', shell=True)
            return "WiFi kapatıldı."
        elif action == "status":
            result = subprocess.run('netsh interface show interface "Wi-Fi"', shell=True, capture_output=True, text=True)
            if "Bağlı" in result.stdout or "Enabled" in result.stdout:
                return "WiFi açık."
            return "WiFi kapalı."
        return f"Bilinmeyen aksiyon: {action}"
    except Exception as e:
        return f"WiFi hatası: {e}"

def bluetooth_control(action: str) -> str:
    action = action.lower().strip()
    try:
        if action == "on":
            ps = '''$bt = Get-PnpDevice -Class Bluetooth; if($bt){Enable-PnpDevice -InstanceId $bt.InstanceId -Confirm:$false}'''
            subprocess.run(["powershell", "-Command", ps], capture_output=True)
            return "Bluetooth açıldı."
        elif action == "off":
            ps = '''$bt = Get-PnpDevice -Class Bluetooth; if($bt){Disable-PnpDevice -InstanceId $bt.InstanceId -Confirm:$false}'''
            subprocess.run(["powershell", "-Command", ps], capture_output=True)
            return "Bluetooth kapatıldı."
        elif action == "status":
            ps = '''$bt = Get-PnpDevice -Class Bluetooth; if($bt.Status -eq "OK"){"enabled"}else{"disabled"}'''
            result = subprocess.run(["powershell", "-Command", ps], capture_output=True, text=True)
            if "enabled" in result.stdout.lower():
                return "Bluetooth açık."
            return "Bluetooth kapalı."
        return f"Bilinmeyen aksiyon: {action}"
    except Exception as e:
        return f"Bluetooth hatası: {e}"

class JarvisLive:
    def __init__(self, ui: JarvisUI):
        self.ui             = ui
        self.session        = None
        self.audio_in_queue = None
        self.out_queue      = None
        self._loop          = None
        self._is_speaking   = False
        self._speaking_lock = threading.Lock()
        self.wa_reader      = WhatsAppMessageReader(ui)

        self.ui.on_text_command  = self._on_text_command
        self.ui.on_pause_toggle  = self._on_pause_toggle
        self.ui.on_effects_state_change = self._on_effects_state_change
        self._paused             = False

    def _on_pause_toggle(self, paused: bool):
        self._paused = paused

    def _on_effects_state_change(self, enabled: bool):
        pass

    def _on_text_command(self, text: str):
        if self._paused:
            return
        
        # WEB'DEN GELEN KOMUTLARI DA İŞLE
        system_response = process_system_command(text, self.wa_reader)
        if system_response:
            self.ui.write_log(f"Siz: {text}")
            self.ui.write_log(f"KUDUKOMUZİKYAPİMASİSTANAL: {system_response}")
            self.ui.set_state("LISTENING")
            response_queue.put(system_response)
            set_web_status("LISTENING")
            return
        
        self.ui.write_log(f"Siz: {text}")
        if not self._loop or not self.session:
            self.ui.write_log("ERR: KUDUKOMUZİKYAPİMASİSTANAL bağlantısı henüz hazır değil.")
            return
        asyncio.run_coroutine_threadsafe(
            self.session.send_client_content(
                turns={"parts": [{"text": text}]},
                turn_complete=True
            ),
            self._loop
        )

    async def _interrupt_audio(self):
        try:
            if self.audio_in_queue:
                while not self.audio_in_queue.empty():
                    try:
                        self.audio_in_queue.get_nowait()
                    except:
                        break
            if self.session:
                await self.session.send_realtime_input(audio_stream_end=True)
            self.set_speaking(False)
        except:
            pass

    def set_speaking(self, value: bool):
        with self._speaking_lock:
            self._is_speaking = value
        if value:
            self.ui.set_state("SPEAKING")
            set_web_status("SPEAKING")
        else:
            self.ui.set_state("LISTENING")
            set_web_status("LISTENING")

    def _build_config(self) -> types.LiveConnectConfig:
        memory = load_memory()
        mem_str = format_memory_for_prompt(memory)
        sys_p = load_system_prompt()
        now = datetime.datetime.now()
        time_ctx = f"[ŞU ANKİ ZAMAN]\n{now.strftime('%A, %d %B %Y — %H:%M')}\n\n"
        parts = [time_ctx]
        if mem_str:
            parts.append(mem_str + "\n\n")
        parts.append(sys_p)
        return types.LiveConnectConfig(
            response_modalities=["AUDIO"],
            output_audio_transcription={},
            input_audio_transcription={},
            system_instruction="\n".join(parts),
            tools=[{"function_declarations": TOOL_DECLARATIONS}],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=str(get_app_config_value("voice", "Charon") or "Charon")
                    )
                )
            ),
        )

    async def _execute_tool(self, fc) -> types.FunctionResponse:
        name = fc.name
        args = dict(fc.args or {})
        print(f"[KUDUKOMUZİKYAPİMASİSTANAL] 🔧 {name} {args}")
        self.ui.set_state("THINKING")
        set_web_status("THINKING")

        if name == "handle_system_command":
            command_text = args.get("command", "")
            result = process_system_command(command_text, self.wa_reader)
            if result is None:
                result = "Komut anlaşılamadı. 'komutlar' yazarak tüm komutları görebilirsiniz."
            response_queue.put(result)
            return types.FunctionResponse(id=fc.id, name=name, response={"result": result})

        loop = asyncio.get_event_loop()
        result = "Tamam."

        try:
            if name == "open_app":
                r = await loop.run_in_executor(None, lambda: open_app(args.get("app_name", "")))
                result = r or f"{args.get('app_name')} açıldı."
            elif name == "close_app":
                r = await loop.run_in_executor(None, lambda: close_app(args.get("app_name", ""), args.get("force", False)))
                result = r
            elif name == "close_all_apps":
                except_str = args.get("except_apps", "")
                except_list = [x.strip() for x in except_str.split(',') if x.strip()] if except_str else []
                r = await loop.run_in_executor(None, lambda: close_all_apps(except_list))
                result = r
            elif name == "wifi_control":
                r = await loop.run_in_executor(None, lambda: wifi_control(args.get("action", "status")))
                result = r
            elif name == "bluetooth_control":
                r = await loop.run_in_executor(None, lambda: bluetooth_control(args.get("action", "status")))
                result = r
            elif name == "sys_info":
                r = await loop.run_in_executor(None, lambda: sys_info(args.get("query", "all")))
                result = r or "Bilgi alındı."
            elif name == "get_weather":
                r = await loop.run_in_executor(None, lambda: get_weather_summary(args.get("location") or None))
                result = r or "Hava durumu bilgisi alindi."
            elif name == "send_whatsapp_message":
                r = await loop.run_in_executor(None, lambda: send_whatsapp_message(
                    args.get("message", ""), args.get("phone_number", ""),
                    args.get("recipient_name", ""), bool(args.get("send_now", False)),
                    args.get("app_target", "auto")))
                result = r
            elif name == "save_whatsapp_contact":
                r = await loop.run_in_executor(None, lambda: save_whatsapp_contact(
                    args.get("display_name", ""), args.get("phone_number", ""), args.get("aliases", "")))
                result = r
            elif name == "whatsapp_call":
                r = await loop.run_in_executor(None, lambda: call_whatsapp(
                    args.get("recipient_name", ""), args.get("phone_number", ""), video_call=False))
                result = r
            elif name == "whatsapp_video_call":
                r = await loop.run_in_executor(None, lambda: call_whatsapp(
                    args.get("recipient_name", ""), args.get("phone_number", ""), video_call=True))
                result = r
            else:
                result = f"Bilinmeyen araç: {name}"
        except Exception as e:
            result = f"Hata: {e}"
            traceback.print_exc()

        response_queue.put(result)
        return types.FunctionResponse(id=fc.id, name=name, response={"result": result})

    async def _send_realtime(self):
        while True:
            msg = await self.out_queue.get()
            await self.session.send_realtime_input(media=msg)

    async def _listen_audio(self):
        print("[KUDUKOMUZİKYAPİMASİSTANAL] 🎤 Mikrofon başladı")
        stream = await asyncio.to_thread(
            pya.open, format=FORMAT, channels=CHANNELS,
            rate=SEND_SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE,
        )
        try:
            while True:
                data = await asyncio.to_thread(stream.read, CHUNK_SIZE, exception_on_overflow=False)
                with self._speaking_lock:
                    jarvis_speaking = self._is_speaking
                if not jarvis_speaking and not self.ui.muted and not self._paused:
                    await self.out_queue.put({"data": data, "mime_type": "audio/pcm"})
        except Exception as e:
            print(f"[KUDUKOMUZİKYAPİMASİSTANAL] ❌ Mikrofon: {e}")
            raise
        finally:
            stream.close()

    async def _receive_audio(self):
        print("[KUDUKOMUZİKYAPİMASİSTANAL] 👂 Alım başladı")
        out_buf = []
        try:
            while True:
                async for response in self.session.receive():
                    if response.data:
                        self.audio_in_queue.put_nowait(response.data)
                    if response.server_content:
                        sc = response.server_content
                        if sc.output_transcription and sc.output_transcription.text:
                            self.set_speaking(True)
                            raw_txt = sc.output_transcription.text.strip()
                            if raw_txt:
                                txt = " ".join(raw_txt.split())
                                if txt:
                                    out_buf.append(txt)
                        if sc.turn_complete:
                            self.set_speaking(False)
                            full_out = " ".join(out_buf).strip()
                            if full_out:
                                self.ui.write_log(f"KUDUKOMUZİKYAPİMASİSTANAL: {full_out}")
                                response_queue.put(full_out)
                            out_buf = []
                    if response.tool_call:
                        fn_responses = []
                        for fc in response.tool_call.function_calls:
                            print(f"[KUDUKOMUZİKYAPİMASİSTANAL] 📞 {fc.name}")
                            fr = await self._execute_tool(fc)
                            fn_responses.append(fr)
                        await self.session.send_tool_response(function_responses=fn_responses)
        except Exception as e:
            print(f"[KUDUKOMUZİKYAPİMASİSTANAL] ❌ Alım: {e}")
            traceback.print_exc()
            raise

    async def _play_audio(self):
        print("[KUDUKOMUZİKYAPİMASİSTANAL] 🔊 Ses çalma başladı")
        stream = await asyncio.to_thread(
            pya.open, format=FORMAT, channels=CHANNELS,
            rate=RECV_SAMPLE_RATE, output=True,
        )
        try:
            while True:
                chunk = await self.audio_in_queue.get()
                self.set_speaking(True)
                await asyncio.to_thread(stream.write, chunk)
        except Exception as e:
            print(f"[KUDUKOMUZİKYAPİMASİSTANAL] ❌ Ses: {e}")
            raise
        finally:
            self.set_speaking(False)
            stream.close()

    async def run(self):
        client = genai.Client(api_key=get_api_key(), http_options={"api_version": "v1alpha"})
        while True:
            if self._paused:
                await asyncio.sleep(1)
                continue
            try:
                print("[KUDUKOMUZİKYAPİMASİSTANAL] 🔌 Bağlanıyor...")
                self.ui.set_state("THINKING")
                set_web_status("THINKING")
                config = self._build_config()
                async with (
                    client.aio.live.connect(model=LIVE_MODEL, config=config) as session,
                    asyncio.TaskGroup() as tg,
                ):
                    self.session = session
                    self._loop = asyncio.get_event_loop()
                    self.audio_in_queue = asyncio.Queue()
                    self.out_queue = asyncio.Queue(maxsize=10)
                    print("[KUDUKOMUZİKYAPİMASİSTANAL] ✅ Bağlandı.")
                    self.ui.set_state("LISTENING")
                    set_web_status("LISTENING")
                    self.ui.write_log("SYS: KUDUKOMUZİKYAPİMASİSTANAL hazır. Dinliyorum...")
                    tg.create_task(self._send_realtime())
                    tg.create_task(self._listen_audio())
                    tg.create_task(self._receive_audio())
                    tg.create_task(self._play_audio())
            except Exception as e:
                print(f"[KUDUKOMUZİKYAPİMASİSTANAL] ⚠️ {e}")
                traceback.print_exc()
                self.set_speaking(False)
                self.ui.write_log(f"ERR: Bağlantı kesildi — {e}")
                self.ui.set_state("ERROR")
                set_web_status("ERROR")
                await asyncio.sleep(3)

# WEB KOMUT DİNLEYİCİ FONKSİYONU
def web_command_listener(jarvis):
    while True:
        try:
            # Güncellenmiş: command_queue artık (request_id, command) tuple'ı alıyor
            item = command_queue.get(timeout=0.5)
            if isinstance(item, tuple) and len(item) == 2:
                request_id, cmd = item
            else:
                cmd = item
                request_id = None
            
            if cmd:
                set_web_status("THINKING")
                if jarvis._loop and jarvis.session:
                    asyncio.run_coroutine_threadsafe(
                        jarvis.session.send_client_content(
                            turns={"parts": [{"text": cmd}]},
                            turn_complete=True
                        ),
                        jarvis._loop
                    )
        except:
            pass

def main():
    if os.environ.get("TERM_PROGRAM") == "vscode":
        print("[KUDUKOMUZİKYAPİMASİSTANAL] VS Code icinden baslatildi.")

    ui = JarvisUI()
    
    # WEB SUNUCUSUNU BAŞLAT - Güncellenmiş
    web_thread = threading.Thread(target=lambda: start_web_server(port=5000, open_browser=True, use_main_processor=True), daemon=True)
    web_thread.start()
    print("🌐 Web arayüzü http://localhost:5000 adresinde çalışıyor")

    def runner():
        ui.wait_for_api_key()
        jarvis = JarvisLive(ui)
        
        # Web komutlarını dinleyen thread
        listener_thread = threading.Thread(target=web_command_listener, args=(jarvis,), daemon=True)
        listener_thread.start()
        
        try:
            asyncio.run(jarvis.run())
        except KeyboardInterrupt:
            print("\n🔴 Kapatılıyor...")
            if hasattr(jarvis, 'wa_reader'):
                jarvis.wa_reader.stop_monitoring()

    threading.Thread(target=runner, daemon=True).start()
    ui.root.mainloop()

if __name__ == "__main__":
    main()