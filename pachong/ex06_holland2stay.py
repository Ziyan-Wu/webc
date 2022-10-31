import time
from wxauto import WeChat
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from lxml import etree
import json
import re
import numpy as np
import prettytable as pt
import pandas as pd

from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

'''
获取链接========================
'''
holland2stay = 'https://holland2stay.com/residences.html?available_to_book=179'
# 'https://holland2stay.com/residences/studio1-indefinite.html?available_to_book=179,336&city=25,90'

# https://holland2stay.com/residences.html?_=1664690948191&available_to_book=179&p=2

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    # 'cookie': 'ai_user=5YqS2gz3MaBT/lERkqpo0o|2022-06-26T15:26:26.666Z; _ga=GA1.2.2000435899.1656257187; _gcl_au=1.1.1020666982.1664034236; _gid=GA1.2.265423349.1664034237; __cf_bm=GA5S_sB0elMcNrpbsALXyt7WxomMn_W6VUjA4HCzub0-1664093813-0-AXqQvnwPewLxq64/dVy20XtMqYSJ0vPZp6EQSG5LRMFIkOqF6ccxReWpxwuObyuCi72FnSFgFyDLKWiRl9uPN6Gub0CCvsFZnTr3i1oycRY9ZpF+p4LE6vzR9cLmY8Miaw==; XSRF-TOKEN=eyJpdiI6IlVXUFU3THQ5N2VXd3J4NFUxQ2FBRnc9PSIsInZhbHVlIjoiU2w4MG1ONjVEL2FFVEJPb2FSVlpOdE5QRWlUeGovWGwvODd6QU9Md2RqN00vSi9rSFF6LzRVT1RQc2xvTTN1V0NVdXdOQllubkdqZ2c1OEhRN1hqOStmVEoyT0owalFCRGkzMjFqUTBENWNJd09Ya1dMMVBiamRrS1FvR0ZWVVciLCJtYWMiOiI2NTUzMzAwOTc3ZjZiODc0ODk5NTUzYWYyZWJmMTI2OWE3ZGI3MDY5ODVjYjBkNzRhOTU3NjNkNTIwMGJmNTI5In0=; laravel_session=eyJpdiI6Im9wM2t1Q0luRnFqVEhKZDBZZkhIMmc9PSIsInZhbHVlIjoiUlBOVmZZbnZ4aUpBcXFiYWdqL0lYYjlrVTh1QjR2SWtkY2w2TW5XY0RWeStpVm5RSXd4VmRMK3hHVldTNzV0ZTZEbjZNMm5TL1ZHdkRFMk9vb2VDQzJmd05SaU43Nk1lK3loWnJqRzRuOG5zQWp4M0QzbGVIeXJBeG41aE9xTkciLCJtYWMiOiIxY2QwOGMwMDMzNmIwOGFjMzRkNGU4YzEwZDdmNWE3Y2NkNGE1YzljMDc3ZWY2YzFhODJhN2M1MmRlNmZiMjk2In0=; _gat_gtag_UA_145833656_1=1; _gat_UA-145833656-1=1',
    # 'x-csrf-token': '2e56v7Xq4YHpyy48ZQ2KQ63w1d95HZiNDAQauD35'
}

response = requests.get(holland2stay, headers=header)
# print(response.status_code)


'''
内容解析=================================
'''
htmls = etree.HTML(response.text)

rent = htmls.xpath('//*[@id="layer-product-list"]/div[2]/div/div[3]/div/div/text()')
# print(rent)

notes = htmls.xpath('//*[@id="layer-product-list"]/div[2]/div/div[3]/p/text()')
# print(notes)
ls_othercost = []
for ele in notes:
    ls_othercost.append(re.findall(r"\d+\.?\d*", str(ele)))
ls_othercost = list(np.ravel(ls_othercost))
# print(ls_othercost)


for i in range(1, 8, 1):
    basic_path = '//*[@id="layer-product-list"]/div[2]/div/div[2]/ul[2]/li[{}]/text()'.format(i)
    if i == 1:
        furnish = htmls.xpath(basic_path)
    elif i == 2:
        floor = htmls.xpath(basic_path)
    elif i == 3:
        size = htmls.xpath(basic_path)
    elif i == 4:
        type = htmls.xpath(basic_path)
    elif i == 5:
        occupancy = htmls.xpath(basic_path)
    elif i == 6:
        contract = htmls.xpath(basic_path)
    elif i == 7:
        min_stay = htmls.xpath(basic_path)
# print(furnish,floor,size,type,occupancy,contract,min_stay)


city = htmls.xpath('//*[@id="layer-product-list"]/div[2]/div/div[2]/ul[1]/li[2]/span/text()')
# print(city)

building = htmls.xpath('//*[@id="layer-product-list"]/div[2]/div/div[2]/ul[1]/li[3]/span/text()')
# print(building)

address = htmls.xpath('//*[@id="layer-product-list"]/div[2]/div/div[2]/div/h4/text()[1]')
# print(address)

book = htmls.xpath("//*[@id='layer-product-list']/div[2]/div/div[2]/div/h4/span[@class='direct-tag']/text()[1]")
# print(book)

available = htmls.xpath('//*[@id="layer-product-list"]/div[2]/div/div[2]/ul[1]/li[1]/strong/text()')
# print(available)


'''
输出格式=====================================================
'''
'''df'''
# dic = {'地址': address, '城市': city, '建筑名字': building, '楼层': floor,
#        '面积': size, '基本房租': rent, '其他费用': ls_othercost,
#        '装修':furnish, '房间数量':type, '居住人数':occupancy,
#        '合同类型':contract, '不少于':min_stay, '抽奖吗':book,
#        '开始时间':available}
# df = pd.DataFrame(dic)
# print(df)


'''pretty table'''
llss = [address, city, building, floor, size,
        rent, ls_othercost, furnish, type, occupancy,
        contract, min_stay, book, available]

colnames = [
    '地址',
    '城市',
    '建筑名字',
    '楼层',
    '面积',
    '基本房租',
    '其他费用',
    '装修',
    '房间数量',
    '居住人数',
    '合同类型',
    '不少于',
    '抽奖吗',
    '开始时间'
]

combo = [*zip(colnames, llss)]
tb = pt.PrettyTable()
tb.field_names = colnames

for ele in combo:
    tb.add_column(ele[0], ele[1])
print(tb)

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '共有：{}套'.format(len(city)),
      '\n 鹿特丹：{}套'.format(city.count('Rotterdam')),
      '\n 海牙：{}套'.format(city.count('Rotterdam')))

'''
微信通知========================================
'''

# # 获取当前微信客户端
# wx = WeChat()
# # 获取会话列表
# wx.GetSessionList()
#
# who1 = '文件传输助手'  # 这里填要发送的人的备注
# who2 = 'S岳-1.12阴'
# wx.ChatWith(who1)  # 只能给一个人发送
#
# if 'Rotterdam' in city:
#     text = 'Holland2stay：鹿特丹！快去抢'
#     wx.SendMsg(text)
# else:
#     text = 'Holland2stay：还没有你想要的'



'''
邮件通知=================================
'''
host_server = 'smtp.qq.com'  # qq邮箱smtp服务器
sender_qq = '865924194@qq.com'  # 发件人邮箱
pwd = 'cxfumlezsziebfaj'
receiver = ['juliawu97@outlook.com']  # 收件人邮箱
# receiver = '913@qq.com'
mail_title = 'Python自动发送_Holland2Stay'  # 邮件标题
mail_content = "鹿特丹和海牙有房子了！！！"  # 邮件正文内容

if city.count('Rotterdam') != 0 or city.count('Den Haag') != 0:
    # 初始化一个邮件主体
    msg = MIMEMultipart()
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq
    # msg["To"] = Header("测试邮箱",'utf-8')
    msg['To'] = ";".join(receiver)
    # 邮件正文内容
    msg.attach(MIMEText(mail_content, 'plain', 'utf-8'))

    smtp = SMTP_SSL(host_server)  # ssl登录
    smtp.login(sender_qq, pwd)
    smtp.sendmail(sender_qq, receiver, msg.as_string())
    # quit():用于结束SMTP会话。
    smtp.quit()