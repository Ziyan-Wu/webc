import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys  # 控制按键


def select_ticket(No, from_station, to_station, train_date):
    driver = webdriver.Chrome()  # 弹出谷歌浏览器

    # ====================================================================================
    '''解决滑块问题
    绕过selenium检测'''
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                           {"source": """Object.defineProperty(navigator, 'webdriver',
                           {get: () => undefined})"""})
    # ====================================================================================

    driver.get('https://kyfw.12306.cn/otn/resources/login.html')  # 到指定url

    '''
    自动输入账号+密码，自动登录
    '''
    # find selector, right click, copy selector
    # J-userName
    # J-login
    # J-password
    driver.find_element_by_css_selector('#J-userName').send_keys('13672793200')
    driver.find_element_by_css_selector('#J-password').send_keys('13772993701')

    driver.find_element_by_css_selector('#J-login').click()

    '''
    自动拖动滑块验证
    '''
    driver.implicitly_wait(5)  # 表示隐性等待5秒，
    track = [300, 400, 500]  # track中放的是滑块拉动的距离，像素
    for i in track:
        try:
            # 找到滑块
            # browser.find_element_by_xpath和id的区别：在右键复制时要copy XPath或copy full XPath
            btn = driver.find_element_by_xpath('//*[@id="nc_1__scale_text"]/span')  # M1
            # driver.find_element_by_id("nc_1_n1z") # M2
            # driver.find_element_by_css_selector('#nc_1_n1z') # M3

            # 移动
            ActionChains(driver).drag_and_drop_by_offset(btn, i, 0).perform()  # M1

            # ActionChains(driver).click_and_hold(btn).move_by_offset(300, 0).perform()  # M2
            # ActionChains(driver).release()
        except:
            time.sleep(2)

    '''
    疫情温馨提示-点击确定
    '''
    driver.implicitly_wait(5)
    driver.find_element_by_xpath('/html/body/div[2]/div[7]/div[2]/div[3]/a').click()

    '''
    车票预定 + 关闭进京提示
    '''
    driver.find_element_by_css_selector('#link_for_ticket').click()  # 车票预定链接
    # 关闭进京提示
    driver.find_element_by_css_selector('#qd_closeDefaultWarningWindowDialog_id').click()
    # driver.find_element_by_css_selector('#link_for_ticket').send_keys(Keys.ENTER)  # M1

    '''
    车票查询
    '''
    # TODO: 起始地点的输入
    driver.implicitly_wait(3)
    driver.find_element_by_css_selector('#fromStationText').clear()  # 出发地 #fromStationText
    driver.find_element_by_css_selector('#fromStationText').click()
    driver.find_element_by_css_selector('#fromStationText').send_keys(from_station, Keys.ENTER)
    # driver.find_element_by_css_selector('#fromStationText').send_keys()

    driver.implicitly_wait(3)
    driver.find_element_by_css_selector('#toStationText').clear()  # 目的地 #toStationText
    driver.find_element_by_css_selector('#toStationText').click()
    driver.find_element_by_css_selector('#toStationText').send_keys(to_station, Keys.ENTER)
    # driver.find_element_by_css_selector('#toStationText').send_keys()

    driver.implicitly_wait(3)
    driver.find_element_by_css_selector('#train_date').clear()  # 出发时间 #train_date
    driver.find_element_by_css_selector('#train_date').send_keys(train_date)

    driver.implicitly_wait(3)
    driver.find_element_by_css_selector('#query_ticket').click()  # 点击查询

    '''
        买票阶段
        '''
    driver.implicitly_wait(3)
    driver.find_element_by_xpath(
        ('/html/body/div[2]/div[8]/div[8]/table/tbody/tr[{}]/td[13]/a').format(2 * int(No) - 1)).click()  # 点击选的车票预订
    '''
        规律： full Xpath
        /html/body/div[2]/div[8]/div[8]/table/tbody/tr[1]/td[13]/a
        
        /html/body/div[2]/div[8]/div[8]/table/tbody/tr[3]/td[13]/a
        
        /html/body/div[2]/div[8]/div[8]/table/tbody/tr[5]/td[13]/a
        '''

    driver.find_element_by_xpath(
        '/html/body/div[1]/div[10]/div[3]/div[2]/div[1]/div[2]/ul/li[1]/input').click()  # 选择乘车人
    driver.find_element_by_css_selector('#submitOrder_id').click()  # 提交订单
    time.sleep(10)
    '''火车票：直接确认'''
    # driver.find_element_by_css_selector('#qr_submit_id').click()  # 确认
    '''高铁票：选座位，也可以不选择，随机分配'''
    # driver.find_element_by_css_selector('#qr_submit_id').click()  # 确认
    '''确认后票被锁定，有10 min支付时间'''



def book_ticket(aim_link, No): # Unfeasible
    driver = webdriver.Chrome()  # 弹出谷歌浏览器
    # ====================================================================================
    '''解决滑块问题
    绕过selenium检测'''
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                           {"source": """Object.defineProperty(navigator, 'webdriver',
                               {get: () => undefined})"""})
    # ====================================================================================

    driver.get(aim_link)  # 到指定url

    '''
       车票预定
       '''
    driver.implicitly_wait(3)
    driver.find_element_by_xpath(
        ('/html/body/div[2]/div[8]/div[8]/table/tbody/tr[{}]/td[13]/a').format(2 * int(No) - 1)).click()  # 点击选的车票预订

    '''
        自动输入账号+密码，自动登录
        '''
    # find selector, right click, copy selector
    # J-userName
    # J-login
    # J-password
    driver.find_element_by_css_selector('#J-userName').send_keys('13672793200')
    driver.find_element_by_css_selector('#J-password').send_keys('13772993701')

    driver.find_element_by_css_selector('#J-login').click()

    '''
        自动拖动滑块验证
        '''
    driver.implicitly_wait(5)  # 表示隐性等待5秒，
    track = [300, 400, 500]  # track中放的是滑块拉动的距离，像素
    for i in track:
        try:
            # 找到滑块
            # browser.find_element_by_xpath和id的区别：在右键复制时要copy XPath或copy full XPath
            btn = driver.find_element_by_xpath('//*[@id="nc_1__scale_text"]/span')  # M1
            # driver.find_element_by_id("nc_1_n1z") # M2
            # driver.find_element_by_css_selector('#nc_1_n1z') # M3

            # 移动
            ActionChains(driver).drag_and_drop_by_offset(btn, i, 0).perform()  # M1

            # ActionChains(driver).click_and_hold(btn).move_by_offset(300, 0).perform()  # M2
            # ActionChains(driver).release()
        except:
            time.sleep(2)

    '''
        买票阶段
        '''
    driver.find_element_by_xpath(
        '/html/body/div[1]/div[10]/div[3]/div[2]/div[1]/div[2]/ul/li[1]/input').click()  # 选择乘车人
    driver.find_element_by_css_selector('#submitOrder_id').click()  # 提交订单
    time.sleep(10)
    '''火车票：直接确认'''
    # driver.find_element_by_css_selector('#qr_submit_id').click()  # 确认
    '''高铁票：选座位，也可以不选择，随机分配'''
    # driver.find_element_by_css_selector('#qr_submit_id').click()  # 确认
    '''确认后票被锁定，有10 min支付时间'''
