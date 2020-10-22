# 데이터 시각화 처리
# 1. 데이터 시각화의 중요성

# 2. 트리맵 (p. 136)
# 2.1 GNI2014 데이터셋으로 트리맵 작성하기
# * 사각타일의 형태로 구성되어 있으며, 각 타일의 크기와 색깔로 데이터의 크기를 나타냄.
# * 각각의 타일은 계층 구조가 있기 때문에 데이터에 존재하는 계층구조도 표현
# * 예제 데이터셋 : treemap 패키지 안에 포함된 GNI2014.2014년도의 전 세계 국가별 인구,
# 국민총소득(GNI), 소속 대륙의 정보를 담고 있음.

library(treemap)
data(GNI2014)
head(GNI2014)
# iso3 : 국가를 식별하는 표준코드
# country : 국가명
# continent : 국가가 속한 대륙명
# population : 국가의 인구
# GNI : 국가의 국민총소득


treemap(GNI2014,
        index=c('continent', 'iso3'), # 대륙 - 국가
        vSize='population', # 타일의 크기
        vColor='GNI', # 타일의 컬러 
        type='value', # 타일 컬러링 방법
        bg.labels='yellow', # 레이블의 배경색
        title='Worlds GNI') # 트리맵 제목


# 2.2 state.x77 데이터셋으로 트리맵 작성하기
library(treemap)
st <- data.frame(state.x77)
st <- data.frame(st, stname=rownames(st))

treemap(st,
        index=c('stname'), # 타일에 주 이름 표기
        vSize='Area',  # 타일의 크기
        vColor='Income', # 타일의 컬러
        type='value', # 타일 컬러링 방법
        title='USA states area and Income') # 트리맵의 제목

# 3. 버블차트 (p.138)
# 산점도가 2개의 변수에 의한 위치 정보를 표시한다면, 
# 버블차트는 3개의 변수 정보를 하나의 그래프에 표시

st <- data.frame(state.x77)

x_values <- st$Illiteracy
y_values <- st$Murder
# 버블을 그린다.
symbols(x_values, t_values, # x, y 좌표의 열
        circles=st$Population, # 원의 반지름의 열
        inches=0.3, # 원의 크기 조절 값
        fg='white', #  원의 테두리 색
        bg='lightgray', # 원의 바탕색
        lwd=1.5, # 원의 테두리선 두께
        xlab='rate of Illiteracy',
        ylab='crime(murder) rate',
        main='Illiteracy and Crime')
# 버블에 글자를 쓴다.
text(x_values, y_values, # 텍스트가 출력될 x, y좌표
     rownames(st), # 출력할 텍스트
     cex=0.6, # 폰트 크기
     col='brown' # 폰트 컬러
)


# 3. 모자이크 플롯        
# 다중변수 범주형 데이터에 대해 각 변수의 그룹별 비율을 면적으로 표시하여 정보를 전달
head(mtcars)
# ~x_values+y_values
mosaicplot(~gear+vs,data=mtcars, color=T, main='Gear and Vs')

# ggplot 패키지
# 보다 미적인 그래프를 작성하려면 ggplot 패키지를 주로 이용
# 대표적인 R의 시각화 패키지..(그럴꺼면..위에꺼 배울 필요가..)
# 하지만 배우기 어렵다...(배우기 어려울 이유가??)

# 1. ggplot 
# 특성
# - 하나의 ggplot() 함수와 여러개의 geom_xx() 함수들이 + 로 연결되어 하나의 그래프를 완성
# - ggplot() 함수의 매개변수로 그래프를 작성할 때 사용할 데이터넷(data=xx)와 데이터 셋안에서
#   x축, y축으로 사용할 열 이름(aes(x=x1, y=y1))을 지정
#   ex> geom_bar()

# 2. 막대그래프의 생성
# 2.1 기본적인 막대그래프 작성하기

library(ggplot2)
month <- c(1,2,3,4,5,6)
rain <- c(55,50,45,50,60,70)
df <- data.frame(month, rain) #  그래프를 작성할 대상 데이터 (데이터 프레임 형식)


# 그래프를 그릴 데이터 지정

ggplot(df, aes(x=month, y=rain)) +  # aes는 그래프를 그리기 위한 x, y축의 열을 지정한다.
  
  geom_bar(stat='identity', # 막대 높이는 y축에 해당하는 열의 값으로 자동 지정하도록 하는 옵션
           width=0.7, # 막대의 폭 지정
           fill='steelblue') # 막대의 채움 색상 지정

# 2.1 막대그래프 꾸미기
ggplot(df, aes(x=month, y=rain)) +
  geom_bar(
    stat='identity',
    width=0.7,
    fill='steelblue'
  ) +
  ggtitle('월별 강수량') + # 그래프 제목 지정
  theme(plot.title = element_text(size=25, face='bold', colour='steelblue')) +
  labs(x='월', y='강수량') + # 그래프의 x, y축 레이블 지정
  coord_flip # 그래프를 가로 방향으로


# 3. 히스토그램의 작성
# 3.1 기본적인 히스토그램 작성하기
library(ggplot2)

# 히스토그램은 범주형 데이트를 기반으로 하므로 값이 한 배열만 있어도 된다.
ggplot(iris, aes(x=Petal.Length)) + 
  geom_histogram(binwidth=0.5)

# 3.2 그룹별 히스토그램 작성하기
# column을 분리한 것이 아니고 
ggplot(iris, aes(x=Sepal.Width, fill=Species, color=Species)) +
  geom_histogram(binwidth=0.5, position='dodge') +
  theme(legend.position='top')