import requests, time
from bs4 import BeautifulSoup

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '48',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'iportal.ntnu.edu.tw',
    'Origin': 'https://iportal.ntnu.edu.tw',
    'Referer': 'https://iportal.ntnu.edu.tw/ntnu/',
    'Sec-Ch-Ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
}

account = {'muid': '',
          'mpassword': '',
          'forceMobile': 'pc'}
cookies = ''
domain = 'https://iportal.ntnu.edu.tw/'
url = domain + 'login.do'

fp = open("log.txt", "a", encoding='utf8')

""" 登入 """
r = requests.post(url, headers=headers, data=account)
if r.status_code != requests.codes.ok:
    print("Login Failse:", r.status_code)
    print(r.raise_for_status())
    fp.write("Login Failse:", r.status_code)
    fp.write(r.raise_for_status())
    fp.close()
    exit()
print("Login Success")
fp.write("Login Success: " + str(r.status_code) + "\n")
cookies = r.cookies.get_dict()

""" 進校網 """
# time.sleep(1)
headers['Referer'] = url
# url = domain + 'myPortal.do'
index = r.text.find('myPortal.do?thetime=')
t = r.text[index+20:index+33]
url = domain + r.text[index:index+33]
# params = {'thetime': t}
r = requests.get(url, headers=headers, cookies=cookies)
if r.status_code != requests.codes.ok:
    print("Enter School Web Failse:", r.status_code)
    print(r.raise_for_status())
    fp.write("Enter School Web Failse:", r.status_code + '\n')
    fp.write(r.raise_for_status())
    fp.close()
    exit()
print("Enter School Web Success")
fp.write("Enter School Web Success: " + str(r.status_code) + "\n")

""" 進琴房 """
headers['Sec-Fetch-Site'] = 'none'
url = domain + 'ssoIndex.do?apUrl=https://pms.itc.ntnu.edu.tw/BookMeApp/BookMe1010Ctrl?action=doLogin&apOu=Practice_Piano_Room_Booking&sso=true&datetime1='+t
r = requests.get(url, cookies=cookies)
if r.status_code != requests.codes.ok:
    print("Enter Booking Web (1/2) Failse:", r.status_code)
    print(r.raise_for_status())
    fp.write("Enter Booking Web (1/2) Failse:", r.status_code + '\n')
    fp.write(r.raise_for_status())
    fp.close()
    exit()
print("Enter Booking Web (1/2) Success")
fp.write("Enter Booking Web (1/2) Success: " + str(r.status_code) + "\n")

""" 進琴房 (2/2) """
domain = 'https://pms.itc.ntnu.edu.tw/'
url = domain + 'BookMeApp/BookMe1010Ctrl?action=doLogin'
# 取得data
index1 = r.text.find("sessionId' value='")
index2 = r.text.find("'>\n<input type='hidden' name='userid")
sessionId = r.text[index1+18:index2]
userid = '41047023S'
data = {'sessionId': sessionId, 'userid': userid}
r = requests.post(url, headers=headers, data=data, cookies=cookies)
if r.status_code != requests.codes.ok:
    print("Enter Booking Web (2/2) Failse:", r.status_code)
    print(r.raise_for_status())
    fp.write("Enter Booking Web (2/2) Failse:", r.status_code + '\n')
    fp.write(r.raise_for_status())
    fp.close()
    exit()
print("Enter Booking Web (2/2) Success")
fp.write("Enter Booking Web (2/2) Success: " + str(r.status_code) + "\n")
cookkies = r.cookies.get_dict

# 觀察response
with open("response.txt", 'w', encoding='utf8') as fp2:
    soup = BeautifulSoup(r.text, 'lxml')
    fp2.write(soup.prettify())
# 

fp.close()