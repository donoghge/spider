import sys
import time

from selenium import  webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pyexcel
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

if __name__ == '__main__':
    keyword = 'iphone'
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
    # 隐藏chrome，创建一个option对象
    option = Options()
    # option.add_argument('--headless')
    # 创建driver对象， 并把隐藏chrome值赋给driver
    driver = webdriver.Chrome(chrome_options=option)
    # 截图
    driver.save_screenshot('1.png')

    driver.get('https://www.jd.com/')
    # 输入搜索信息
    kw = driver.find_element_by_id('key')
    kw.send_keys(keyword)
    # 输入回车
    kw.send_keys(Keys.RETURN)

    # 隐式等待
    driver.implicitly_wait(10)
    # 按销量排序
    # 显式等待， 当查找到我们需要定位的元素时，则立即返回，否则最长等待10秒钟
    # 默认每隔500毫秒查找一次，直到找到了响应的元素或者timeout
    sort_btn = WebDriverWait(driver, 10).until(
        # 期待条件
        EC.presence_of_element_located((By.XPATH, './/div[@class="f-sort"]/a[2]'))
    )
    # sort_btn = driver.find_element_by_xpath('.//div[@class="f-sort"]/a[2]')
    sort_btn.click()
    driver.save_screenshot('2.png')

    has_next = True
    rows = []

    page_count = 0

    while has_next:
        page_count += 1
        if page_count > 3:
            break
        goods_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_element_located()
        )
        goods_list = driver.find_element_by_id('J_goodsList')
        # 先获取整个商品区域的尺寸坐标
        y = goods_list.rect['y'] + goods_list.rect['height']
        # 执行js
        driver.execute_script('window.scrollTo(0, %s)' % y)

        # 获取所有商品节点
        products = driver.find_elements_by_class_name('gl-item')

        # 价格 sku唯一id。
        for p in products:
            row = {}
            sku = p.get_attribute('data-sku')
            row['price'] = p.find_element_by_css_selector('strong.J_%s' % sku).text
            row['name'] = p.find_element_by_css_selector('div.p-name>a>em').text
            row['comments'] = p.find_element_by_id('J_comment_%s' % sku).text

            try:
                row['shop'] = p.find_element_by_css_selector('div.p-shop>span>a').text
            except Exception:
                row['shop'] = '无'
            print(row)
            rows.append(row)

        try:
            # 下一页元素
            next_page = driver.find_element_by_css_selector('a.pn-next')

            if 'disabled' in next_page.get_attribute('class'):
                has_next = False
            else:
                next_page.click()
        except Exception:
            has_next = False

    pyexcel.save_as(records=rows, dest_file_name='%s.xls' % keyword)
    driver.quit()


"""
goods_list.rect()   可显示长宽高
next_page.is_enabled()  查看元素是否可点
get_attribute('class'):  获取属性
driver.back()   返回上一步
next_page.location()    当前位置
"""
"""
等待的几种方式：
隐式等待:
implicitly_wait(10): 如果没有立即查到相应的元素，则最长等待10秒钟。
time.sleep(10)： 不管能否找到元素，都等待10秒。
"""
