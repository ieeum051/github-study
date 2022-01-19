from matplotlib import pyplot as plt

from .calstockasset import CalStockAsset
from .render import Render

class RenderGraph(Render):
    """ draw trends of total stock assets
    """

    def __init__(self, calstockasset, opt=None):
        self.calstockasset = calstockasset

    def draw(self):
        date_index = self.calstockasset.get_daily_index_list()
          # TOOD : date index에서 5일 단위로 값을 넣는다던지..
        plt.figure(1, figsize=(8,4))
        plt.title("My Graph")

        value_list = self.calstockasset.get_daily_revenu_sum_list()

        # value가 List다.
        plt.plot(date_index, value_list, c='seagreen', lw=2)
        
        # plt.legend(graphStyle.stockNames) 

        plt.xticks(rotation=45)
        plt.gca().invert_xaxis()
        plt.grid(True)

        # # 0 base line
        plt.axhspan(-0.1, 0.1, color='red' ) #, alpha=1)
        plt.show()