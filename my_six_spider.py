import os   # 系统控制库
import requests # 请求网页库
from bs4 import BeautifulSoup # 解析网页库
import time # 时间推迟库
from urllib.parse import urljoin # 网页拼接库

url = 'https://books.toscrape.com/'
count = 0
page = url
os.makedirs('images', exist_ok=True)  # 建文件夹 exist_ok=True：同名文件夹不报错
try:
    while page:
        response = requests.get(page, timeout=5)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')

        article = soup.find_all('article', class_="product_pod")
        for link in article:  # 遍历每本的jpg地址
            count += 1  # 递增jpg名
            if os.path.exists(f'images/{count:03d}.jpg'):  # 断点接续  os.path.getsize() > 1024 : 应对0字节空文件 假阳性
                # 但是它只管文件在不在，不保证好不好
                continue
            try:

                time.sleep(1)
                img = link.find('a').find('img')['src']
                img_url = urljoin(url, img)  # 拼接每本jpg相对地址
                img_response = requests.get(img_url).content  # 转变二进制

                with open(f'images/{count:03d}.jpg', 'wb') as f:  # 补零：保持最少三位数
                    f.write(img_response)

            except Exception as e:
                print(f'第{count}张失败，跳过{e}')
                continue

        page_next = soup.find('li', class_="next")  # 翻页地址
        # print(page_next)
        if page_next:  # 先看有无li
            print(f'继续下载{page}中')
            page_url = page_next.find('a')['href']
            page = urljoin(page, page_url)
            time.sleep(1)
        else:
            break

except Exception as e:
    print(e)

#    第657张失败，跳过('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
# 再运行一次或者 用运算补下：
# import requests
# from urllib.parse import urljoin
# from bs4 import BeautifulSoup
#
# n = 657
# page_num = (n - 1) // 20 + 1   # 整除算页 → 33
# book_idx = (n - 1) % 20        # 取余算下标 → 16
#
# soup = BeautifulSoup(
#     requests.get(f'https://books.toscrape.com/catalogue/page-{page_num}.html').text,
#     'html.parser')
# img = soup.find_all('article', class_='product_pod')[book_idx].find('img')['src']
#
# data = requests.get(urljoin('https://books.toscrape.com/', img)).content
# with open(f'images/{n:03d}.jpg', 'wb') as f:
#     f.write(data)
# print('补下成功')

