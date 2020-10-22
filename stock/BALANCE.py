# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt

# 한달 주기로 update (카드대금 차감 후 )
# 항상 최신 Data가 위로 올라오도록 설계.
# 파일에서 가져오자 (미구현)
date = ['0117', '0904','0803', "0706", "0605", "0506", "0406", "0302" , "0203", "0102", "1203", "1104"]

# 하나 + 산은 + 카뱅 + 사이다 + 새마을 + 한투,
# 하나 + 산은 + 카뱅 + 사이다 + 새마을 + 기타(장모님) + 한투, (~20.8월)
value = [270+3258+407+4822+1000+1937, 
         240+3471+760+4817+1000+1098,
    210+1136+627+4812+1000+2400+(64+574+107), 181+733+636+4800+1000+2400,
    150+2511+500+3901+1000+1400, 120+2380+600+4896+1000, 90+2660+651+4589+1000, 30+2564+1753+4577, 1946+2238+3960 ,2109+2644+3455,1867+2818+3100, 1845+2617+3100]
variation = []

# 특이사항
# 20년 1월말에 어머니 수술비 지원 3백만원

LOAN_OUT = 1000 # TP + WM (5K는 월세로 대체)
DEPOSIT = 9000 # 500(101)+1000(201)+7500(202)
FIXED_DEBT = LOAN_OUT - DEPOSIT

BLUE = '\033[94m'
RED = '\033[91m'
YELLOW = '\033[93m'

COLOR_OUT = 0

def print_list(alist, pos=0, colorcode=None):
    for i in range(pos):
        print(" ", end='')

    for a in alist:
        color = colorcode
        if colorcode == None:
            if a > 0:
                color = RED
            else:
                color = BLUE
        if COLOR_OUT:
            print(color, '%5d, '%a, end='')
        else:
            print('%5d, '%a, end='')
    print()

def run():
    for i in range(len(value)):
        value[i] += FIXED_DEBT
        if i > 0:
            variation.append(value[i-1] - value[i]) 
    print_list (value, 0, YELLOW)
    print_list (variation, 4)
    render()

def render():
    # value가 List다.
    plt.plot(date, value)
    plt.xticks(rotation=45)
    plt.gca().invert_xaxis()
    plt.grid(True)
    # 0 base line
    #plt.axhspan(-0.1, 0.1, color='red' ) #, alpha=1) # X축 역전
    plt.show()

if __name__ == "__main__":
    run()
