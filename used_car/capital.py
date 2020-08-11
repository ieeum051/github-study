from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import json
import time
import datetime
import sys

OUTPUT_PATH = './output/'
#CHROME_PATH = '../../chromedriver'
CHROME_PATH = '/usr/local/bin/chromedriver'
LOAD_WEB_PAGE = 1

# from pyvirtualdisplay import Display

def get_now():
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    return nowDatetime

def main():
    # display = Display(visible=0, size=(800, 800))  
    # display.start()
    # try_chrome()
    UsedCar().run()
    # UsedCar()._conver_num('2,499만원')

def try_firefox(): # 안됨.
    # export PATH=$PATH:/home/ieeum/work/used_car
    # browser = webdriver.Firefox('/home/ieeum/work/used_car')
    driver = webdriver.Firefox()
    driver.implicitly_wait(3)
    driver.get("http://python.org")  

class UsedCar:
    def __init__(self):
        self._set_url_list()
        self.json_file = 'captial_list.json'
        self.new_car_file = 'new_capital_list.json'

        if LOAD_WEB_PAGE:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

            self.driver = webdriver.Chrome(executable_path=CHROME_PATH,
                                        chrome_options=chrome_options)
        # self.driver.implicitly_wait(3)


    def run(self):
        for i in range(10000):
            print('\n'+ '\033[93m' + 'Run Crawling at {}'.format(get_now()) + '\033[0m')
            self.gen_car_info_list()
            break
            time.sleep(60*15)            

    def _set_url_list(self):
        self.url_list = [
            # 쏘렌토 검색
            'https://certifiedcar.hyundaicapital.com/hcsfront/ms/carList?schKeyword=%25EC%258F%2598%25EB%25A0%258C%25ED%2586%25A0'
            # 'http://www.encar.com/dc/dc_carsearchlist.do?carType=kor#!%7B%22action%22%3A%22(And.Year.range(201800..)._.Hidden.N._.FuelType.%EB%94%94%EC%A0%A4._.Options.%EC%B0%A8%EC%84%A0%EC%9D%B4%ED%83%88%20%EA%B2%BD%EB%B3%B4%20%EC%8B%9C%EC%8A%A4%ED%85%9C(LDWS_)._.Options.%ED%81%AC%EB%A3%A8%EC%A6%88%20%EC%BB%A8%ED%8A%B8%EB%A1%A4(%EC%96%B4%EB%8C%91%ED%8B%B0%EB%B8%8C_)._.(C.CarType.Y._.(C.Manufacturer.%EA%B8%B0%EC%95%84._.(C.ModelGroup.%EC%8F%98%EB%A0%8C%ED%86%A0._.(C.Model.%EB%8D%94%20%EB%89%B4%20%EC%8F%98%EB%A0%8C%ED%86%A0._.BadgeGroup.%EB%94%94%EC%A0%A4%202WD.))))_.Price.range(2000..3000)._.Mileage.range(..60000).)%22%2C%22toggle%22%3A%7B%224%22%3A0%7D%2C%22layer%22%3A%22%22%2C%22sort%22%3A%22ModifiedDate%22%2C%22page%22%3A1%2C%22limit%22%3A%2250%22%7D',
            # 'http://www.encar.com/dc/dc_carsearchlist.do?carType=kor#!%7B%22action%22%3A%22(And.Year.range(201800..)._.Hidden.N._.FuelType.%EB%94%94%EC%A0%A4._.Options.%EC%B0%A8%EC%84%A0%EC%9D%B4%ED%83%88%20%EA%B2%BD%EB%B3%B4%20%EC%8B%9C%EC%8A%A4%ED%85%9C(LDWS_)._.Options.%ED%81%AC%EB%A3%A8%EC%A6%88%20%EC%BB%A8%ED%8A%B8%EB%A1%A4(%EC%96%B4%EB%8C%91%ED%8B%B0%EB%B8%8C_)._.(C.CarType.Y._.(C.Manufacturer.%EA%B8%B0%EC%95%84._.(C.ModelGroup.%EC%8F%98%EB%A0%8C%ED%86%A0._.(C.Model.%EB%8D%94%20%EB%89%B4%20%EC%8F%98%EB%A0%8C%ED%86%A0._.BadgeGroup.%EB%94%94%EC%A0%A4%202WD.))))_.Price.range(2000..3000)._.Mileage.range(..60000).)%22%2C%22toggle%22%3A%7B%224%22%3A0%7D%2C%22layer%22%3A%22%22%2C%22sort%22%3A%22ModifiedDate%22%2C%22page%22%3A2%2C%22limit%22%3A%2250%22%7D',
        ]

    def get_car_info_list(self):

        try:
            with open(self.json_file, 'r') as f:
                car_list = json.load(f)
        except:
            return []

        return car_list

        # for car in car_list:
        #     for key in car.keys():
        #         if key == 'etc': continue
        #         print('{}:{} '.format(key, car[key]), end='')
        #     print('\n------')

    
    def gen_car_info_list(self):
        temp_html_file = 'captical_temp.html'        
        if LOAD_WEB_PAGE:
            html = ''
            self.driver.get(self.url_list[0])
            # self.driver.implicitly_wait(3) # 서브 페이지 로딩이므로 실제 로딩은 빨리 끝난 것으로 판단한다.
            time.sleep(3)

            year1 = "/html/body/div[2]/div[2]/div[1]/div[2]/div[4]/div[1]/div/div/div[1]/a"
            # year1 = "/html/body/div[2]/div[2]/div[1]/div[2]/div[4]/div[1]/div/div/div[2]/div[1]/ul/li[6]/a"
            for i in range(5):
                try:
                    self.driver.find_element_by_xpath(year1).click()
                    print('정렬 선택')
                    time.sleep(3)
                    break
                except:
                    print('not clickable!!!')
                    time.sleep(2)

            # year1 = "/html/body/div[2]/div[2]/div[1]/div[2]/div[4]/div[1]/div/div/div[1]/a"
            year2 = "/html/body/div[2]/div[2]/div[1]/div[2]/div[4]/div[1]/div/div/div[2]/div[1]/ul/li[6]/a"
            for i in range(5):
                try:
                    self.driver.find_element_by_xpath(year2).click()
                    print('연식 순')
                    time.sleep(3)
                    break
                except:
                    print('not clickable!!!')
                    time.sleep(2)                   
            
            self.driver.save_screenshot('captital.png')

            html = self.driver.page_source


            with open(temp_html_file, 'w') as f:
                f.write(html)

            sys.exit()
        
        with open(temp_html_file, 'r') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')


        car_list = soup.find_all('tr')

        car_info_list = []
        for car in car_list:
            # print('--------------------')
            # print(car)

            car_info = {
                'state': None,
                'name': None,
                'type': None,
                'year': None,
                'km': None,
                'region': None,
                'price': None,
                'etc':car.text
                }
            
            for element in car.find_all('span'):
                if str(element).find('class=\"detail\"') > 0: continue # 중복 자료

                if str(element).find('class=\"ass\"') > 0:
                    car_info['state'] = element.text
                if str(element).find('class=\"cls\"') > 0:
                    car_info['name'] = element.text
                if str(element).find('class=\"dtl\"') > 0:
                    car_info['type'] = element.text
                if str(element).find('class=\"yer\"') > 0:
                    car_info['year'] = element.text
                if str(element).find('class=\"km\"') > 0:
                    car_info['km'] = self._convert_num(element.text)
                if str(element).find('class=\"loc\"') > 0:
                    car_info['region'] = element.text
   
            for element in car.find_all('td'):
                if str(element).find('만원') > 0:
                    car_info['price'] = self._convert_num(element.text)

            car_info_list.append(car_info)
        
        # 중복제거
        car_info_list = list(map(dict, set(tuple(sorted(d.items())) for d in car_info_list)))


        # 신규 정보 있는지 확인
        saved_car_info_list = self.get_car_info_list()

        key_cnt = len(car_info.keys())
        find_new_car = False
        find_sold_car = False

        
        #=====================================================================
        new_car_list = []
        for new_car in car_info_list:
            find_flag = False
            for pre_car in saved_car_info_list:
                shared_items = {k: new_car[k] for k in new_car if k in pre_car and new_car[k] == pre_car[k]}
                if len(shared_items) == key_cnt:
                    find_flag = True
            if not find_flag:
                find_new_car = True
                print('\033[95m')
                print(new_car['etc'])
                print('-----------------------')
                new_car_list.append(new_car)

        print('\033[0m')

        if find_new_car:
            with open('new_car_'+get_now()+'.json', 'w') as f:
                json.dump(new_car_list, f)
        else:
            pass
            # print('   There is no new cars...')

        #=====================================================================
        sold_car_list = []            
        for sold_car in saved_car_info_list:
            find_flag = False
            for pre_car in car_info_list: # saved_car_info_list
                shared_items = {k: sold_car[k] for k in sold_car if k in pre_car and sold_car[k] == pre_car[k]}
                if len(shared_items) == key_cnt:
                    find_flag = True
            if not find_flag:
                find_sold_car = True
                print('\033[92m')
                print(sold_car['etc'])
                print('-----------------------')
                sold_car_list.append(sold_car)

        print('\033[0m')
        if find_sold_car:
            with open('sold_car_'+get_now()+'.json', 'w') as f:
                json.dump(new_car_list, f)
        else:
            pass        
        #=====================================================================

        # shared_items = {k: x[k] for k in x if k in y and x[k] == y[k]}
        # print len(shared_items)

        with open(self.json_file, 'w') as f:
            json.dump(car_info_list, f)


    def _convert_num(self, str_num):
        temp = ''.join(list(filter(str.isdigit, str_num)))
        return int(temp)

            

        



    

if __name__ == '__main__':
    main()