#!/usr/bin/env python3
"""
KUDUKOMUZİKYAPİMASİSTANAL Web Sunucusu - Hızlı AJAX Versiyonu
"""

import threading
import webbrowser
import queue
import time
from flask import Flask, render_template_string, request, jsonify

# Web arayüzü HTML kodu - Arayüz yukarı çekildi ve ortalandı
WEB_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>KUDUKOMUZİKYAPİMASİSTANAL - Web Asistan</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            display: flex;
            align-items: center; /* İçeriği ortala - dikeyde ortalama */
            justify-content: center; /* Yatayda ortalama */
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            width: 100%;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.2);
            animation: slideUp 0.5s ease;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        
        @keyframes slideUp {
            from { transform: translateY(50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            text-align: center;
            color: white;
        }
        
        .header h1 { font-size: 1.5rem; margin-bottom: 5px; }
        .header p { font-size: 0.8rem; opacity: 0.9; }
        
        .status-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 20px;
            background: rgba(0, 0, 0, 0.3);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .status {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #ffc107;
            transition: all 0.3s ease;
        }
        
        .status-dot.listening { background: #4caf50; box-shadow: 0 0 10px #4caf50; }
        .status-dot.speaking { background: #2196f3; box-shadow: 0 0 10px #2196f3; }
        .status-dot.thinking { background: #ff9800; box-shadow: 0 0 10px #ff9800; }
        .status-dot.error { background: #f44336; box-shadow: 0 0 10px #f44336; }
        
        .status-text { color: white; font-size: 0.9rem; }
        
        .chat-container {
            height: 400px;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .chat-container::-webkit-scrollbar { width: 6px; }
        .chat-container::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.1); border-radius: 3px; }
        .chat-container::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.3); border-radius: 3px; }
        
        .message {
            display: flex;
            animation: fadeIn 0.3s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .message.user { justify-content: flex-end; }
        .message.assistant { justify-content: flex-start; }
        
        .message-content {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 20px;
            word-wrap: break-word;
        }
        
        .message.user .message-content {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 5px;
        }
        
        .message.assistant .message-content {
            background: rgba(255, 255, 255, 0.15);
            color: white;
            border-bottom-left-radius: 5px;
        }
        
        .input-area {
            padding: 20px;
            background: rgba(0, 0, 0, 0.3);
            display: flex;
            gap: 10px;
        }
        
        .input-area input {
            flex: 1;
            padding: 12px 18px;
            border: none;
            border-radius: 25px;
            background: rgba(255, 255, 255, 0.15);
            color: white;
            font-size: 1rem;
            outline: none;
        }
        
        .input-area input::placeholder { color: rgba(255, 255, 255, 0.6); }
        
        .input-area button {
            padding: 12px 24px;
            border: none;
            border-radius: 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            cursor: pointer;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        .input-area button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 0.6s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* Telefon için özel stiller */
        @media (max-width: 600px) {
            body { 
                padding: 10px;
                align-items: center;
            }
            .container {
                border-radius: 20px;
                margin: 0;
            }
            .chat-container { 
                height: 350px;
                padding: 15px;
            }
            .message-content { 
                max-width: 85%; 
                font-size: 0.9rem;
                padding: 10px 14px;
            }
            .header h1 { font-size: 1.2rem; }
            .header p { font-size: 0.7rem; }
            .status-bar { padding: 10px 15px; }
            .input-area { padding: 15px; }
            .input-area input { padding: 10px 15px; font-size: 0.9rem; }
            .input-area button { padding: 10px 20px; font-size: 0.9rem; }
        }
        
        /* Daha büyük ekranlar için */
        @media (min-width: 601px) and (max-width: 900px) {
            .container {
                margin: 0 auto;
                border-radius: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 KUDUKOMUZİKYAPİMASİSTANAL</h1>
            <p>Just A Rather Very Intelligent System</p>
        </div>
        
        <div class="status-bar">
            <div class="status">
                <div class="status-dot" id="statusDot"></div>
                <span class="status-text" id="statusText">Hazır</span>
            </div>
            <button class="mic-btn" id="micBtn" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none; width: 40px; height: 40px; border-radius: 50%; cursor: pointer; color: white; font-size: 18px;">🎤</button>
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div class="message assistant">
                <div class="message-content">
                    Merhaba! Ben KUDUKOMUZİKYAPİMASİSTANAL.<br>
                    Size nasıl yardımcı olabilirim?<br>
                    <small style="opacity:0.7;">💡 "komutlar" yazarak tüm komutları görebilirsiniz</small>
                </div>
            </div>
        </div>
        
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="Mesajınızı yazın..." autocomplete="off">
            <button id="sendBtn">Gönder</button>
        </div>
    </div>
    
    <script>
        const chatContainer = document.getElementById('chatContainer');
        const messageInput = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendBtn');
        const micBtn = document.getElementById('micBtn');
        const statusDot = document.getElementById('statusDot');
        const statusText = document.getElementById('statusText');
        
        let isWaiting = false;
        let pendingRequest = null;
        
        function updateStatus(status) {
            statusDot.className = 'status-dot';
            switch(status) {
                case 'listening':
                    statusDot.classList.add('listening');
                    statusText.textContent = 'Dinleniyor...';
                    break;
                case 'speaking':
                    statusDot.classList.add('speaking');
                    statusText.textContent = 'Konuşuyor...';
                    break;
                case 'thinking':
                    statusDot.classList.add('thinking');
                    statusText.textContent = 'Düşünüyor...';
                    break;
                case 'error':
                    statusDot.classList.add('error');
                    statusText.textContent = 'Hata!';
                    break;
                default:
                    statusText.textContent = 'Hazır';
            }
        }
        
        function addMessage(text, isUser) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.innerHTML = text.replace(/\\\\n/g, '<br>');
            messageDiv.appendChild(contentDiv);
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        function showLoading() {
            isWaiting = true;
            const loadingDiv = document.createElement('div');
            loadingDiv.id = 'loadingIndicator';
            loadingDiv.className = 'message assistant';
            loadingDiv.innerHTML = '<div class="message-content"><div class="loading"></div> Yanıt bekleniyor...</div>';
            chatContainer.appendChild(loadingDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        function hideLoading() {
            isWaiting = false;
            const loading = document.getElementById('loadingIndicator');
            if (loading) loading.remove();
        }
        
        async function sendCommand(cmd) {
            if (!cmd.trim() || isWaiting) return;
            
            addMessage(cmd, true);
            messageInput.value = '';
            showLoading();
            updateStatus('thinking');
            
            if (pendingRequest) {
                pendingRequest.abort();
            }
            
            const controller = new AbortController();
            pendingRequest = controller;
            
            const timeoutId = setTimeout(() => {
                controller.abort();
                hideLoading();
                addMessage('❌ Zaman aşımı: Sunucu yanıt vermiyor.', false);
                updateStatus('error');
                setTimeout(() => updateStatus('listening'), 3000);
                pendingRequest = null;
            }, 15000);
            
            try {
                const response = await fetch('/command', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ command: cmd }),
                    signal: controller.signal
                });
                
                clearTimeout(timeoutId);
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                
                const data = await response.json();
                hideLoading();
                addMessage(data.response, false);
                updateStatus('listening');
            } catch (error) {
                clearTimeout(timeoutId);
                if (error.name === 'AbortError') {
                    return;
                }
                hideLoading();
                addMessage('❌ Bağlantı hatası: ' + error.message, false);
                updateStatus('error');
                setTimeout(() => updateStatus('listening'), 3000);
            } finally {
                if (pendingRequest === controller) {
                    pendingRequest = null;
                }
            }
        }
        
        function startVoiceRecognition() {
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                addMessage('❌ Tarayıcınız sesli komut desteklemiyor.', false);
                return;
            }
            
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognition = new SpeechRecognition();
            recognition.lang = 'tr-TR';
            recognition.continuous = false;
            recognition.interimResults = false;
            
            recognition.onstart = () => {
                micBtn.style.background = '#f44336';
                addMessage('🎤 Dinleniyor...', false);
            };
            
            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                sendCommand(transcript);
            };
            
            recognition.onerror = (event) => {
                console.error('Ses hatası:', event.error);
                addMessage(`❌ Ses hatası: ${event.error}`, false);
                micBtn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
            };
            
            recognition.onend = () => {
                micBtn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
            };
            
            recognition.start();
        }
        
        async function fetchStatus() {
            try {
                const response = await fetch('/status');
                const data = await response.json();
                updateStatus(data.status);
            } catch (error) {
                console.error('Status fetch error:', error);
            }
        }
        
        sendBtn.addEventListener('click', () => sendCommand(messageInput.value));
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendCommand(messageInput.value);
        });
        micBtn.addEventListener('click', startVoiceRecognition);
        
        setInterval(fetchStatus, 2000);
        fetchStatus();
        
        // Sayfa yüklendiğinde input'a odaklan
        messageInput.focus();
    </script>
</body>
</html>
"""

# Queue'lar
command_queue = queue.Queue()
response_queue = queue.Queue()
request_id_counter = 0
request_lock = threading.Lock()
pending_responses = {}  # request_id -> queue

app = Flask(__name__)
web_status = "listening"

def set_web_status(status):
    global web_status
    web_status = status

@app.route('/')
def index():
    return render_template_string(WEB_HTML)

@app.route('/command', methods=['POST'])
def handle_command():
    """Web'den gelen komutu işler"""
    global request_id_counter
    
    data = request.get_json()
    command = data.get('command', '').strip()
    
    if not command:
        return jsonify({'response': 'Komut boş olamaz.'})
    
    # Benzersiz request ID oluştur
    with request_lock:
        request_id = request_id_counter
        request_id_counter += 1
    
    # Bu request için queue oluştur
    pending_responses[request_id] = queue.Queue()
    
    # Komutu ID ile birlikte gönder
    command_queue.put((request_id, command))
    
    # Yanıt bekle (15 saniye timeout)
    try:
        response = pending_responses[request_id].get(timeout=15)
        return jsonify({'response': response})
    except queue.Empty:
        return jsonify({'response': '⚠️ Zaman aşımı: Asistan yanıt vermiyor.'})
    finally:
        if request_id in pending_responses:
            del pending_responses[request_id]

@app.route('/status')
def get_status():
    return jsonify({'status': web_status})

def process_response_forwarder():
    """response_queue'daki yanıtları ilgili request'lere yönlendirir"""
    while True:
        try:
            response = response_queue.get(timeout=0.5)
            if response:
                # Not: Bu basit versiyonda response'u tüm bekleyenlere gönderiyoruz
                # Daha gelişmiş versiyon için request_id eşleştirmesi yapılabilir
                for req_id, q in list(pending_responses.items()):
                    try:
                        q.put(response)
                    except:
                        pass
        except:
            pass

def start_web_server(port=5000, open_browser=True, use_main_processor=False):
    """Web sunucusunu başlatır"""
    print(f"\n🌐 Web sunucusu başlatılıyor...")
    print(f"📍 Adres: http://localhost:{port}")
    print(f"📱 Telefonunuzdan bağlanmak için: http://[BILGISAYAR_IP]:{port}")
    print("=" * 50)
    
    # Yanıt yönlendirici thread'i başlat
    forwarder_thread = threading.Thread(target=process_response_forwarder, daemon=True)
    forwarder_thread.start()
    
    if open_browser:
        webbrowser.open(f"http://localhost:{port}")
    
    # Flask'ı başlat
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False, threaded=True)

if __name__ == "__main__":
    start_web_server()