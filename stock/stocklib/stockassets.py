
import json

DATA_JSON = 'stock1.json'

class StockAssets:
  """
  """
  def __init__(self):
    self.file_name = DATA_JSON
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