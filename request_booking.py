import requests, time
from bs4 import BeautifulSoup

account = {'muid': '',
          'mpassword': '',
          'forceMobile': 'pc'}
""" # YYYYMMDD
roomIwant =  """
headers = {
    'Host': 'iportal.ntnu.edu.tw',
    'Referer': 'https://iportal.ntnu.edu.tw/ntnu/',
    'Sec-Ch-Ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
}
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
print(str(cookies))

""" 進校網 """
# time.sleep(1)
headers['Referer'] = url
# url = domain + 'myPortal.do'
index = r.text.find('myPortal.do?thetime=')
t = r.text[index+20:index+33]
url = domain + r.text[index:index+33] # params = {'thetime': t}
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
print(str(cookies))

""" 進琴房 (1/2) """ # 需要JSESSIONID
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
print(str(cookies))

""" 進琴房 (2/2) """ # 會給新的JSESSIONID
domain = 'https://pms.itc.ntnu.edu.tw/'
url = domain + 'BookMeApp/BookMe1010Ctrl?action=doLogin'
# 取得data
index1 = r.text.find("sessionId' value='")
index2 = r.text.find("'>\n<input type='hidden' name='userid")
sessionId = r.text[index1+18:index2]
userid = account['muid']
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
cookies = r.cookies

# Google Analytics cookies需要手動更新
cookies['_ga'] = ''
cookies['_gid'] = ''
cookies['_ga_L47EP67E8W'] = ''

""" 預約琴房 """
headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
headers['Host'] = 'pms.itc.ntnu.edu.tw'
headers['Origin'] = 'https://pms.itc.ntnu.edu.tw'
headers['Referer'] = 'https://pms.itc.ntnu.edu.tw/BookMeApp/BookMe1010Ctrl'
headers['Sec-Fetch-Dest'] = 'empty'
headers['Sec-Fetch-Mode'] = 'cors'
headers['Sec-Fetch-Site'] = 'same-origin'
headers['X-Requested-With'] = 'XMLHttpRequest'
# data = {'action': 'doBookMe', 'data': '202404303Ds05'} # (年月日 + 房號) + 時段
data = {'action': 'doGoTo1050'} # 琴房狀態
# data = {'action': 'doBookMe', 'data': 's05'} # (年月日 + 房號) + 時段

url = domain + 'BookMeApp/BookMe1010Ctrl'
# url = domain + 'BookMeApp/BookMe1050Ctrl'
r = requests.post(url, headers=headers, data=data, cookies=cookies)
print(r.text)

fp.close()