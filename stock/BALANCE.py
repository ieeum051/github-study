# -*- coding: utf-8 -*-
import sys
from matplotlib import pyplot as plt
# from datetime import date
import datetime
from dateutil.relativedelta import relativedelta
import copy

# 한달 주기로 update (카드대금 차감 후 )
# 항상 최신 Data가 위로 올라오도록 설계.

balance = {
    # 같은 월은 안됨..
    '220101' : 70+1332+4.4+1699+6878+1011+1448+3124+5333-130,
    '211209' : 46.3+1146+57+833+6878+1009+1353+3100+5222,
    '211105' : 1184+16+750+6876+688+1343+3380+5153,
    '211008' : 1211+284+6947+704+1234+3554+4900,
    '210618' : 1080+22+4858+3252+1512+4967+504,
    '201017' : 270+3258+407+4822+1000+1937,
    '200904' : 240+3471+760+4817+1000+1098,
    '200803' : 210+1136+627+4812+1000+2400+(64+574+107),
    '200706' : 181+733+636+4800+1000+2400,
    '200605' : 150+2511+500+3901+1000+1400,
    '200506' : 120+2380+600+4896+1000,
    '200406' : 90+2660+651+4589+1000,
    '200302' : 30+2564+1753+4577,
    '200203' : 1946+2238+3960,
    '200102' : 2109+2644+3455,
    '191203' : 1867+2818+3100,
    '191104' : 1845+2617+3100
}

# 특이사항
# 20년 1월말에 어머니 수술비 지원 3백만원

LOAN_OUT = 0 # TP + WM (5K는 월세로 대체), TP 비용으로 써 버림..
DEPOSIT = 9000 + 375 # 500(101)+1000(201)+7500(202) + 375 (202호 추가)
FIXED_DEBT = LOAN_OUT - DEPOSIT

# https://intotw.tistory.com/128
GREEN = '\033[32m'
BLUE = '\033[94m'
RED = '\033[91m'
YELLOW = '\033[93m'
WHITE = '\033[37m'

COLOR_OUT = 1

check_date_list = list(balance.keys())
current_assets_list = list(balance.values())

def run():
    # print
    print_list ('정산DAY_____', check_date_list, 0, WHITE, num=5)
    print_list ('유동자산____', current_assets_list, 0, WHITE, num=5)
    print_list ('순수유동자산', get_pure_val(current_assets_list), 0, GREEN, num=5)
    print_list ('이전대비변동', get_var_list(current_assets_list), 0, WHITE, num=5)
    print_list ('월평균변동__', 
        get_monthly_var_list(
            get_month_gap_list(check_date_list),
            get_var_list(current_assets_list)), 
        0, YELLOW)

    render_chart()
def print_list(cat, alist, pos=0, colorcode=None, num=5):
    print(colorcode, '%s'%cat, end=':')

    for i in range(pos):
        print(" ", end='')

    cnt = 0
    for a in alist:
        cnt+=1
        if cnt > num: break

        a = int(a)
        color = colorcode
        if colorcode == None:
            if a > 0:
                color = RED
            else:
                color = BLUE
        if COLOR_OUT:
            print(color, '%10d, '%a, end='')
        else:
            print('%5d, '%a, end='')
    print()

def get_pure_val(value_list):
    pure_val_list = []
    for val in value_list:
        pure_val_list.append(val + FIXED_DEBT)

    return pure_val_list

def get_var_list(value):
    variation_list = []
    for i in range(len(value)):
        # value[i] += FIXED_DEBT
        if i > 0:
            variation_list.append(value[i-1] - value[i])     

    return variation_list

def get_monthly_var_list(month_gap_list, var_list):
    monthly_var_list = []
    for i in range(len(month_gap_list)):
        monthly_var_list.append(var_list[i] / month_gap_list[i])

    return monthly_var_list

def get_month_gap_list(date_list):
    cur = 0
    prev = 0
    gap_list = []
    for date in date_list:
        year = int(date[0:2])
        month = int(date[2:4])
        cur = year*12 + month
        if prev != 0:
            gap = prev - cur 
            # print(gap)
            gap_list.append(gap)
        prev = cur
    return gap_list
   

def add_skip_month_estimate_monthly_asset(date_list, current_assets_list):
    converted_date_list = convert_str_date2datetype(date_list)
    
    
    work_date_list = gen_date_asset_list_with_date_gap(converted_date_list, current_assets_list)

    # 201911-04가 사라짐   
    return gen_complete_date_asset_list(work_date_list)


def convert_str_date2datetype(date_list):
    converted_date_list = []
    for each_date in date_list:
        re_date_str = '{}-{}-{}'.format('20'+each_date[0:2], each_date[2:4], each_date[4:6])
        re_date = datetime.datetime.strptime(re_date_str, '%Y-%m-%d')
        converted_date_list.append(re_date)

    return converted_date_list


def gen_date_asset_list_with_date_gap(converted_date_list, current_assets_list):
    work_date_list = []
    loop_size = len(converted_date_list)
    end_idx = loop_size - 1

    for i in range(loop_size):
        if i == end_idx:
            this_date = converted_date_list[i]
            this_asset = current_assets_list[i]
            gap = 0
        else:
            this_date = converted_date_list[i]
            next_date = converted_date_list[i+1]
            this_asset = current_assets_list[i]

            gap = this_date.month - next_date.month

            if gap < 0:
                gap += 12

        work_date_list.append({
            'date': this_date,
            'asset': this_asset,
            'prev_gap': gap
        })
    return work_date_list


def gen_complete_date_asset_list(work_date_list):
    complete_date_asset_list = []
    one_month = relativedelta(months=1)

    # add skipped month data by average estimation (date, asset)
    loop_size = len(work_date_list)
    end_idx = loop_size - 1
    for i in range(loop_size):
        this_date = work_date_list[i]

        if i == end_idx:
            next_date = 0
        else:
            next_date = work_date_list[i+1]

        complete_date_asset_list.append(
            {
                'date' : this_date['date'],
                'asset' : this_date['asset'],
                'true': 1,
            }
        )

        # condition :  add skipped month data by average estimation (date, asset)
        if this_date['prev_gap'] > 1:
            decreased_month = this_date['date']

            if i == end_idx:
                asset_gap = 0
            else:
                asset_gap = this_date['asset'] - next_date['asset']

            avg_asset_gap = asset_gap / this_date['prev_gap']
            
            decreased_asset = this_date['asset']
            for i in range(this_date['prev_gap'] -1):
                decreased_asset -= avg_asset_gap
                decreased_month = decreased_month - one_month
                complete_date_asset_list.append({
                    'date' : decreased_month,
                    'asset' : decreased_asset,
                    'true': 0,
                })

    for each_date in complete_date_asset_list:
        each_date['date'] = each_date['date'].strftime('%y%m%d')

    return complete_date_asset_list

def render_chart():
    # data adaptation for rendering # need to refactor
    date_asset_list = add_skip_month_estimate_monthly_asset(check_date_list, current_assets_list)

    # rendering
    render_date_asset(date_asset_list)

def render_date_asset(date_asset_list):
    # data check
    # for date_asset in date_asset_list:
    #     print(date_asset)

    date_list = []
    asset_list = []
    for date_asset in date_asset_list:
        date_list.append(date_asset['date'])
        asset_list.append(date_asset['asset'])

    plt.plot(date_list, asset_list)
    plt.xticks(rotation=45)
    plt.gca().invert_xaxis()
    plt.grid(True)
    # 0 base line
    #plt.axhspan(-0.1, 0.1, color='red' ) #, alpha=1) # X축 역전
    plt.show()


if __name__ == "__main__":
    run()
