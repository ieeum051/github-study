import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time
import datetime
import sys

OUTPUT_PATH = './output/'
CHROME_PATH = '/usr/local/bin/chromedriver'
# CHROME_PATH = '../../chromedriver'
LOAD_WEB_PAGE = 1

# from pyvirtualdisplay import Display

def get_now():
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    return nowDatetime

def get_today():
    now =datetime.datetime.now()
    return '{}.{}.{}'.format(now.year, now.month, now.day)



def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'fileread':
        global LOAD_WEB_PAGE
        LOAD_WEB_PAGE = 0

    UsedCar().run()


class UsedCar:
    def __init__(self):
        self._set_url_list()
        self.json_file = 'kcar_list.json'
        self.new_car_file = 'new_kcar_list.json'
        self.html_tmp = 'kcar_temp.html'

        if LOAD_WEB_PAGE:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--window-size=1920,2160")
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

            self.driver = webdriver.Chrome(executable_path=CHROME_PATH,
                                        chrome_options=chrome_options)
        # self.driver.implicitly_wait(3)
    def run(self):
        for i in range(10000):
            print('\n'+ '\033[93m' + 'Run Crawling at {}'.format(get_now()) + '\033[0m')
            try:
                self.gen_car_info_list()
            except:
                pass
            time.sleep(60*60)

    def _set_url_list(self):
        self.url_list = [
            'https://www.kcar.com/car/search/car_search_list.do'
        ]

    def send_msg(self, year="", km="", price=""):
        # 등록된 핸드폰으로 신차 정보 전송 (자세한 내용은 ifttt 검색해볼 것)
        url1 = "https://maker.ifttt.com/trigger/new_saved_carrrived/with/key/dQ2HNeN_GmArjr6OAkLru6"
        requests.post(url1, data={"value1": year + " 케이카", "value2":km, "value3": price})

    def get_car_info_list(self):
        try:
            with open(self.json_file, 'r') as f:
                car_list = json.load(f)
        except:
            return []

        return car_list

    def print_car_info(self, car_info_list):
        for car_info in car_info_list:
            arrived = 0 if 'arrived' not in car_info.keys() else car_info['arrived']
            print('{} / {} / {} / {}'.format(car_info['price'], car_info['year'], car_info['km'], arrived))

        # 이게 왜 필요했을까?
        # car_info_list = list(map(dict, set(tuple(sorted(d.items())) for d in car_info_list)))
        # print('-- 중복을 제거한 갯수 : ', len(car_info_list))

    def gen_car_info_list(self):
        if LOAD_WEB_PAGE:
            self._request_car_info()

        car_info_list = self._parse_car_info()
   
        self._check_sold_new_car_info(car_info_list)
        self.print_car_info(car_info_list)
        # print(car_info_list[0])
        with open(self.json_file, 'w') as f:
            json.dump(car_info_list, f)


    def _request_car_info(self):
        """ web에서 원하는 정보를 얻기 위해 page를 조작(각종 메뉴 클릭)하고 html_tmp 파일에 저장한다.
        """
        # xpath 정보는 chrome F11에서 확인 가능
        xpath_dict = {
    'car_type':  # 대형차
        "/html/body/div[2]/section/div[2]/form[2]/section[1]/div[3]/div[1]/div[1]/div/div/label[5]",
    'car_company':  # 현대
        "/html/body/div[2]/section/div[2]/form[2]/section[1]/div[3]/div[1]/div[2]/div/div/div[1]/ul/li[1]/label",
    'car_name':  # 그랜저
        "/html/body/div[2]/section/div[2]/form[2]/section[1]/div[3]/div[1]/div[2]/div/div/div[1]/ul/li/ul/li[1]/label",
    'car_name2': # 그랜저IG 
        "/html/body/div[2]/section/div[2]/form[2]/section[1]/div[3]/div[1]/div[2]/div/div/div[1]/ul/li/ul/li/ul/li[4]/label",

    # 아래는 그랜저IG 세부 모델 이나. 잘 선택이 안됨.  ~ li[13] 만 선택이 됨. 왜?
    'car_name3': # 2.4 프리미엄
        "/html/body/div[2]/section/div[2]/form[2]/section[1]/div[3]/div[1]/div[2]/div/div/div[1]/ul/li/ul/li/ul/li[4]/ul/li[2]/label",
    'car_name4': # 2.4 익스클루시브 스페셜
        "/html/body/div[2]/section/div[2]/form[2]/section[1]/div[3]/div[1]/div[2]/div/div/div[1]/ul/li/ul/li/ul/li[4]/ul/li[13]/label",
    'car_name5': # 2.4 스페셜
        "/html/body/div[2]/section/div[2]/form[2]/section[1]/div[3]/div[1]/div[2]/div/div/div[1]/ul/li/ul/li/ul/li[4]/ul/li[17]/label",

    'color_sel': # 색상 선택
        "/html/body/div[2]/section/div[2]/form[2]/section[1]/div[3]/div[1]/div[6]/h3/button",
    'color_gray':  # 쥐색
        "/html/body/div[2]/section/div[2]/form[2]/section[1]/div[3]/div[1]/div[6]/div/ul/li[5]/label",
    'color_silver': # 은색
        "/html/body/div[2]/section/div[2]/form[2]/section[1]/div[3]/div[1]/div[6]/div/ul/li[6]/label",
    'color_silver_gray':  # 은회색
        "/html/body/div[2]/section/div[2]/form[2]/section[1]/div[3]/div[1]/div[6]/div/ul/li[7]/label",

    'car_year_sel': # 연식 선택
        "/html/body/div[2]/section/div[2]/form[2]/section[1]/div[3]/div[1]/div[3]/div/div[1]",
    'car_year': # 2018 이상
        "/html/body/div[2]/section/div[2]/form[2]/section[1]/div[3]/div[1]/div[3]/div/div[1]/div[3]/div/ul/li[4]",

    'car_km_se': # 키로수 선택
        "/html/body/div[2]/section/div[2]/form[2]/section[1]/div[3]/div[1]/div[4]/div/div[2]",
    'car_km': # 5만키로 까지
        "/html/body/div[2]/section/div[2]/form[2]/section[1]/div[3]/div[1]/div[4]/div/div[2]/div[3]/div/ul/li[6]",

    'car_opt': # 차량 옵션 선택
        "/html/body/div[2]/section/div[2]/form[2]/section[1]/div[3]/div[1]/div[9]",
    'car_opt_btn': # 추가 옵션 선택
        "/html/body/div[2]/section/div[2]/form[2]/section[1]/div[3]/div[1]/div[9]/div/button",
    'car_opt_ldws': # LDWS (차선 유지 보조)
        "/html/body/div[2]/section/div[2]/form[2]/section[1]/div[3]/div[1]/div[9]/section/div[2]/ul/li[3]/ul/li[17]",
    'car_opt_confirm': # 선택
        "/html/body/div[2]/section/div[2]/form[2]/section[1]/div[3]/div[1]/div[9]/section/div[3]/button[2]",
        }
        self.driver.get(self.url_list[0])

        for key in xpath_dict.keys():
            # print ('check {}'.format(key))
            if key == 'car_opt':
                self.driver.execute_script("window.scrollTo(0, 1000)") 
                self.driver.implicitly_wait(3)

            xpath = xpath_dict[key]
            self.driver.find_element_by_xpath(xpath).click()
            self.driver.implicitly_wait(3)

            if key == 'car_opt' : time.sleep(3)

        # 스크린 캡쳐
        # a. 캡쳐하기 전에 옵션 정보를 보기 위해 스크롤을 상단으로 올림.
        self.driver.execute_script("window.scrollTo(0, 0)") 
        time.sleep(3)

        # b. 캡쳐 
        self.driver.save_screenshot('kcar.png') 

        # html page 저장 (디버그 용)
        html = self.driver.page_source
        with open(self.html_tmp, 'w') as f:
            f.write(html)

    
    def _parse_car_info(self):
        """ temp_html 파일을 읽어서 parsing한다.
        """
        html = ''
        with open(self.html_tmp, 'r') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')

        car_list = soup.find_all('li')

        car_info_list = []
        
        for car in car_list:
            car_info = {
                'state': None,
                'name': None,
                'type': None,
                'year': None,
                'km': None,
                'region': None,
                'price': None,
                'desc':'',
                'summary':None,                
                }

            find_flag = False
            for element in car.find_all('div'):
                if str(element).find('class=\"car_cont_box\"') == -1 or \
                    str(element).find('그랜저 IG') == -1 or \
                    str(element).find('2.4') == -1:
                        continue

                find_flag = True
                for elmt in element.find_all('span'):
                    if str(elmt).find('월식') > 0:
                        car_info['year'] = elmt.text
                        continue

                    if str(elmt).find('class=\"cash\"') > 0:
                        car_info['price'] = self._convert_num(elmt.text)
                        if car_info['price'] > 3300 or car_info['price'] < 2500:
                            find_flag = False
                            break
                        continue

                    if str(elmt).find('km') > 0:
                        car_info['km'] = self._convert_num(elmt.text)
                        continue

                    if str(elmt).find('ui_tooltip') > 0:
                        car_info['desc'] += elmt.text
                        continue

            if find_flag:
                car_info_list.append(car_info)

        return car_info_list

    def _is_same_car(self, saved_car, current_car ):
        if 'arrived' not in saved_car: # saved_car (saved_car 정보가 최신 차 정보가 없다면..)
            return False

        if saved_car['price'] == current_car['price'] and \
            saved_car['km'] == current_car['km'] and \
            saved_car['year'] == current_car['year']:
            return True
        return False

    def _check_sold_new_car_info(self, car_info_list):
        """ 신차 정보나 팔린 차 정보를 확인하고 msg를 송출한다.
        """
        MARGENTA_COLOR = '\033[95m'
        REVERT_COLOR = '\033[0m'
        GREEN_COLOR = '\033[92m'
        saved_car_info_list = self.get_car_info_list()

        find_new_car = False
        find_sold_car = False

        # 0. 기존 정보와 비교하여 등록일자 추가하기
        for car_info in car_info_list:
            for saved_car in saved_car_info_list:
                if self._is_same_car(saved_car, car_info):
                    car_info['arrived'] = saved_car['arrived']

        key_cnt = len(car_info_list[0].keys())
        
        # 1. 신차 확인
        print('[ New Cars ]')
        new_car_list = []
        for new_car in car_info_list:
            flag_same_info = False
            for pre_car in saved_car_info_list:
                # 새로운 정보와 기존 정보가 공유하는 차량이 새로운 정보의 갯수와 동일하면 flag_same_info = True
                shared_items = {k: new_car[k] for k in new_car if k in pre_car and new_car[k] == pre_car[k]}
                if len(shared_items) == key_cnt:
                    flag_same_info = True
            if not flag_same_info:
                find_new_car = True
                new_car['arrived'] = get_today()
                print(MARGENTA_COLOR)
                self.print_info(new_car)
                print("---------------------------------------")
                self.send_msg(new_car['year'], new_car['km'], new_car['price'])
                new_car_list.append(new_car)

        print(REVERT_COLOR)

        if find_new_car:
            with open(OUTPUT_PATH+'new_kcar_'+get_now()+'.json', 'w') as f:
                json.dump(new_car_list, f)
        else:
            pass

        # 2. 팔린 차 확인
        print('[ Sold Cars ]')
        sold_car_list = []
        for sold_car in saved_car_info_list:
            flag_same_info = False
            for pre_car in car_info_list: # saved_car_info_list
                # 새로운 정보와 기존 정보가 공유하는 차량이 새로운 정보의 갯수와 동일하면 flag_same_info = True
                shared_items = {k: sold_car[k] for k in sold_car if k in pre_car and sold_car[k] == pre_car[k]}
                if len(shared_items) == key_cnt:
                    flag_same_info = True
            if not flag_same_info:
                find_sold_car = True
                print(GREEN_COLOR)
                # print(sold_car['etc'])
                self.print_info(sold_car)
                print("---------------------------------------")
                sold_car_list.append(sold_car)

        print(REVERT_COLOR)
        if find_sold_car:
            with open(OUTPUT_PATH+'new_kcar_'+get_now()+'.json', 'w') as f:
                json.dump(new_car_list, f)
        else:
            pass

    def _convert_num(self, str_num):
        # 숫자 스트링 정보를 숫자로 변환
        temp = ''.join(list(filter(str.isdigit, str_num)))
        return int(temp)


    def print_info(self, car_info):
        print("{}  /  {}  / {}".format(car_info['price'], car_info['year'], car_info['km']))
        print("---------------------------------------")
        print(car_info['desc'])

if __name__ == '__main__':
    main()
