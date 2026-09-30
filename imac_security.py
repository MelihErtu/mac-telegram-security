#!/usr/bin/env python3
import json, os, subprocess, time, urllib.request, urllib.parse
from pathlib import Path

BASE = Path(__file__).resolve().parent
CONFIG = BASE / 'config.json'
PHOTO = Path('/tmp/mac_login.jpg')
IMAGESNAP = '/opt/homebrew/bin/imagesnap'
WAIT = 120

def config_read():
    if not CONFIG.exists():
        raise SystemExit('config.json was not found. Copy config.example.json and enter your settings.')
    cfg = json.loads(CONFIG.read_text())
    token = str(cfg.get('bot_token','')).strip()
    chat_id = str(cfg.get('chat_id','')).strip()
    if not token or not chat_id:
        raise SystemExit('bot_token and chat_id are required in config.json.')
    return token, chat_id

TOKEN, CHAT_ID = config_read()
API = f'https://api.telegram.org/bot{TOKEN}/'

def api(method, data=None):
    body = json.dumps(data or {}).encode()
    req = urllib.request.Request(API + method, data=body, headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())

def photo_take():
    subprocess.run([IMAGESNAP, '-q', str(PHOTO)], check=True)

def photo_send():
    keyboard = json.dumps({'inline_keyboard': [[
        {"text":"✅ Yes, It's Me",'callback_data':'yes'},
        {'text':'🔒 No, Lock Mac','callback_data':'lock'}
    ]]})
    boundary = '----MacSecurityBoundary'
    parts=[]
    def field(name, value):
        parts.extend([f'--{boundary}\r\n'.encode(), f'Content-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode()])
    field('chat_id', CHAT_ID); field('caption', '🔐 Your Mac was unlocked. Was this you?'); field('reply_markup', keyboard)
    parts.extend([f'--{boundary}\r\n'.encode(), b'Content-Disposition: form-data; name="photo"; filename="login.jpg"\r\n', b'Content-Type: image/jpeg\r\n\r\n', PHOTO.read_bytes(), b'\r\n', f'--{boundary}--\r\n'.encode()])
    req=urllib.request.Request(API+'sendPhoto', data=b''.join(parts), headers={'Content-Type':f'multipart/form-data; boundary={boundary}'})
    with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read().decode())

def last_update():
    try:
        res=api('getUpdates', {'limit':1,'offset':-1})
        arr=res.get('result',[])
        return arr[-1]['update_id'] if arr else 0
    except Exception: return 0

def wait_answer(last):
    end=time.time()+WAIT
    offset=last+1
    while time.time()<end:
        try:
            res=api('getUpdates', {'offset':offset,'timeout':5,'allowed_updates':['callback_query']})
            for u in res.get('result',[]):
                offset=u['update_id']+1
                cb=u.get('callback_query',{})
                msg=cb.get('message',{})
                if str(msg.get('chat',{}).get('id')) != CHAT_ID: continue
                api('answerCallbackQuery', {'callback_query_id':cb.get('id')})
                choice=cb.get('data')
                if choice=='yes':
                    print('✅ Login approved.'); return
                if choice=='lock':
                    api('sendMessage', {'chat_id':CHAT_ID,'text':'🔒 Locking Mac...'})
                    subprocess.run(['/usr/bin/osascript','-e','tell application "System Events" to keystroke "q" using {control down, command down}'])
                    return
        except Exception as e:
            print('Telegram error:', e)
            time.sleep(2)
    print('⌛ No response received.')

def main():
    try:
        photo_take(); last=last_update(); photo_send(); wait_answer(last)
    finally:
        try: PHOTO.unlink(missing_ok=True)
        except Exception: pass

if __name__=='__main__': main()
