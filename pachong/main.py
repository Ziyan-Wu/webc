# This is a sample Python script.
import re

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

import requests

requests.DEFAULT_RETRIES = 5



def get_one_page(url):
    headers = {
        'Connection':'close',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko)   Chrome/65.0.3325.162 Safari/537.36'
    }
    s = requests.session()
    s.keep_alive = False
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text

    s = requests.session()
    s.keep_alive = False
    s.post(url)
    return None

def main():
    url = 'http://maoyan.com/board/4'
    html = get_one_page(url)
    print(html)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
