import requests
from bs4 import BeautifulSoup
from lxml import etree
import json
import re
import multiprocessing
# import xlwt
import time
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
import prettytable as pt
import ticket_buy

'''读取城市code.json'''

# json文件 转 Python数据类型
with open("D:/03workplace/pachong/ex04_12306/citycode.json",
          'r', encoding='utf-8') as f:
    city_data = json.load(f)
# %%

# city_data['上海']

# %%
'''输入出发到达城市，时间'''
from_station = city_data['西安']
to_station = city_data['广州']
train_date = '2022-10-02'

# from_station = city_data[input('departure city: ')]
# to_station = city_data[input('arrive city: ')]
# train_date = input('date (format: 2022-05-01): ')
# print(from_station, to_station, train_date)

'''根据输入-更改url'''
aim_link = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?' \
           'leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&' \
           'leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(train_date, from_station, to_station)
# print(aim_link)
# https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2022-09-27&leftTicketDTO.from_station=XAY&leftTicketDTO.to_station=GZQ&purpose_codes=ADULT


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55',
          'Cookie': '_uab_collina=166383369752571822153616; JSESSIONID=DF7EF7E7BD4C9AE3DB630A223EBB7ABC; BIGipServerotn=418382346.50210.0000; RAIL_EXPIRATION=1664130073550; RAIL_DEVICEID=JM23qN7Whm3pkS5TjxWBqKegm7ebeDHn6CLWwR8SKmY-1u45fy5Y83v9rSLPWMuisqG_4MoopusAslMgnXjdHnGz7mkuaYngFv8oY8Oh9geHA0lBgvtlT84_2g3TLOEzxao9U1IXHX0wsi8P1OX5RuOqai9arg4t; BIGipServerpool_passport=149160458.50215.0000; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; fo=mr4xxi63eitk7a6rIMBl60T0R7mb2JQ3aPSMIO3c_3RFjJi7fu7SsaRmhT5N0XWyDiaJk-Ar5oUKnthIhYQqfJPOppWyXzkXpriBsBsqD7QiXru-tRLga3i80SQwvSCRUuZMh-YuAxo7udCPbWpAG4fbzaWYVGjDeTtk3CbK7mQkm1L_rckwNJrP_Zk; route=495c805987d0f5c8c84b14f60212447d; ai_user=yn5FsvthZPkgVt4UK8uDxu|2022-09-22T08:01:36.281Z; _jc_save_fromStation=%u5E7F%u5DDE%2CGZQ; _jc_save_toDate=2022-09-22; _jc_save_wfdc_flag=dc; _jc_save_fromDate=2022-09-30; _jc_save_toStation=%u676D%u5DDE%2CHZH'}

response = requests.get(aim_link, headers=header)
# print(response.status_code)


""" 获取内容 """
response.encoding = response.apparent_encoding  # change to Chinese

# '''M1'''
# response.text
#
# #%%
# '''M2'''
#
# response.json()
# # type(response.json()) # dict
#
# #%%
# ''' M2等效 '''
# data = json.loads(response.text)
# data
# # type(data) # dict

'''pretty table'''
tb = pt.PrettyTable()
tb.field_names = [
    '序号',
    '车次',
    '发车时间',
    '到达时间',
    '车程',
    '特等',
    '一等',
    '二等',
    '软卧',
    '硬卧',
    '硬座',
    '无座'
]

# %%

''' 内容解析 '''

'''解析'''
cnt = 0
for ele in response.json()['data']['result']:
    info = ele.split('|')
    # print([*enumerate(ele.split('|'))])
    t_num = info[3]

    start_time = info[8]
    end_time = info[9]
    used_time = info[10]

    topGrade = info[32]
    first_class = info[31]
    second_class = info[30]

    soft_sleeper = info[23]
    hard_sleeper = info[28]

    # soft_seat = info[]
    hard_seat = info[29]
    no_seat = info[26]

    cnt += 1

    dic = {'车次': t_num,
           '发车时间': start_time, '到达时间': end_time, '车程': used_time,
           '特等': topGrade, '一等': first_class, '二等': second_class,
           '软卧': soft_sleeper, '硬卧': hard_sleeper,
           '硬座': hard_seat, '无座': no_seat
           }  # '软座': soft_seat,
    # print(dic)

    tb.add_row([
        cnt, t_num,
        start_time, end_time, used_time,
        topGrade, first_class, second_class,
        soft_sleeper, hard_sleeper,
        hard_seat, no_seat
    ])
# %%

print(tb)

No = input("Select the train's No.: ")

ticket_buy.select_ticket(No, from_station, to_station, train_date) # 原始B站版本

# ====================================================================================
## 在查询的基础上，登录预定
# ticket_buy.book_ticket(aim_link, No)
## 此方法失败，aimlink打开后是包含目标查询信息的html文字版本，非直接从12306点击查询的网页格式
# =========================================================================================