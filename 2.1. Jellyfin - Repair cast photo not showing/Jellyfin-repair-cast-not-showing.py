import requests
import threading
import time

apikey = "YOUR_API"
url = "192.168.x.x:port"

us = requests.get(f"http://{url}/emby/Users?api_key={apikey}").json()
uids = ["2ab240787c354396bf36d25a910136ed"]
for u in us:
    uids.append(u["Id"])

url = f"http://{url}/emby/Persons?api_key={apikey}&enableImages=false"
ps = requests.get(url).json()["Items"]


def update_pid(pid):
    for userid in uids:
        url = f"http://{url}/Users/{userid}/Items/{pid}?api_key={apikey}"
        requests.get(url).json()["Name"]


pslen = len(ps)
count = 0
maxthreads = 5
for p in ps:
    count += 1

    while 1:
        tcount = 0
        for t in threading.enumerate():
            if t.name == "worker":
                tcount += 1

        if tcount < maxthreads:
            break

    print(f"{count}/{pslen}", p["Name"])
    time.sleep(0.1)

    pid = p["Id"]
    t = threading.Thread(target=update_pid, args=(pid,), name="worker")
    t.start()
