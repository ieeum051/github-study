# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime
from time import sleep
import datetime as dt
import sys
import json
import copy

RUN_FAST = 1

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
  cal.gen_total_summary()


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

    for stock in self.stock_list:
      self._print_stock_info_by_grp(stock, 'a')      
    print("----------------------")
    for stock in self.stock_list:
      self._print_stock_info_by_grp(stock, 'b')
    print("----------------------")

  def _print_stock_info_by_grp(self, stock, grp):
    if stock['grp'] == grp:
        gap_yesterday = stock['daily_asset'][0] - stock['daily_asset'][1]
        print("{:<8}{:>7}\t{:>5}".format(stock['name'],
                                    round(stock['daily_asset_var'][0], 1),
                                    round(gap_yesterday, 1)
                                  ))

  def gen_total_summary(self):
    summary = {'cur_val':0, 'gap_from_init' : 0, 'gap_from_yesterday': 0}
    summary_data = {
      'total': copy.deepcopy(summary),
      'a': copy.deepcopy(summary),
      'b': copy.deepcopy(summary)
     }
    cur_sum = 0
    cur_var_sum = 0

    for stock in self.stock_list:
      self._cal_total(summary_data['total'], stock)

      if stock['grp'] == 'a':
        self._cal_total(summary_data['a'], stock)

      if stock['grp'] == 'b':
        self._cal_total(summary_data['b'], stock)

    self._print_summary(summary_data['total'])
    self._print_summary(summary_data['a'])
    self._print_summary(summary_data['b'])

  def _cal_total(self, data, stock):
    data['cur_val'] += stock['daily_asset'][0]
    data['gap_from_init'] += stock['daily_asset_var'][0]
    data['gap_from_yesterday']  += \
      (stock['daily_asset'][0] - stock['daily_asset'][1])

  def _print_summary(self, data):
    print("{:<8}{:>7}\t{:>5}".format(round(data['cur_val'], 1), 
                        round(data['gap_from_init'], 1),
                        round(data['gap_from_yesterday'], 1)
                        ))








if __name__ == '__main__':
  main()
