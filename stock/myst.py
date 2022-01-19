# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
from time import sleep
import datetime as dt
import sys

from pytz import timezone

# Local Class
from stocklib.calstockasset import CalStockAsset
from stocklib.stockassets import StockAssets
from stocklib.stockrealinfo import StockRealInfo
from stocklib.rendergraph import RenderGraph
from stocklib.rendertext import RenderText
from stocklib.rendertelegram import RenderTelegram

RUN_FAST = 0  # 웹페이지 로딩없이 로딩된 자료를 기반으로 수행
DRAW_GRAPH = 0  # [0 / 1] or [False / True]
PRINT_TOTAL = 0 

NUM_CRAWL_PAGES = 1
NO_TEXT_COLOR = 0

TELEGRAM_BOT = 0
MINUTE_30 = 30*60

def main():
  activate_opt()
  first_flag = 1

  if not DRAW_GRAPH and not RUN_FAST:
      while True:
        if is_available_time() or first_flag:
          run_stock_monitor_and_renderer()
          first_flag = 0

        sleep(MINUTE_30)
  else:
    run_stock_monitor_and_renderer()

def activate_opt():
  set_options(get_opt())

def set_options(opts):
  global PRINT_TOTAL
  global RUN_FAST
  global DRAW_GRAPH
  global NUM_CRAWL_PAGES
  global TELEGRAM_BOT
  global MINUTE_30
  global DATA_JSON
  global NO_TEXT_COLOR
  
  for opt in opts:
    if opt == 'nocolor':
      NO_TEXT_COLOR = 1
    elif opt == 'fast':
      RUN_FAST = 1
      NUM_CRAWL_PAGES = 1 # fast시 draw를 1page로 제한. (일반적으로 저장하는 page크기가 1이다.)
    elif opt == 'draw':
      DRAW_GRAPH = 1
      NUM_CRAWL_PAGES = 12 # stock draw 시 4 page의 데이터를 그린다.
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
      TELEGRAM_BOT = 1
    elif opt == 'freq':
      MINUTE_30 = 20*60
    elif opt == 'namu':
      DATA_JSON = 'stock2.json'
    else:
      pass

def get_opt():
  opt = []
  argv = sys.argv
  argv_cnt = len(argv)
  for i in range(argv_cnt):
    opt.append(argv[i])
  return opt

def is_available_time():
    now = dt.datetime.now(timezone('Asia/Seoul'))
    now_hour = now.hour

    return True if(now_hour>= 9 and now_hour < 16) else False    

def run_stock_monitor_and_renderer():
  stock_asset = StockAssets()
  stock_real_info = StockRealInfo(stock_asset.get_code_list(), 
                    {'run_fast': RUN_FAST, 'num_crawl_pages': NUM_CRAWL_PAGES}) 

  cal_stock_asset = CalStockAsset(stock_asset, stock_real_info) # 전체 계산 클래스
  cal_stock_asset.update_daily_price()

  # Render
  render = RenderText(cal_stock_asset, {'is_print_total': PRINT_TOTAL, 'nocolor': NO_TEXT_COLOR })
  render.draw()  
  
  if DRAW_GRAPH:
    render = RenderGraph(cal_stock_asset)
    render.draw()
    return

  if TELEGRAM_BOT:
    render = RenderTelegram(cal_stock_asset)
    render.draw()    
    return

if __name__ == '__main__':
  main()
