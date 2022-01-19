import datetime as dt
import copy

# ASCII Color Code for print menu
CR_MARGENTA = '\033[95m'
CR_YELLOW = '\033[93m'
CR_REVERT = '\033[0m'
CR_GREEN = '\033[92m'
CR_BLUE = '\033[94m'
CR_WHITE = '\033[37m'

VALUE_UNIT = 10000

class CalStockAsset:
  """ convert data from stock code and current stock state for printing

  Attributes:
    stock_asset : 
    stock_realinfo : 
    stock_list : 
    print_stocks : 
    daily_revenu_sum_list : 
    daily_index_list : x axis data for drawing chart

  """
  def __init__(self, stock_asset, stock_realinfo):
    self.stock_asset = stock_asset        # StockAssets
    self.stock_realinfo = stock_realinfo  # StockRealInfo
    self.stock_list = self.stock_asset.get_stock_list()
    self.print_stocks = {}
    self.daily_revenu_sum_list =[]
    self.daily_index_list = stock_realinfo.get_daily_index_list()

  def get_print_stocks(self):
    return self.print_stocks

  def get_daily_index_list(self):
    return self.daily_index_list

  def get_daily_revenu_sum_list(self):
    return self.daily_revenu_sum_list

  def update_daily_price(self):  
    for stock in self.stock_list:
      code = stock['code']
      stock['daily_prc'] = self.stock_realinfo.get_daily_price_list(code)

      # 문제점 : 여기서 데이터 요소가 정해짐...이상타..
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
      for i in range(len(stock['daily_revenu'])):
        self.daily_revenu_sum_list[i] += stock['daily_revenu'][i]

  def merge_print_stocks_by_grp(self):
    """ stock을 그룹별로 모아서 출력
    input : self.stock_list
    output : self.print_stocks
    """
    # grp 정보를 모아서 중복되지 않게 리스트를 만든다.
    grp_list = sorted(list(set([stock['grp'] for stock in self.stock_list])))

    # grp 정보에 따라 grp 별로 stock 정보를 모은다.
    for grp in grp_list:
      self.print_stocks[grp] = [stock for stock in self.stock_list if stock['grp'] == grp]

  def get_summary(self):
    """ self.print_stocks를 total summary로 출력

    rendertelegram.py의 RenderTelegram에서 사용 중
    """
    summary = {}

    # 문제점 : 중요한 데이터 타입이 LOCAL에서 설정됨.
    init_dict = {'cur_val': 0, 'gap_from_init': 0, 'gap_prev': 0, 'init_val': 0}

    # make total data
    summary['total'] = copy.deepcopy(init_dict)
    for stock in self.stock_list:
      self._cal_total(summary['total'], stock)

    # make group data
    for grp in self.print_stocks.keys():
      summary[grp] = copy.deepcopy(init_dict)
      for stock in self.print_stocks[grp]:
        self._cal_total(summary[grp], stock)

    return summary

  def _cal_total(self, summary, stock):
    summary['init_val'] += stock['init_val']
    summary['cur_val'] += stock['daily_asset'][0]
    summary['gap_from_init'] += stock['daily_asset_var'][0]
    summary['gap_prev'] += (stock['daily_asset'][0] - stock['daily_asset'][1])
