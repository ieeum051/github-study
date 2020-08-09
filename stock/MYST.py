# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import pandas as pd
from datetime import datetime
from time import sleep
import datetime as dt
import sys

PRINT_TOTAL = 0

# TODO : 수익률을 반영한 GRAPH와 현재 수익금액을 반영한 GRAPH를 선택해서 사용할 수 있도록 하자. (혹은 동시 출력)
# 종목 변경시 변경 전 사항을 제대로 보기 어렵다. 예> 바닥 종목을 구입시 이전 가치가 높게 보여진다.
# -> 전체 수익 측면에서 기록을 유지할 필요가 있어 보인다.

DRAW_GRAPH = 0  # [0 / 1] or [False / True]

if DRAW_GRAPH:
  NUM_CRAWL_PAGES = 4
else:
  NUM_CRAWL_PAGES = 1

## class를 이용한 data indexing.
# Stock Info Class
DEPOSIT = 1
stockNames = ['TOTAL', 'K_GAS', 'K_GAS2',  "H_CAR", 'L_LIFE'] 
stockCodes =        [ "036460", "036460", "005380", "051905"]
num_stocks =        [  291,    211,    53, 15]
init_stockValue =   [ 41766,  33200,  124000, 732000]


class StockInfo:
  def __init__(self, stockCodes, num_stocks, init_stockValue):
    self.stockCodes = stockCodes
    self.num_stocks = num_stocks
    self.init_stockValue = init_stockValue

# Graph Style Class
VALUE_UNIT = 10000

LineColor=['bisque', 'seagreen', 'firebrick','maroon', 'navy']
LineWidth=[2, 1.4, 1.4, 1.4, 1]

class GraphStyle:
  def __init__(self, stockNames, LineColor, LineWidth):
    self.stockNames = stockNames
    self.LineColor = LineColor
    self.LineWidth = LineWidth

def run():
  
  # Initialize stock info. and  graph Style 
  stockInfo = StockInfo(stockCodes, num_stocks, init_stockValue)
  gStyle = GraphStyle(stockNames, LineColor, LineWidth)

  # Get price data frame using pandas
  total_df = gen_dataFrame(stockInfo.stockCodes)
  # print(total_df)

  # Manipulate data for making graph
  stock_revenue_list_byDay = calc_RevenueOfEachStocks(total_df, num_stocks, stockInfo.init_stockValue)

  # Calculate and merge total Revenue into stock value list.
  cal_and_insert_totalRevenue(stock_revenue_list_byDay)

  # Print Stock Info. in Terminal
  print_stock_value(stock_revenue_list_byDay, num_stocks, stockInfo.init_stockValue)
    
  # Render Graph using PyPlot
  if DRAW_GRAPH:
    render_chart(total_df.index.tolist(), stock_revenue_list_byDay, gStyle)


def gen_dataFrame(stockCodes):
  """
  종목 코드를 이용하여 시세를 받아온다.
  return: pandas Dataframe type
  """  
  dic_items = {}

  for i in range(0, len(stockCodes)):
    df = get_currentValue(stockCodes[i])
    dic_items[stockCodes[i]] = df['종가'].values

  #날짜에서 연도를 제거
  date = []
  for d in df['날짜'].values:
    date.append( ''.join( [d.split('.')[1], d.split('.')[2]]))

  total_df = pd.DataFrame(dic_items, index=date)
  return total_df

def get_currentValue(stockCodes):
  """
  해당 종목의 날짜, 종가 정보만 이용한다.
  """  
  url = get_url(stockCodes)
  df = pd.DataFrame()

  for page in range(1, NUM_CRAWL_PAGES+1):
      pg_url = '{url}&page={page}'.format(url=url, page=page)
      df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

  # df.dropna()를 이용해 결측값 있는 행 제거 
  df = df[['날짜','종가']]
  df = df.dropna() # 상위 5개 데이터 확인하기
  return df

def get_url(stockCodes): 
  """
  네이버 finance 정보를 이용한다. (crawling)
  return: url
  """  
  url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=stockCodes)
  return url 

def calc_RevenueOfEachStocks(total_df, num_stocks, init_stockValue):
  stock_list = []
  for code in stockCodes:
    stock_list.append( total_df[code].tolist() ) 

  for i in range(len(stock_list)):
    for j in range (len(stock_list[i])):
      stock_list[i][j] -= init_stockValue[i] # 초기값과의 차이..
      stock_list[i][j] *= num_stocks[i]  # 보유 주식수 고려
      stock_list[i][j] /= VALUE_UNIT   # 만원 단위  -- define으로 정리 필요???
  
  return stock_list


def cal_and_insert_totalRevenue(stock_revenue_list):
  total_revenue = []
  
  for i in range(len(stock_revenue_list[0])):
    sum = 0
    for j in range(len(stock_revenue_list)):
      sum += stock_revenue_list[j][i]
      
    total_revenue.append(sum)

  stock_revenue_list.insert(0, total_revenue)


def check_total_balance():
  # 임시 확인 코드 -- start
  if len(sys.argv) > 1 : return
  a = datetime.today().day
  if(a > 2 and a < 8):
    print('###### Check Your Balance!!')
    print('###### Buy KODEX200!!')
    print('###### Check 300 thousand won in HanaBank')
  # 임시 확인 코드 -- end


def print_list_with_format(target_list):
    # 0:<9 : left alignment with maximum 9 white spaces
    print_format = '' .join('{0:<9}'.format(k) for k in target_list)
    print ("[ "+ print_format +"]")

def print_stock_value(stock_revenue_list_byDay, num_stocks, init_stockValue):
  """
  현재 종목당 자산가치 + 수익 표시 in Terminal
  """
  round = lambda x:int(x+1) if (x-int(x))>0.5 else int(x)
  round_below_decimalPoint = lambda x:int(x*10+1)/10 if (x*10-int(x*10))>0.5 else int(x*10)/10
  
  now_dt = dt.datetime.now()


  print("["+ str(now_dt.hour) + ":" + str(now_dt.minute) + "]" + \
    "        p: " + str(round_below_decimalPoint(stock_revenue_list_byDay[0][0] - stock_revenue_list_byDay[0][1])) )  
  today_evaluation_list = []

  for i in range(len(num_stocks)):
    today_evaluation_list.append(num_stocks[i]*init_stockValue[i]/VALUE_UNIT +  stock_revenue_list_byDay[i+1][0])
  
  today_evaluation_list.insert(0, sum(today_evaluation_list) + DEPOSIT  )

  # list를 정수로 : list(map(int, myList)),  lambda 함수를 이용하여 반올림 구현.
  # (현재 주가) a
  # (수익률) 표시.
  if PRINT_TOTAL:
    print_list_with_format( list(map(round, today_evaluation_list)) ) # 현재 자산 (현재 주가)

  today_revenue_list = []

  for i in range(len(stock_revenue_list_byDay)):
    today_revenue_list.append(stock_revenue_list_byDay[i][0])
  
  print_list_with_format( list(map(round, today_revenue_list)) ) # 수익


  # 초기 매입 총액을 계산한다. (궂이 여기서 계산해야하나???)
  init_evaluation = []
  init_total = 0
  for i in range(len(num_stocks)):
    init_total += num_stocks[i]*init_stockValue[i] / VALUE_UNIT
    init_evaluation.append(num_stocks[i]*init_stockValue[i] / VALUE_UNIT)
  init_evaluation.insert(0,init_total+DEPOSIT)

  per = []
  for i in range(len(init_evaluation)):
    # per.append(today_revenue_list[i]*100/ today_evaluation_list[i]) # 매입 가치로 계산 해야함.
    per.append(today_revenue_list[i]*100/ init_evaluation[i]) # 매입 가치로 계산 해야함.

    # 매입가치는 
#     num_stocks =        [67,       291,        53]
# init_stockValue =   [130500,   41766,    124000]

  print_list_with_format( list(map( lambda x: float("%0.2f"%x), per)) ) # 수익률

  print(" ----------------------------------------------")

  check_total_balance()


def render_chart(dateIndex, value, graphStyle):
  # TOOD : date index에서 5일 단위로 값을 넣는다던지..

  plt.figure(1, figsize=(8,4))
  plt.title("My Graph")

  # value가 List다.
  for i in range(len(value)):
    plt.plot(dateIndex, value[i], c=graphStyle.LineColor[i], lw=graphStyle.LineWidth[i])
 
  plt.legend(graphStyle.stockNames) 

  plt.xticks(rotation=45)
  plt.gca().invert_xaxis()
  plt.grid(True)

    
  # 0 base line
  plt.axhspan(-0.1, 0.1, color='red' ) #, alpha=1)
  plt.show()
  

if __name__ == "__main__" :
  if not DRAW_GRAPH:
    for i in range(20):
      run()
      sleep(30*60)
  run()

