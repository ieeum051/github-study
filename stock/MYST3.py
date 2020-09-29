# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime
from time import sleep
import datetime as dt
import sys
import json
import copy
# import 

RUN_FAST = 0

DRAW_GRAPH = 0  # [0 / 1] or [False / True]

if DRAW_GRAPH:
  NUM_CRAWL_PAGES = 4
else:
  NUM_CRAWL_PAGES = 1

VALUE_UNIT = 10000  

def main():
  # print("▲ ▼")
  # sys.exit()
  if len(sys.argv) > 1 :
      if sys.argv[1] == 'fast':
        global RUN_FAST
        RUN_FAST = 1

  sa = StockAssets()  # 계좌 정보
  # code_list = sa.get_code_list()
  sri = StockRealInfo(sa.get_code_list()) # 관련 주식 계좌 가격 이력 
  
  # print( sri.get_daily_price_list('036460') )
  cal = CalStockAsset(sa, sri) # 전체 계산 클래스
  cal.update_daily_price()
  cal.merge_print_data_by_grp()
  cal.print_stock_info()
  # cal.gen_total_summary()
  cal.print_summary_info()


class StockAssets:
  def __init__(self):
    self.stock_list = self._read_stock_json()

  def _read_stock_json(self):
    stocks_file = 'mystocks.json'

    stock_list = []
    with open(stocks_file, 'r', encoding='UTF8') as f:
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
    self.total_df = None
    if code_list != None:
      self.gen_dataFrame(code_list)

  def get_daily_price_list(self, code):
    return self.total_df[code].tolist()

  def gen_dataFrame(self, stockCodes):
    """
    종목 코드를 이용하여 시세를 받아온다.
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
    self.stock_asset = stock_asset
    self.stock_realinfo = stock_realinfo
    self.stock_list = self.stock_asset.get_stock_list()
    self.print_data = {}

    self.sum_list = {}

  # def calc_RevenueOfEachStocks(self):
  def update_daily_price(self):  
    for stock in self.stock_list:
      code = stock['code']
      stock['daily_prc'] = self.stock_realinfo.get_daily_price_list(code)
      stock['daily_asset_var']  = []
      stock['daily_asset']  = []
      for prc in stock['daily_prc']: # 최근 며칠간의 기록을 보관
        gap = prc - stock['init_p']
        stock['daily_asset_var'].append(
          gap * stock['cnt'] / VALUE_UNIT
        )
        stock['daily_asset'].append(
          prc * stock['cnt'] / VALUE_UNIT
        )
      
      stock['gap_prev'] = stock['daily_asset'][0] - stock['daily_asset'][1]
      stock['init_val'] = (stock['init_p'] * stock['cnt']) / VALUE_UNIT
    

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
    grp_element_max_len = max([len(self.print_data[key]) for key in self.print_data.keys()])

    print_text = ''
    for i in range(grp_element_max_len):
      line_text = '| '
      for grp in self.print_data.keys():
        if len(self.print_data[grp]) > i:
          stock = self.print_data[grp][i]
          line_text += (self.get_print_text(stock) +  ' | ')
        else:
          line_text += ( '{:<28}'.format('')+  ' | ')
      print_text +=  (line_text + '\n')
    
    print(print_text, end='')


  def print_summary_info(self):
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


    # make print data
    line_text = '| '
    for grp in self.print_data.keys():
      line_text += self._get_summary_text(summary[grp]) + ' | '
    
    self.print_border()
    print(line_text)
    self.print_border()
    print('| ' + self._get_summary_text(summary['total']) )


  def get_print_text(self, stock):
    # gap_yesterday = stock['daily_asset'][0] - stock['daily_asset'][1]
    # init_asset = (stock['init_p'] * stock['cnt']) / VALUE_UNIT
    rate = round((stock['daily_asset'][0] / stock['init_val']) - 1, 2)
    return '{:<8}{:>7}{:>7}{:>6}'.format(stock['name'], rate,
                                    round(stock['daily_asset_var'][0], 1),
                                    round(stock['gap_prev'], 1)
    )
    
  def _get_summary_text(self, grp_data):
    rate = round((grp_data['cur_val'] / grp_data['init_val']) - 1, 2)
    return '{:<8}{:>7}{:>7}{:>6}'.format(
                                    round(grp_data['cur_val'], 1),
                                    rate,
                                    round(grp_data['gap_from_init'], 1),
                                    round(grp_data['gap_prev'], 1)
    )


  def _cal_total(self, summary, stock):
    summary['init_val'] += stock['init_val']
    summary['cur_val'] += stock['daily_asset'][0]
    summary['gap_from_init'] += stock['daily_asset_var'][0]
    summary['gap_prev'] += (stock['daily_asset'][0] - stock['daily_asset'][1])



  def print_border(self):
    for key in self.print_data.keys():
      print('- - - - - - - - - - - - - - - -', end='')
    print()


  # def gen_total_summary(self):
  #   summary = {'cur_val':0, 'gap_from_init' : 0, 'gap_from_yesterday': 0}
  #   summary_data = {
  #     'total': copy.deepcopy(summary),
  #     'a': copy.deepcopy(summary),
  #     'b': copy.deepcopy(summary)
  #    }
  #   cur_sum = 0
  #   cur_var_sum = 0

  #   for stock in self.stock_list:
  #     self._cal_total(summary_data['total'], stock)

  #     if stock['grp'] == 'a':
  #       self._cal_total(summary_data['a'], stock)

  #     if stock['grp'] == 'b':
  #       self._cal_total(summary_data['b'], stock)

  #   print('--------------------------------------------')
  #   self._print_summary(summary_data['total'])
  #   self._print_summary(summary_data['a'])
  #   self._print_summary(summary_data['b'])

  # # def _cal_total(self, data, stock):
  # #   data['cur_val'] += stock['daily_asset'][0]
  # #   data['gap_from_init'] += stock['daily_asset_var'][0]
  # #   data['gap_from_yesterday']  += \
  # #     (stock['daily_asset'][0] - stock['daily_asset'][1])

  # def _print_summary(self, data):
  #   print("{:<8}{:>7}\t{:>5}".format(round(data['cur_val'], 1), 
  #                       round(data['gap_from_init'], 1),
  #                       round(data['gap_from_yesterday'], 1)
  #                       ))








if __name__ == '__main__':
  main()
