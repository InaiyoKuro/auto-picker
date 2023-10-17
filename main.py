try:
    import sys, os, json,time
    import requests
    from tkinter import messagebox
    import psutil
except:
    os.system('pip install requests')
    os.system('pip install psutil')
import requests
import psutil

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable the warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# url = 'https://riot:<pass>@127.0.0.1:54680/lol-champions/v1/owned-champions-minimal'

LC = 'LeagueClientUx.exe'
LOL = 'League of Legends.exe'

def check_process_exists(process_name):
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.info['name'] == process_name:
            return process.info['pid']
    return False

def get_process_directory(pid):
    try:
        process = psutil.Process(pid)
        return process.cwd()
    except psutil.NoSuchProcess:
        return None



PIDLOL = check_process_exists(LOL)

if PIDLOL:
    messagebox.showinfo("Thông con báo","Bạn đã vào game rồi!")
    sys.exit()

PID = check_process_exists(LC)

if not PID:
    messagebox.showinfo("Thông con báo","Mở game lên đi bạn êii")
    sys.exit()

path = get_process_directory(PID)
lockfile = f"{path}\\lockfile"
with open(lockfile,'r') as file:
    content = file.read().split(":")

Port = content[2]
Pass = content[3]

host = f'https://riot:{Pass}@127.0.0.1'


# 1. GET   /lol-champions/v1/owned-champions-minimal | Xem tướng đã sở hữu và miễn phí
# 2. GET   /lol-matchmaking/v1/ready-check
# 3. POST  /lol-matchmaking/v1/ready-check/accept
# 4. GET   /lol-champ-select/v1/session
# 5. PATCH /lol-champ-select/v1/session/actions/{id}
# 6. POST  /lol-champ-select/v1/session/actions/{id}/complete
def getAPI(n):
    api = [
        '/lol-champions/v1/owned-champions-minimal',
        '/lol-matchmaking/v1/ready-check',
        '/lol-matchmaking/v1/ready-check/accept',
        '/lol-champ-select/v1/session',
        '/lol-champ-select/v1/session/actions/',
    ]
    return f"{host}:{Port}{api[n]}"

def request(url, method = "GET", data = None):
    data = requests.request(method, url ,verify = False, headers={ 'Content-type': 'application/json; charset=UTF-8' }, data=data)
    return data

def isMatchFound():
    res = request(getAPI(1))
    data = json.loads(res.text)

    if res.status_code == 200:
        return data["state"]
        # if data["state"] == "InProgress":

def acceptMatch():
    request(getAPI(2), 'POST')

def getActionId():
    res = request(getAPI(3))
    
    if res.status_code != 200:
        return
    
    data = json.loads(res.text)

    localPlayerCellId = data["localPlayerCellId"]
    actions = data["actions"][0]
    for action in actions:
        if action["actorCellId"] == localPlayerCellId:
            return action["id"]

def pick(id, championId):
    requests.patch(f"{getAPI(4)}{id}",verify=False, json={ "championId": championId })
    return True
def lock(id):
    res = request(f"{getAPI(4)}{id}/complete", "POST")
    if res.status_code == 400 or res.status_code == 404:
        return False
    else: 
        return True
    

def GetChampionsList():
    list_champions = []
    res = request(getAPI(0))
    data = json.loads(res.text)
    for champion in data:
        list_champions.append({ "name": champion['name'], "id": champion["id"]})
    return list_champions

# running = True
# while running:
#     if not PID:
#         print("Mở game lên đi bạn êi")
#         break

#     check = isMatchFound()
#     # data = json.loads(check)
#     print(check)
            