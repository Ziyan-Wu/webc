
import json
import requests

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9051'

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55'}
response = requests.get(url, headers=header)
print(response.status_code)

response.encoding = response.apparent_encoding
# print(response.text)

# context = ssl._create_unverified_context()

# result = urllib.request.urlopen(url, context=context).read().decode('utf8')
# print(result.status)
result = response.text.replace('var station_names =\'', '').replace('\'', '').replace(';', '')
station = result.split('@')
# print(station)
cc = {}

for s in station[1::]:
    # print(s)
    data = s.split('|')
    # print(data)
    # break
    cc[str(data[1])] = data[2]
# print(cc)

''' 写成json文件'''

with open("citycode.json", "w", encoding='utf-8') as outfile:
    json.dump(cc, fp=outfile, ensure_ascii=False)



