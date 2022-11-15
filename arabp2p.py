import os
import sys
import requests
from bs4 import BeautifulSoup
import json
import time
from selfupdate import update
update()
basicHeaders = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Origin': 'https://www.arabp2p.net',
    'Referer': 'https://www.arabp2p.net/index.php',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"'}

os.system("")

# DEFINE SOME COLORS
NORMAL = '\x1b[0m'
RED = '\x1b[1;31;40m'
GREEN = '\x1b[1;32;40m'
YELLOW = '\x1b[1;33;40m'
BLUE = '\x1b[1;34;40m'
WHITE = '\x1b[1;55;40m'
PURPLE = '\x1b[1;35;40m'

def getAccount():
	# IF FOLDER DOES NOT EXIST 
	if not os.path.exists("config"):
		os.makedirs("config")
	# IF ACCOUNT FILE DOES NOT EXISTS OR ACCOUNT, THEN ASK HIM TO ADD HIS ACCOUNT
	if not os.path.exists("config/account.txt") or open("config/account.txt", "r").read()=="":
		email = input("Add Your Email: ")
		pwd = input("Add Your Password: ")
		with open("config/account.txt", "w") as f:
			f.write(f"{email}:{pwd}")
		print(f"{GREEN}Your Account Added Successfully{NORMAL}")
	# IF ACCOUNT EXISTS THEN READ IT
	else:
		acc = open("config/account.txt", "r").read()
		email = acc.split(":")[0]
		pwd = acc.split(":")[1]
	return email, pwd


def checkAccount(email, pwd):
	"""
	Here I Just Check The Account;
	If It's True It will pass
	And If It's False The Script Will Exit!
	"""
	global headers

	r = requests.post("https://www.arabp2p.net/index.php", headers=basicHeaders, params={'page': 'login'}, data={'uid': email,'pwd': pwd})
	headers = r.request.headers
	if r.status_code == 200:
		print(f"{GREEN}Your Account Is Valid{NORMAL}")
		soup = BeautifulSoup(r.content,"html.parser")
		return soup
	else:
		sys.exit(f"{RED}! Check Your Email/Password !{NORMAL}")


def getAccountInfo(soup):
	for a in soup.find_all("a"):
		if 'userdetails' in str(a['href']):
			userId = a['href'].split("=")[-1]
			myProfile = "https://www.arabp2p.net/"+a['href']
			break
	
	soup = BeautifulSoup(requests.get(myProfile, headers=headers).content, "html.parser").find("table", {"class":"userinfo"})
	info = {}
	for tr in soup.find_all("tr", {"class":"torrent"}):
		if "التوقيع" in str(tr):
			break
		if "اسم المستخدم" in str(tr):
			info['userName'] = tr.get_text().split("اسم المستخدم")[1].split("\n")[1].replace(" ", "")
		elif "الرتبة"  in str(tr):
			info['rank'] = tr.get_text().split("الرتبة")[1].split("\n")[1].replace(" ", "")
		elif "حمل" in str(tr):
			info['downlaod'] = tr.get_text().split("حمل")[1].split("\n")[1].replace("  ", "")
		elif "رفع" in str(tr):
			info['upload'] = tr.get_text().split("رفع")[1].split("\n")[1].replace(" ", "")
		elif "النقاط" in str(tr):
			info['points'] = tr.get_text().split("النقاط")[1].split("\n")[1].replace(" ", "")
		else:
			continue
			

	print(f"{YELLOW}{info['userName']} {info['rank']}  ⬆ {info['downlaod']}  ⬇ {info['upload']}  ✴ {info['points']}{NORMAL}")
	return userId, info['userName'], info['points']

def getSupporters():
	
	r = json.loads(requests.get("https://pastebin.com/raw/McnpyYGx").text)
	if len(r) != 0:
		print(f"{RED}# SUPPORTERS MEMBERS #{NORMAL}")
		for i in r.items():
			print(f"{GREEN}{i[0]} : {i[1]} Points{NORMAL}")
		thanks  = "THANK YOU GUYS\n"
		for l in thanks:
			sys.stdout.write(l)
			sys.stdout.flush()
			time.sleep(0.2)
		time.sleep(2)
		os.system("clear")

def sayThanks(latestTorrent):
	for id in latestTorrent:
		id = id.split("=")[-1]
		data = {'tid': str(id),'thanks': '1','rndval': '1668350638337'}
		r = requests.post('https://www.arabp2p.net/thanks.php', headers=headers, data=data)
		if r.status_code == 200:
			print(f"\r{GREEN}ID [{id}] Done Succeffully{NORMAL}", end="\r")
		else:
			print(f"{RED}! Something Went Wrong !{NORMAL}")
	

def getNewMessages(soup):
	newMessages = soup.find("span", {"class":"msgs_alart"}).text
	if newMessages == "":
		newMessages = 0
	else:
		newMessages = int(newMessages)
	return newMessages


def donate(points, userName):
	print(f"{YELLOW}You Have {points} Points {NORMAL}")
	points = input("How Many Points Would You Send To Me?: ")
	if not points.isdigit():
		print("! You Can Only Add Numbers !")
		return False
	params = {
		'page': 'userdetails',
		'id': '91413',
		'tab': '13',
	}

	data = {
		'points': str(points),
		'user_msg': '',
		'submit': 'ارسال',
	}

	response = requests.post('https://www.arabp2p.net/index.php', params=params, headers=headers, data=data)
	if response.status_code == 200:
		print(f"You Have Sent {points} Points To Me\n Thanks {userName}")
		return True
	else:
		return False


def getLatestTorrents():
	latestTorrent = []
	r = requests.get("https://www.arabp2p.net/index.php?page=torrents", headers=headers)
	soup = BeautifulSoup(r.content, "html.parser")
	for a in soup.find_all('a', {"class":"screenshot"}):
		latestTorrent.append("https://www.arabp2p.net/"+a['href'])
	return latestTorrent


getSupporters()

email, pwd = getAccount()
print("Let's Check Your Account...Please Wait!")
soup = checkAccount(email, pwd)
userId, userName, points = getAccountInfo(soup)
print(f"""
 [1] Upload New Torrent
 [2] Say Thanks For Latest Torrent
 [3] Donate Me With Points
""")
choose = input("Choose: ")
if choose == "1":
	pass
elif choose == "2":
	latestTorrent = getLatestTorrents()
	sayThanks(latestTorrent)
	os.system("clear")
	print(f"You Sent Thanks For {len(latestTorrent)} Torrents")
elif choose == "3":
	state = donate(points, userName)
	if state == False:
		print("! SomeThing Went Wrong !")
else:
	sys.exit("! Incorrect Choice !")





#sayThanks()
