#！/user/bin/pytthon
# -*- coding:utf-8 -*-
# @Time: 2018/5/23 20:08
# @Author: lichexo
# @File: taobaomeishi.py


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
from config import *
import pymongo


KEYWORDS = "美食"
MONGO_URL = "localhost"
MONGO_DB = "taobao"
MONGO_TABLE = "product"


client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


browser = webdriver.Chrome('D:\Applications\chrome\Google\Chrome\Application\chromedriver.exe')
wait = WebDriverWait(browser, 10)


def search():
    # 由主页进入到搜索框，并进行搜索
    try:
        browser.get('https://www.taobao.com')
        input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
            )
        submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button"))
            )
        input.send_keys(KEYWORDS)
        submit.click()
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))
        )
        get_products()
        return total.text
    except TimeoutException:
        return search()


def next_page(page_number):
    # 根据所选中框的状态来进行自动翻页
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit"))
        )
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > ul > li.item.active > span"), str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)


def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-itemlist .items .item")))
    html = browser.page_source
    doc = pq(html)
    items = doc("#mainsrp-itemlist .items .item").items()
    for item in items:
        product = {
            "image": item.find(".pic .img").attr('src'),
            "price": item.find(".price").text(),
            "deal": item.find(".deal-cnt").text()[:-3],
            "title": item.find(".title").text(),
            "shop": item.find(".shop").text(),
            "location": item.find(".location").text()
        }
        print(product)
        save_to_mongodb(product)


def save_to_mongodb(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print("保存到MONGOdb成功",result)
    except Exception:
        print("存储到MONGOdb失败", result)


def main():
    try:
        total = search()
        total = int(re.compile('(\d+)').search(total).group(1))
        for i in range(2, total+1):
            next_page(i)
    except Exception:
        print('出错啦')
    finally:
        browser.close()


if __name__ == '__main__':
    main()