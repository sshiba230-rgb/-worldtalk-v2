from flask import Flask, request, jsonify, render_template_string
import time
app = Flask(__name__)
messages = [{"name": "WorldTalk 🌍", "text": "Welcome! LIVE from Pretoria 🇿🇦 Type anything!", "time": time.time()}]
HTML = """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><title>WorldTalk V2</title><style>body{margin:0;font-family:sans-serif;background:#e5ddd5;display:flex;flex-direction:column;height:100vh}.top{background:#0A66C2;color:white;padding:14px;font-weight:bold;text-align:center} .bubble{background:white;padding:10px 14px;border-radius:18px;margin:8px;max-width:80%;box-shadow:0 1px 1px #0002}#chat{flex:1;overflow:auto;padding:12px;padding-bottom:90px;max-width:700px;margin:auto;width:100%} .bar{position:fixed;bottom:0;left:0;right:0;background:#f0f0f0;display:flex;padding:10px;gap:6px} .bar input{border:none;border-radius:25px;padding:12px 16px;outline:none}#name{width:80px}#msg{flex:1} .bar button{background:#0A66C2;color:white;border:none;border-radius:25px;padding:12px 20px;font-weight:bold}</style></head><body><div class="top">🌍 WorldTalk V2 — LIVE CHAT</div><div id="chat"></div><div class="bar"><input id="name" placeholder="Name"><input id="msg" placeholder="Message..."><button onclick="send()">Send</button></div><script>let last=0;async function load(){let r=await fetch('/messages');let m=await r.json();if(m.length==last)return;last=m.length;let c=document.getElementById('chat');c.innerHTML='';m.forEach(x=>{let d=document.createElement('div');d.className='bubble';d.innerHTML='<b style=color:#0A66C2;font-size:11px>'+x.name+'</b><br>'+x.text;c.appendChild(d)});c.scrollTop=c.scrollHeight}async function send(){let n=document.getElementById('name').value||'Anon';let t=document.getElementById('msg').value;if(!t)return;document.getElementById('msg').value='';await fetch('/send',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:n,text:t})});load()}setInterval(load,800);load();document.getElementById('msg').addEventListener('keydown',e=>{if(e.key==='Enter')send()})</script></body></html>"""
@app.route('/')
def home(): return render_template_string(HTML)
@app.route('/messages')
def msgs(): return jsonify(messages[-100:])
@app.route('/send', methods=['POST'])
def send_msg():
    d=request.json
    messages.append({"name":d['name'][:20],"text":d['text'][:300],"time":time.time()})
    if len(messages)>150: messages.pop(0)
    return jsonify({"ok":True})
if __name__ == "__main__": app.run(host="0.0.0.0", port=5000)
