# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime
from time import sleep
import datetime as dt
import sys
import json
import copy
import telegram

# ASCII Color Code
CR_MARGENTA = '\033[95m'
CR_YELLOW = '\033[93m'
CR_REVERT = '\033[0m'
CR_GREEN = '\033[92m'
CR_BLUE = '\033[94m'
CR_WHITE = '\033[37m'
#------
RUN_FAST = 0
DRAW_GRAPH = 0  # [0 / 1] or [False / True]
PRINT_TOTAL = 0

DRAW_GRAPH = 0
NUM_CRAWL_PAGES = 1

VALUE_UNIT = 10000
MINUTE_30 = 30*60


# for Telegram 
BOT_TOKEN = '1406855830:AAHxMrhLzNtKK8veSbxkAF2c9E3WH6clXkY'
TELE_ME = '1404750626'
SEND_MSG2TELEGRAM = 0


def set_options(opts):
  global CR_MARGENTA
  global CR_REVERT
  global CR_BLUE
  global PRINT_TOTAL
  global RUN_FAST
  global DRAW_GRAPH
  global NUM_CRAWL_PAGES
  global SEND_MSG2TELEGRAM
  
  for opt in opts:
    if opt == 'nocolor':
      CR_MARGENTA = CR_WHITE
      CR_REVERT = CR_WHITE
      CR_BLUE = CR_WHITE
    elif opt == 'fast':
      RUN_FAST = 1
      NUM_CRAWL_PAGES = 1 # fast시 draw를 1page로 제한. (일반적으로 저장하는 page크기가 1이다.)
    elif opt == 'draw':
      DRAW_GRAPH = 1
      NUM_CRAWL_PAGES = 6 # stock draw 시 4 page의 데이터를 그린다.
    elif opt == 'total':
      PRINT_TOTAL = 1
    elif opt == 'tf':
      RUN_FAST = 1
      PRINT_TOTAL = 1
    elif opt == 'df':
      DRAW_GRAPH = 1
      NUM_CRAWL_PAGES = 1      
      RUN_FAST = 1
    elif opt == 'telegram':
      SEND_MSG2TELEGRAM = 1
    else:
      pass
    

def get_opt():
  opt = []
  argv = sys.argv
  argv_cnt = len(argv)
  for i in range(argv_cnt):
    opt.append(argv[i])
  return opt

def activate_opt():
  # global 변수를 셋팅하고 StockAsset class에서 사용한다.
  # 차라리 option manager를 두면?? 
  set_options(get_opt())
  # set_no_color_by_opt(opt)
  # set_run_fast_by_opt(opt)
  # set_print_total_by_opt(opt)
  # set_draw_by_opt(opt)
  # set_run_fast_total_by_opt(opt)

def is_available_time():
    # 최초 1회는 수행하고 그 다음부터 수행여부를 시간 체크하여 판단하자.
    now = dt.datetime.now()
    now_hour = now.hour
    return True if(now_hour>= 9 and now_hour < 16) else False    


def run():
  sa = StockAssets()  # 1. 계좌 정보
  sri = StockRealInfo(sa.get_code_list()) # 2. 관련 주식 계좌 가격 이력 

  #3. 1, 2정보를 종합하여 현재 시점 및 그래프를 그릴 정보를 생성한다.
  cal = CalStockAsset(sa, sri) # 전체 계산 클래스
  cal.update_daily_price()

  if DRAW_GRAPH:
    render_chart(cal, sri.get_daily_index_list())
    return

  # mystocks.json에서 grp 정보 별로 데이터를 분류
  cal.merge_print_data_by_grp()


  if SEND_MSG2TELEGRAM:
    cal.send_telegram()
    return

  # grp별 데이터 출력
  cal.print_stock_info()

  # grp 별 및 전체 합산 데이터 출력
  cal.print_summary_info()



def main():
  activate_opt()

  first_flag = 1

  if not DRAW_GRAPH and not RUN_FAST:
      # for i in range(20):
      while 1:
        if is_available_time() or first_flag:
          run()
          first_flag = 0

        # 유효한 시간이 아니면 1회 수행하고 그만둔다.
        # TODO : 개장 시간이 아닐때 요청하면 파일 정보를 읽어보고 유효한지 파악한 후에 가져온다.
        # if not is_available_time(): return 
        sleep(MINUTE_30)
        
  else:
    run()


class StockAssets:
  def __init__(self):
    self.file_name = 'mystocks.json'
    self.stock_list = self._read_stock_json()


  def _read_stock_json(self):
    stock_list = []
    with open(self.file_name, 'r', encoding='UTF8') as f:
      stock_list = json.load(f)

    return stock_list

  def get_stock_list(self):
    return self.stock_list

  def get_code_list(self):
    code_list = []
    for stock in self.stock_list:
      code_list.append(stock['code'])
    
    return list(set(code_list))

class StockRealInfo:
  def __init__(self, code_list = None):
    self.total_df = None  # df <- dataframe
    if code_list != None:
      self.gen_dataFrame(code_list)

  def get_daily_price_list(self, code):
    return self.total_df[code].tolist()

  def get_daily_index_list(self):
    code = self.total_df.keys()[0]
    return self.total_df[code].index.tolist()

  def gen_dataFrame(self, stockCodes):
    """
    종목 코드들을 이용하여 시세를 받아온다.
    return: pandas Dataframe type
    """  
    dic_items = {}
    # print(stockCodes)

    for i in range(0, len(stockCodes)):
      df = self.get_currentValue(stockCodes[i])
      dic_items[stockCodes[i]] = df['종가'].values

    #날짜에서 연도를 제거
    date = []
    for d in df['날짜'].values:
      date.append( ''.join( [d.split('.')[1], d.split('.')[2]]))

    self.total_df = pd.DataFrame(dic_items, index=date)


  def get_currentValue(self, stock_code):
    """
    해당 종목의 날짜, 종가 정보만 이용한다.
    """  
    flag_read_csv = RUN_FAST
    url = self._get_url(stock_code)
    df = pd.DataFrame()

    for page in range(1, NUM_CRAWL_PAGES+1):
        folder_name = 'stock_info'
        file_name = folder_name + '/' + stock_code + '_stock_info.csv'

        if not flag_read_csv: # url로부터 정보를 얻어온다.
          pg_url = '{url}&page={page}'.format(url=url, page=page)
          saved_pd = pd.read_html(pg_url, header=0)[0]
          saved_pd.to_csv(file_name, mode='w')

        read_pd = pd.read_csv(file_name, index_col=0)
        df = df.append(read_pd, ignore_index=True)
    
    # df.dropna()를 이용해 결측값 있는 행 제거 
    df = df[['날짜','종가']]
    df = df.dropna() # 상위 5개 데이터 확인하기
    return df

  def _get_url(self, stock_code): 
    # 네이버 finance 정보를 이용한다. (crawling)
    return 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=stock_code)


class CalStockAsset:
  def __init__(self, stock_asset, stock_realinfo ):
    self.stock_asset = stock_asset        # StockAssets
    self.stock_realinfo = stock_realinfo  # StockRealInfo
    self.stock_list = self.stock_asset.get_stock_list()
    self.print_data = {}
    self.daily_revenu_sum_list =[]


  def get_daily_revenu_sum_list(self):
    return self.daily_revenu_sum_list

  def update_daily_price(self):  
    sum = []
    for stock in self.stock_list:
      code = stock['code']
      stock['daily_prc'] = self.stock_realinfo.get_daily_price_list(code)
      stock['daily_asset_var']  = []
      stock['daily_asset']  = []
      stock['daily_revenu']  = []

      for prc in stock['daily_prc']: # 최근 며칠간의 기록을 보관
        gap = prc - stock['init_p']
        stock['daily_asset_var'].append(
          gap * stock['cnt'] / VALUE_UNIT
        )
        stock['daily_asset'].append(
          prc * stock['cnt'] / VALUE_UNIT
        )
        stock['daily_revenu'].append(
          (prc - stock['init_p']) * stock['cnt'] / VALUE_UNIT
        )
      stock['gap_prev'] = stock['daily_asset'][0] - stock['daily_asset'][1]
      stock['init_val'] = (stock['init_p'] * stock['cnt']) / VALUE_UNIT

    # 수익 액수 그래프를 위한 데이터 생성. ( self.daily_revenu_sum_list )
    for i in range(len(self.stock_list[0]['daily_prc'])):
      self.daily_revenu_sum_list.append(0)
    
    for stock in self.stock_list:
      revenu_len = len(stock['daily_revenu'])
      for i in range(len(stock['daily_revenu'])):
        self.daily_revenu_sum_list[i] += stock['daily_revenu'][i]

  def merge_print_data_by_grp(self):
    merge_data_list = []

    # grp 정보를 모아서 중복되지 않게 리스트를 만든다.
    grp_list = sorted(list(set([stock['grp'] for stock in self.stock_list])))

    # grp 정보에 따라 grp 별로 stock 정보를 모은다.
    for grp in grp_list:
      self.print_data[grp] = [stock for stock in self.stock_list if stock['grp'] == grp]


  def print_stock_info(self):
    now_dt = dt.datetime.now()
    print("["+ str(now_dt.hour) + ":" + str(now_dt.minute) + "]")

    # 제일많은 element 수 확인
    # (가장 많은 grp의 element 수에 맞춰서 길이를 출력해야 한다.)
    grp_element_max_len = max([len(self.print_data[key]) for key in self.print_data.keys()])

    print_text = ''

    for i in range(grp_element_max_len):
      line_text = '| '

      # 그룹별 print 데이터 생성
      for grp in self.print_data.keys():
        if len(self.print_data[grp]) > i:
          stock = self.print_data[grp][i]
          line_text += (self.get_print_text(stock) +  ' | ')
        else:  # 왼쪽에 stock 정보가 없을때, 빈칸으로 띄어준다.
          if PRINT_TOTAL:
            line_text += ( '{:<36}'.format('')+  ' | ')
          else:
            line_text += ( '{:<29}'.format('')+  ' | ')
      print_text +=  (line_text + '\n')
    
    print(print_text, end='')

  def print_summary_info(self):
    # summary = {}
    # init_dict = {'cur_val': 0, 'gap_from_init': 0, 'gap_prev': 0, 'init_val': 0}

    # # make total data
    # summary['total'] = copy.deepcopy(init_dict)
    # for stock in self.stock_list:
    #   self._cal_total(summary['total'], stock)

    # # make group data
    # for grp in self.print_data.keys():
    #   summary[grp] = copy.deepcopy(init_dict)
    #   for stock in self.print_data[grp]:
    #     self._cal_total(summary[grp], stock)

    summary = self._get_summary()

    space = ''
    if PRINT_TOTAL:
      space = '       '
      

    # make print data
    line_text = '| '
    for grp in self.print_data.keys():
      
      line_text += self._get_summary_text(summary[grp]) + space + ' | '
    
    self.print_border()
    print(line_text)
    self.print_border()
    print('| ' + self._get_summary_text(summary['total']) )
    print()

  def send_telegram(self):
    """
    {'total': {'cur_val': 6302.3115, 'gap_from_init': 567.6899,
     'gap_prev': 19.71149999999993, 'init_val': 5734.6215999999995}, 
     'a': {'cur_val': 3662.72, 'gap_from_init': 80.1094, 
     'gap_prev': 2.2099999999999227, 'init_val': 3582.6106},
     'b': {'cur_val': 2639.5915, 'gap_from_init': 487.5805000000001,
     'gap_prev': 17.501500000000007, 'init_val': 2152.011}}
----------------
dict_keys(['total', 'a', 'b'])
    """
    summary = self._get_summary()

    msg = ''
    for grp in ['total', 'a', 'b']:
      grp_val = summary[grp]
      msg_sub = '{} ({}) : {}({}%), {}({}%)'.format(
          grp.upper(),
          round(grp_val['cur_val'], 1),
          round(grp_val['gap_from_init'], 1),
          round(grp_val['gap_from_init']*100/grp_val['init_val'], 1),
          round(grp_val['gap_prev'], 1),
          round(grp_val['gap_prev']*100 / (grp_val['cur_val']-grp_val['gap_prev']), 1)
      )
      msg += (msg_sub + '\n')

    print(msg)
    mybot = telegram.Bot(token = BOT_TOKEN)
    mybot.sendMessage(TELE_ME, msg)


  def _get_summary(self):
    summary = {}
    init_dict = {'cur_val': 0, 'gap_from_init': 0, 'gap_prev': 0, 'init_val': 0}

    # make total data
    summary['total'] = copy.deepcopy(init_dict)
    for stock in self.stock_list:
      self._cal_total(summary['total'], stock)

    # make group data
    for grp in self.print_data.keys():
      summary[grp] = copy.deepcopy(init_dict)
      for stock in self.print_data[grp]:
        self._cal_total(summary[grp], stock)

    return summary    



  def get_print_text(self, stock):
    rate = round((stock['daily_asset'][0]*100 / stock['init_val']) - 100, 1)
    daily_var = round(stock['daily_asset_var'][0], 1)
    gap_prev = round(stock['gap_prev'], 1)

    CR_TOTAL = CR_WHITE
    CR_RATE = CR_MARGENTA if rate > 0 else CR_BLUE
    CR_VAR = CR_MARGENTA if  daily_var > 0 else CR_BLUE
    CLR_GAP = CR_MARGENTA if gap_prev > 0 else CR_BLUE

    # if rate > 0 : rate = CR_MARGENTA + str(rate) + '%'
    # else: rate = CR_BLUE + str(rate) + '%'

    if PRINT_TOTAL:
      stock_total = round(stock['daily_asset'][0], 1)
      return '{:<7}{}{:>7}{}{:>7}%{}{:>8}{}{:>6}{}'.format(
                                      stock['name'], 
                                      CR_TOTAL, stock_total,
                                      CR_RATE, rate,
                                      CR_VAR, daily_var,
                                      CLR_GAP, gap_prev,
                                      CR_REVERT
        )


    return '{:<7}{}{:>7}%{}{:>8}{}{:>6}{}'.format(
                                    stock['name'], 
                                    CR_RATE, rate,
                                    CR_VAR, daily_var,
                                    CLR_GAP, gap_prev,
                                    CR_REVERT
      )
    
  def _get_summary_text(self, grp_data):

    total_asset = round(grp_data['cur_val'], 1)
    if not PRINT_TOTAL:
      total_asset = '----'

    rate = round((grp_data['cur_val']*100 / grp_data['init_val']) - 100, 1)

    daily_var = round(grp_data['gap_from_init'], 1)
    gap_prev = round(grp_data['gap_prev'], 1)

    cr_rate = CR_MARGENTA if rate > 0 else CR_BLUE
    cr_var = CR_MARGENTA if  daily_var > 0 else CR_BLUE
    cr_gap = CR_MARGENTA if gap_prev > 0 else CR_BLUE

    return '{:<7}{}{:>7}%{}{:>8}{}{:>6}{}'.format(
                                    total_asset,
                                    cr_rate, rate,
                                    cr_var, daily_var,
                                    cr_gap, gap_prev, CR_REVERT
    )

  def _cal_total(self, summary, stock):
    summary['init_val'] += stock['init_val']
    summary['cur_val'] += stock['daily_asset'][0]
    summary['gap_from_init'] += stock['daily_asset_var'][0]
    summary['gap_prev'] += (stock['daily_asset'][0] - stock['daily_asset'][1])

  def print_border(self):
    for key in self.print_data.keys():
      if PRINT_TOTAL:
        print('- - - - - - - - - - - - - - - - - - - -', end='')
      else:
        print('- - - - - - - - - - - - - - - -', end='')
        
    print()


def render_chart(calstockasset, date_index):
  # TOOD : date index에서 5일 단위로 값을 넣는다던지..

  plt.figure(1, figsize=(8,4))
  plt.title("My Graph")

  value_list = calstockasset.get_daily_revenu_sum_list()

  # value가 List다.
  plt.plot(date_index, value_list, c='seagreen', lw=2)
 
  # plt.legend(graphStyle.stockNames) 

  plt.xticks(rotation=45)
  plt.gca().invert_xaxis()
  plt.grid(True)

    
  # # 0 base line
  plt.axhspan(-0.1, 0.1, color='red' ) #, alpha=1)
  plt.show()


if __name__ == '__main__':
  main()
