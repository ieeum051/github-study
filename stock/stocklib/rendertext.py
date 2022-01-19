import datetime as dt
from .calstockasset import CalStockAsset
from .render import Render

# ASCII Color Code for print menu
CR_MARGENTA = '\033[95m'
CR_YELLOW = '\033[93m'
CR_REVERT = '\033[0m'
CR_GREEN = '\033[92m'
CR_BLUE = '\033[94m'
CR_WHITE = '\033[37m'

VALUE_UNIT = 10000

class RenderText(Render):
    """ print text result in console
    """
    def __init__(self, calstockasset, opt):
        self.calstockasset = calstockasset
        self.calstockasset.merge_print_stocks_by_grp()  
        self.stocks = calstockasset.get_print_stocks() 
        self.is_print_total = opt['is_print_total']

        self.set_text_color(opt['nocolor'])

    def set_text_color(self, is_nocolor):
        global CR_MARGENTA 
        global CR_REVERT
        global CR_BLUE         

        if is_nocolor:
            CR_MARGENTA = CR_WHITE
            CR_REVERT = CR_WHITE
            CR_BLUE = CR_WHITE

    def draw(self):
        self._print_stock_info()
        self._print_summary_info()

    def _print_stock_info(self):
        """ self.print_data로 모아진 내용을 출력f
        input : self.print_data
        output : print
        """
        now_dt = dt.datetime.now()
        print("["+ str(now_dt.hour) + ":" + str(now_dt.minute) + "]")

        grp_element_max_len = max([len(self.stocks[key]) for key in self.stocks.keys()])

        print_text = ''

        for i in range(grp_element_max_len):
            line_text = '| '

            # 그룹별 print 데이터 생성
            for grp in self.stocks.keys():
                
                if len(self.stocks[grp]) > i:
                    stock = self.stocks[grp][i]
                    # SK스퀘어 표현이 지저분해서 생략함. 
                    if stock['name'] == 'SKSQ':
                        continue
                    line_text += (self._get_print_text(stock) +  ' | ')
                else:  # 왼쪽에 stock 정보가 없을때, 빈칸으로 띄어준다.
                    if self.is_print_total:
                        line_text += ( '{:<43}'.format('')+  ' | ')
                    else:
                        line_text += ( '{:<29}'.format('')+  ' | ')
            print_text +=  (line_text + '\n')
        
        print(print_text, end='')

    def _print_summary_info(self):
        """ self.print를 통합 계산하여 출력
        """
        summary = self.calstockasset.get_summary()
        space = '       ' if self.is_print_total else ''

        # make print data
        line_text = '| '
        for grp in self.stocks.keys():
            line_text += self._get_summary_text(summary[grp]) + space + ' | '
        
        self._print_border()
        print(line_text)
        self._print_border()
        print('| ' + self._get_summary_text(summary['total']) )
        print()

    def _print_border(self):
        for key in self.stocks.keys():
            if self.is_print_total:
                print('- - - - - - - - - - - - - - - - - - - - - - -', end='')
            else:
                print('- - - - - - - - - - - - - - - -', end='')
            
        print()

    def _get_print_text(self, stock):
        """ stock 정보를 출력가능한 형태로 변환
        """
        rate = round((stock['daily_asset'][0]*100 / stock['init_val']) - 100, 1)
        daily_var = round(stock['daily_asset_var'][0], 1)
        gap_prev = round(stock['gap_prev'], 1)
        gap_rate_prev = round(stock['gap_prev']*100 / (stock['daily_asset'][0] - stock['gap_prev']), 1)

        CR_TOTAL = CR_WHITE
        CR_RATE = CR_MARGENTA if rate > 0 else CR_BLUE
        CR_VAR = CR_MARGENTA if  daily_var > 0 else CR_BLUE
        CR_GAP = CR_MARGENTA if gap_prev > 0 else CR_BLUE
        CR_GAP_RATE = CR_MARGENTA if gap_rate_prev > 0 else CR_BLUE

        # if rate > 0 : rate = CR_MARGENTA + str(rate) + '%'
        # else: rate = CR_BLUE + str(rate) + '%'
        if self.is_print_total:
            stock_total = round(stock['daily_asset'][0], 1)
            return '{:<7}{}{:>7}{}{:>7}%{}{:>8}{}{:>6}{}{:>6}%{}'.format(
                                            stock['name'], 
                                            CR_TOTAL, stock_total,
                                            CR_RATE, rate,
                                            CR_VAR, daily_var,
                                            CR_GAP, gap_prev,
                                            CR_GAP_RATE, gap_rate_prev,
                                            CR_REVERT
            )

        return '{:<7}{}{:>7}%{}{:>8}{}{:>6}{}'.format(
                                        stock['name'], 
                                        CR_RATE, rate,
                                        CR_VAR, daily_var,
                                        CR_GAP, gap_prev,
                                        CR_REVERT
        )

    def _get_summary_text(self, grp_data):
        """ grp_data를 print가능한 형태로 출력.
        문제 : 나눴지만, grp_data 의 구조를 분석해야한다.
        """
        total_asset = round(grp_data['cur_val'], 1)
        if not self.is_print_total:
            total_asset = '----'

        rate = round((grp_data['cur_val']*100 / grp_data['init_val']) - 100, 1)

        daily_var = round(grp_data['gap_from_init'], 1)
        gap_prev = round(grp_data['gap_prev'], 1)
        gap_rate_prev = round(grp_data['gap_prev']*100 / (grp_data['cur_val'] -  grp_data['gap_prev']) , 1)

        cr_rate = CR_MARGENTA if rate > 0 else CR_BLUE
        cr_var = CR_MARGENTA if  daily_var > 0 else CR_BLUE
        cr_gap = CR_MARGENTA if gap_prev > 0 else CR_BLUE
        cr_gap_rate = CR_MARGENTA if gap_rate_prev > 0 else CR_BLUE

        # TODO 퍼센테지이지는 telegram에도 사용됨. 합쳐야한다.
        # TODO total이 아닌경우 깨짐. 나중에 고치자
        return '{:<7}{}{:>7}%{}{:>8}{}{:>6}{}{:>6}%{}'.format(
                                        total_asset,
                                        cr_rate, rate,
                                        cr_var, daily_var,
                                        cr_gap, gap_prev, 
                                        cr_gap_rate, gap_rate_prev,
                                        CR_REVERT
        )