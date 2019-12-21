# coding=utf-8
import requests
import re

url = 'https://yunpan.360.cn/surl_yuaMCkNRDH2'
response1 = requests.get(url)
pattern1 = re.compile('"nid": ".*?"') #nid
pattern2 = re.compile("download_permit_token: '.*?',") #download_permit_token
#print(response1)
#print(response1.text)
matchNid = pattern1.findall(response1.text)
matchDLToken = pattern2.search(response1.text).group()

nidList = []
for i in matchNid:
    nidList.append(re.search(r'\d*\d',i).group()) #取出数字

print(matchDLToken)
payload = {
    'shorturl': url.replace('https://yunpan.360.cn/',''),
    'nid': nidList[0], #这里填获取文件nid
    'download_permit_token': re.search(r"'.*'", matchDLToken).group()
}
trueUrl = re.search(r'\/\/.*?\/',response1.url).group().replace('/', '')
headers = '''
Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive
Content-Length: 102
Content-type: application/x-www-form-urlencoded UTF-8
Host: {0}
Origin: https://{0}
Referer: https://{0}/lk/{1}
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36
X-Requested-With: XMLHttpRequest
'''.format(trueUrl,payload['shorturl'])

def gen_headers(s):
    ls = s.split('\n')
    lsl = []
    ls = ls[1:-1]
    headers = {}
    for l in ls:
        l = l.split(': ')
        lsl.append(l)
    for x in lsl:
        headers[str(x[0]).strip('    ')] = x[1]
    return headers


response2 = requests.post('https://{0}/share/downloadfile'.format(trueUrl), data=payload,
                          headers=gen_headers(headers))
resultJson = response2.json()
print(resultJson['data']['downloadurl']) #输出文本
