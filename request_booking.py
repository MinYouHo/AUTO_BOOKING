import requests, time

# GA cookies
ga = ''
ga_L47EP67E8W = ''
gid = ''

# 想要的琴房
room = '2C'
# 想要的時段：s + 第幾時段
section = ['s14', 's15']

# 學校帳號
account = {'muid': '',
           'mpassword': '',
           'forceMobile': ''}

headers = {
    'Host': 'iportal.ntnu.edu.tw',
    'Referer': 'https://iportal.ntnu.edu.tw/ntnu/',
    'Sec-Ch-Ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
}
cookies = ''
t = time.localtime(time.time())

fp = open("log.txt", "a", encoding='utf8')
fp.write(time.strftime('%Y/%m/%d %H:%M:%S\n',t))

""" 登入 """
domain = 'https://iportal.ntnu.edu.tw/'
url = domain + 'login.do'
r = requests.post(url, headers=headers, data=account)
if r.status_code != requests.codes.ok:
    fp.write("Login Failse:", r.status_code)
    fp.write(r.raise_for_status())
    fp.close()
    exit()
fp.write("Login Success: " + str(r.status_code) + "\n")
cookies = r.cookies.get_dict()

""" 進校網 """
# time.sleep(1)
headers['Referer'] = url
# url = domain + 'myPortal.do'
index = r.text.find('myPortal.do?thetime=')
url = domain + r.text[index:index+33] # params = {'thetime': t}
r = requests.get(url, headers=headers, cookies=cookies)
if r.status_code != requests.codes.ok:
    fp.write("Enter School Web Failse:", r.status_code + '\n')
    fp.write(r.raise_for_status())
    fp.close()
    exit()
fp.write("Enter School Web Success: " + str(r.status_code) + "\n")

# 進琴房 (1/2)， 需要JSESSIONID
headers['Sec-Fetch-Site'] = 'none'
datetime = r.text[index+20:index+33]
url = domain + 'ssoIndex.do?apUrl=https://pms.itc.ntnu.edu.tw/BookMeApp/BookMe1010Ctrl?action=doLogin&apOu=Practice_Piano_Room_Booking&sso=true&datetime1='+datetime
r = requests.get(url, cookies=cookies)
if r.status_code != requests.codes.ok:
    fp.write("Enter Booking Web (1/2) Failse:", r.status_code + '\n')
    fp.write(r.raise_for_status())
    fp.close()
    exit()
fp.write("Enter Booking Web (1/2) Success: " + str(r.status_code) + "\n")
# get data
sessionId = r.text[r.text.find("sessionId' value='")+18:r.text.find("'>\n<input type='hidden' name='userid")]
userid = account['muid']
data = {'sessionId': sessionId, 'userid': userid}

# 進琴房 (2/2)， 會給新的JSESSIONID
domain = 'https://pms.itc.ntnu.edu.tw/'
url = domain + 'BookMeApp/BookMe1010Ctrl?action=doLogin'

r = requests.post(url, headers=headers, data=data, cookies=cookies)
if r.status_code != requests.codes.ok:
    fp.write("Enter Booking Web (2/2) Failse:", r.status_code + '\n')
    fp.write(r.raise_for_status())
    fp.close()
    exit()
fp.write("Enter Booking Web (2/2) Success: " + str(r.status_code) + "\n")
cookies = r.cookies.get_dict()
cookies['_ga'] = ga
cookies['_gid'] = gid
cookies['_ga_L47EP67E8W'] = ga_L47EP67E8W

# 預約琴房
headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
headers['Host'] = 'pms.itc.ntnu.edu.tw'
headers['Origin'] = 'https://pms.itc.ntnu.edu.tw'
headers['Referer'] = 'https://pms.itc.ntnu.edu.tw/BookMeApp/BookMe1010Ctrl'
headers['Sec-Fetch-Dest'] = 'empty'
headers['Sec-Fetch-Mode'] = 'cors'
headers['Sec-Fetch-Site'] = 'same-origin'
headers['X-Requested-With'] = 'XMLHttpRequest'

url = domain + 'BookMeApp/BookMe1050Ctrl'
data = {'action': 'doBookMe', 'data': ''}
date = time.strftime('%Y%m%d',t)
for i in section:
    data['data'] = date + room + i
    r = requests.post(url, headers=headers, data=data, cookies=cookies)
    fp.write(r.text)

fp.close()