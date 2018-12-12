import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyexcel


def enter_address(driver, start_city, end_city):

    driver.implicitly_wait(10)
    start_input = driver.find_element_by_xpath('//div[@class="qunar-qcbox"]/input[@name="fromCity"]')
    start_input.send_keys(start_city)
    time.sleep(1)
    start_input.send_keys(Keys.RETURN)

    end_input = driver.find_element_by_xpath('//div[@class="qunar-qcbox"]/input[@name="toCity"]')
    end_input.send_keys(end_city)
    time.sleep(1)
    ToCity.send_keys(Keys.RETURN)


def tick_query(fromCity, toCity):
    driver = webdriver.Chrome()
    driver.get('http://www.qunar.com')
    enter_address(driver, fromCity, toCity)


if __name__ == '__main__':
    # start = '北京'
    keyword = '成都'
    driver = webdriver.Chrome()
    driver.get('http://www.qunar.com')
    driver.implicitly_wait(10)
    ToCity = driver.find_element_by_xpath('//div[@class="qunar-qcbox"]/input[@name="toCity"]')
    ToCity.send_keys(keyword)
    time.sleep(1)
    ToCity.send_keys(Keys.RETURN)

    search_btn = driver.find_element_by_xpath(
        '//form[@id="js_flight_domestic_searchbox"]//button[@class="button-search"]')
    search_btn.click()

    flights = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@class="mb-10"]//div[@class="e-airfly"]'))
    )
    data = []
    for f in flights:
        fdata = {}
        airlines = f.find_elements_by_xpath('.//div[@class="d-air"]')
        fdata['airline'] = "".join([airline.text.replace('\n', "-") for airline in airlines])
        # 始发地
        fdata['depart'] = f.find_element_by_xpath('.//div[@class="sep-lf"]/p').text
        # 开始时间
        fdata['time_begin'] = f.find_element_by_xpath('.//div[@class="sep-lf"]/h2').text
        # 时长
        fdata['duration'] = f.find_element_by_xpath('.//div[@class="range"]').text
        # 终点站
        fdata['dest'] = f.find_element_by_xpath('.//div[@class="sep-rt"]').text
        # 原始价格
        fake_price = list(f.find_element_by_xpath('.//em/b[1]').text)
        keys = f.find_elements_by_xpath('.//em/b[position()>1]')

        for k in keys:
            index = int(k.value_of_css_property('left')[:-2]) // 18
            fake_price[index] = k.text
            fdata['price'] = "".join(fake_price)

        print(fdata)
    pyexcel.save_as()

    driver.quit()
