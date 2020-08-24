import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time
import datetime


INTERVAL = 30
LOAD_WEB_PAGE = 1
OUTPUT_PATH = './output/'
# CHROME_PATH = '/usr/local/bin/chromedriver'
CHROME_PATH = '../../chromedriver'

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
        self.json_file = 'encar_list.json'

        if LOAD_WEB_PAGE:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

            self.driver = webdriver.Chrome(executable_path=CHROME_PATH,
                                        chrome_options=chrome_options)
        # self.driver.implicitly_wait(3)

    def send_msg(self, year="", km="", price=""):
        url1 = "https://maker.ifttt.com/trigger/new_car_arrived/with/key/dQ2HNeN_GmArjr6OAkLru6"
        requests.post(url1, data={"value1": year + ' 엔카', "value2":km, "value3": price})


    def run(self):
        for i in range(10000):
            print('\n'+ '\033[93m' + 'Run Crawling at {}'.format(get_now()) + '\033[0m')
            self.gen_car_info_list()
            time.sleep(60*INTERVAL)

    def _set_url_list(self):
        self.url_list = [
            'http://www.encar.com/dc/dc_carsearchlist.do?carType=kor#!%7B%22action%22%3A%22(And.Mileage.range(..50000)._.Price.range(3000..4000)._.Year.range(201800..)._.Hidden.N._.(C.CarType.Y._.(C.Manufacturer.%ED%98%84%EB%8C%80._.(C.ModelGroup.%EA%B7%B8%EB%9E%9C%EC%A0%80._.Model.%EA%B7%B8%EB%9E%9C%EC%A0%80%20IG%20%ED%95%98%EC%9D%B4%EB%B8%8C%EB%A6%AC%EB%93%9C.)))_.Options.%ED%81%AC%EB%A3%A8%EC%A6%88%20%EC%BB%A8%ED%8A%B8%EB%A1%A4(%EC%96%B4%EB%8C%91%ED%8B%B0%EB%B8%8C_)._.Options.%EC%B0%A8%EC%84%A0%EC%9D%B4%ED%83%88%20%EA%B2%BD%EB%B3%B4%20%EC%8B%9C%EC%8A%A4%ED%85%9C(LDWS_)._.(Or.Color.%EC%A5%90%EC%83%89._.Color.%ED%9D%B0%EC%83%89._.Color.%EC%A7%84%EC%A3%BC%EC%83%89._.Color.%EC%B2%AD%EC%83%89._.Color.%EA%B0%88%EC%83%89.))%22%2C%22toggle%22%3A%7B%7D%2C%22layer%22%3A%22%22%2C%22sort%22%3A%22ModifiedDate%22%2C%22page%22%3A1%2C%22limit%22%3A%2250%22%7D'
            # 'http://www.encar.com/dc/dc_carsearchlist.do?carType=kor#!%7B%22action%22%3A%22(And.Hidden.N._.(C.CarType.Y._.(C.Manufacturer.%EA%B8%B0%EC%95%84._.(C.ModelGroup.%EC%8F%98%EB%A0%8C%ED%86%A0._.Model.%EB%8D%94%20%EB%89%B4%20%EC%8F%98%EB%A0%8C%ED%86%A0.)))_.FuelType.%EA%B0%80%EC%86%94%EB%A6%B0._.Options.%ED%81%AC%EB%A3%A8%EC%A6%88%20%EC%BB%A8%ED%8A%B8%EB%A1%A4(%EC%96%B4%EB%8C%91%ED%8B%B0%EB%B8%8C_)._.Options.%EC%B0%A8%EC%84%A0%EC%9D%B4%ED%83%88%20%EA%B2%BD%EB%B3%B4%20%EC%8B%9C%EC%8A%A4%ED%85%9C(LDWS_).)%22%2C%22toggle%22%3A%7B%7D%2C%22layer%22%3A%22%22%2C%22sort%22%3A%22ModifiedDate%22%2C%22page%22%3A1%2C%22limit%22%3A%2250%22%7D'
            # 'http://www.encar.com/dc/dc_carsearchlist.do?carType=kor#!%7B%22action%22%3A%22(And.Year.range(201800..)._.Price.range(2000..3000)._.Mileage.range(..60000)._.Hidden.N._.FuelType.%EB%94%94%EC%A0%A4._.Options.%EC%B0%A8%EC%84%A0%EC%9D%B4%ED%83%88%20%EA%B2%BD%EB%B3%B4%20%EC%8B%9C%EC%8A%A4%ED%85%9C(LDWS_)._.Options.%ED%81%AC%EB%A3%A8%EC%A6%88%20%EC%BB%A8%ED%8A%B8%EB%A1%A4(%EC%96%B4%EB%8C%91%ED%8B%B0%EB%B8%8C_)._.(C.CarType.Y._.(C.Manufacturer.%EA%B8%B0%EC%95%84._.(C.ModelGroup.%EC%8F%98%EB%A0%8C%ED%86%A0._.(C.Model.%EB%8D%94%20%EB%89%B4%20%EC%8F%98%EB%A0%8C%ED%86%A0._.BadgeGroup.%EB%94%94%EC%A0%A4%202WD.))))_.(Or.Color.%EC%A5%90%EC%83%89._.Color.%EC%9D%80%EC%83%89._.Color.%ED%9D%B0%EC%83%89._.Color.%EC%A7%84%EC%A3%BC%EC%83%89._.Color.%EA%B0%88%EC%83%89._.Color.%EC%B2%AD%EC%83%89._.Color.%EB%8B%B4%EB%85%B9%EC%83%89.)_.Trust.Inspection.)%22%2C%22toggle%22%3A%7B%224%22%3A0%7D%2C%22layer%22%3A%22%22%2C%22sort%22%3A%22ModifiedDate%22%2C%22page%22%3A1%2C%22limit%22%3A%2250%22%7D'
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
        temp_html_file = 'encar_html.html'        
        if LOAD_WEB_PAGE:
            html = ''
            for i in range(len(self.url_list)):
                self.driver.get(self.url_list[i])
                html += self.driver.page_source

            with open(temp_html_file, 'w') as f:
                f.write(html)
        
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

        key_cnt = len(car_info_list[0].keys())
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
                print('\033[95m')  # 자주색
                print(new_car['etc'])
                print('-----------------------')
                self.send_msg(new_car['year'], new_car['km'], new_car['price'])
                new_car_list.append(new_car)

        print('\033[0m')

        if find_new_car:
            # self.send_msg('새차가 들어왔다.')
            with open(OUTPUT_PATH+'new_encar_'+get_now()+'.json', 'w') as f:
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
                print('\033[92m')  # 초록색
                print(sold_car['etc'])
                print('-----------------------')
                sold_car_list.append(sold_car)

        print('\033[0m')
        if find_sold_car:
            # self.send_msg('팔린 차들이 있다.')
            with open(OUTPUT_PATH+'sold_encar_'+get_now()+'.json', 'w') as f:
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