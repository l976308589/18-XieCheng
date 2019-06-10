import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import csv
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

def generate_chrome():
    chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    options = webdriver.ChromeOptions()
    options.add_argument('lang=zh_CN.UTF-8')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(chromedriver)
    return driver

def get_comment(driver):
    comment_list = []
    for i in range(100):
        try:
            locator = (By.CLASS_NAME, 'comment_main')
            WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located(locator))
            soup = BeautifulSoup(driver.page_source,"lxml")
            comment = soup.find_all(class_ = "J_commentDetail")
            for j in comment:
                comment_list.append(j.text)#拿到每条评论
            next_ = driver.find_element_by_class_name("c_down")
            next_.click()
            print("第{}页".format(i))
            time.sleep(2)
        except:
                pass
    return comment_list
chrome_options = Options()
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("loglevel='3'")
# chrome_options.add_argument("blink-settings=imagesEnable=false")

start_url = "https://hotels.ctrip.com/hotel/shanghai2#ctm_ref=hod_hp_sb_lst"

try:
    f = open("findtrip.csv", "w", newline="")
    fileheader = ["img_link", "hotel_name", "quality_stars", "address", "hotel_tage", "price", "judge_nums",
                  "hotel_judge", "total_judgement_score", "recommend_kw"]
    cr = csv.DictWriter(f, fieldnames=fileheader)
    cr.writeheader()

    bor = webdriver.Chrome(chrome_options=chrome_options)
    bor.get(start_url)
    while True:
        sleep(random.uniform(2, 3))
        item_list = bor.find_elements_by_xpath("//div[@class='hotel_new_list J_HotelListBaseCell']/ul")
        print(item_list)
        for item in item_list:
            dic = {}
            dic["img_link"] = item.find_element_by_xpath(".//div[@class='dpic J_as_bottom']/img").get_attribute("src")
            dic["img_link"] = dic["img_link"]
            dic["hotel_name"] = item.find_element_by_xpath(".//div[@class='dpic J_as_bottom']/img").get_attribute("alt")
            dic["quality_stars"] = item.find_element_by_xpath(".//span[@class='hotel_ico']/span[last()]").get_attribute(
                "class")
            dic["quality_stars"] = int(dic["quality_stars"][-1])
            dic["address"] = item.find_element_by_xpath(".//p[@class='hotel_item_htladdress']").text
            dic["address"] = dic["address"].split("。")[0]
            dic["hotel_tage"] = item.find_element_by_xpath(".//span[@class='special_label']").text.replace("\n", ",")
            dic["price"] = item.find_element_by_xpath(".//span[@class='J_price_lowList']").text
            dic["judge_nums"] = item.find_element_by_xpath(".//span[@class='hotel_judgement']/span").text
            dic["hotel_judge"] = item.find_element_by_xpath(".//a[@class='hotel_judge']").get_attribute("title")
            dic["total_judgement_score"] = item.find_element_by_xpath(
                ".//span[@class='total_judgement_score']/span").text
            dic["recommend_kw"] = item.find_element_by_xpath(".//span[@class='recommend']").text.replace("\n", ",")
            # print(dic)
            cr.writerow(dic)
        next_url = bor.find_element_by_xpath("//a[text()='下一页']")
        if not next_url:
            break
        # print(next_url)
        next_url.click()
        print(bor.current_url)
        bor.current_window_handle
        # sleep(random.uniform(0.6,1.3))

except Exception as e:
    print(e)

finally:
    f.close()
    bor.quit()
