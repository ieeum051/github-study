
from selenium import webdriver
import numpy as np
import pandas as pd

CHROME_PATH = '/usr/local/bin/chromedriver'

class StockRealInfo:
  """ generate current state of stock after receiving from URL

  Attributes:
    total_df : received from URL and converted format data for prining
    opt : receive_from_url, number_of_crawled_pages
    driver : pre-set webdriver from selenium

  """
  def __init__(self, code_list = None, opt = None):
    self.total_df = None  # df <- dataframe
    self.opt = opt

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,2160")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    self.driver = webdriver.Chrome(executable_path=CHROME_PATH,
                                        chrome_options=chrome_options)
    if code_list != None:
      self.gen_dataFrame(code_list)


  def get_daily_price_list(self, code):
    return self.total_df[code].tolist()

  def get_daily_index_list(self):
    code = self.total_df.keys()[0]
    return self.total_df[code].index.tolist()

  def gen_dataFrame(self, stockCodes):
    """
    Using stock code, receive current state

    return: pandas Dataframe type
    """  
    dic_items = {}

    for i in range(0, len(stockCodes)):
      df = self._receive_currentValue(stockCodes[i])
      dic_items[stockCodes[i]] = df['종가'].values

    #날짜에서 연도를 제거
    date = []
    index = 0
    for d in df['날짜'].values:
      index += 1
      date.append( ''.join( [d.split('.')[1], d.split('.')[2]]))

    for e in dic_items:
      default_stock_csv_column_size = 10
      
      # 이 로직은 새롭게 추가된 SK 스퀘어가 디폴트 기간인 10일을 만족하지 못하기 
      # 때문에 추가된 코드이다.
      # 76000은 SK스퀘어 기준이지만, 텍스트 정보 출력을 위해서는 사실 금일, 어제의 데이터만
      # 만 있으면 되므로 중요한 값은 아니다.
      # SK스퀘어가 추가되므로써 전체 자산의 추세 그래프를 그리는데는 어려움이 생겼는데,
      # (몇개월간의 데이터가 필요하므로..) 아직 이 문제는 해결되지 않았다.
      while dic_items[e].size < default_stock_csv_column_size:
        dic_items[e] = np.append(dic_items[e], 76000)

    self.total_df = pd.DataFrame(dic_items, index=date)


  def _receive_currentValue(self, stock_code):
    """
    해당 종목의 날짜, 종가 정보만 이용한다.
    
    """  
    url = self._get_url(stock_code)
    df = pd.DataFrame()

    flag_receive_from_url = not self.opt['run_fast']

    for page in range(1, self.opt['num_crawl_pages']+1):
        folder_name = 'stock_info'
        file_name = folder_name + '/' + stock_code + '_stock_info.csv'

        if flag_receive_from_url: # url로부터 정보를 얻어온다.
          pg_url = '{url}&page={page}'.format(url=url, page=page)

          self.driver.get(pg_url)
          html_data = self.driver.page_source
          tmp_html = 'tmp.html'
          with open(tmp_html, 'w', encoding='utf-8-sig') as f:
            f.write(html_data)

          saved_pd = pd.read_html(tmp_html, header=0)[0]
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