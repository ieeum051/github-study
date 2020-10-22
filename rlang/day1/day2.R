# R의 제어문과 함수

# 1. if-else 문

# 1.1 기본 if-else문
job.type <- 'A'
if(job.type == 'B'){
  bonus <- 200
}else{
  bonus <- 100
}

print(bonus)

# 1.2. else가 생략된 if문
job.type <- 'B'
bonus <- 100
if(job.type == 'A'){
  bonus <- 200
}
print(bonus)

# 1.3 다중 if-else 문
score <- 85

if(score > 90){
  grade <- 'A'
}else if(score > 80){
  grade <- 'B'
}else if(score > 70){
  grade <- 'C'
}else if(score > 60){
  grade <- 'D'
}else{
  grade <- 'F'
}
print(grade)

# 1.4 조건문에서 논리 연산자의 사용
a <- 10
b <- 20
if(a>5 & b>5){ # and
  print(a+b)
}

if(a>5 | b>30){ # or
  print(a*b)
}


# ifelse 문
a <- 10
b <- 20

if(a>b){
  c <- a
}else {
  c <- b
}
print(c)

c <- ifelse(a>b, a, b) # 일종의 3항 연산자
print(c)

# 반복문
# 1. for문
# 1.1 기본 for문
# 1.2 반복 범위에 따른 반복 변수의 값 변화
for(i in 1:5){
  print(i)
}

# 1.3 반복 변수를 이용한 구구단 출력
for(i in 1:9){
  cat('2 *', i, '=', 2*i, '\n') # 파이썬 for 문에서는 가능
}

# 1.4 for문 안에서 if문 사용
for (i in 1:20){
  if(i%%2==0){ # 짝수 확인
    print(i)  
  }
}

# 1.5 1~100 사이의 숫자의 합 출력
sum <- 0
for(i in 1:100){
  sum <-sum + i
}
print(sum)

# 1.6 iris에서 꽃잎의 길이에 따른 분류 작업
norow <- nrow(iris)
mylabel <- c()
for(i in 1:norow){
  if (iris$Petal.Length[i] <= 1.6){
    mylabel[i] <- 'L'
  }else if (iris$Petal.Length[i] >= 5.1){
    mylabel[i] <- 'H'
  }else{
    mylabel[i] <- 'M'
  }
}
print(mylabel)
print(iris$Petal.Length)
newds <- data.frame(iris$Petal.Length, mylabel)
head(newds)

# 2. while 문

sum <- 0
i <- 1
while(i<=100){
  sum <- sum + i
  i <- i + 1
}
print(sum)

# 구구단
i  <-  2
while(i<=9){
  j  <-  1
  while(j <=9){
    cat(i,'*',j,'=',i*j, '\n')
    j <- j+1    
  }
  i <- i+1
}

# 3. break와 next
# 3.1 break
sum <- 0
for (i in 1:10){
  sum <- sum + i
  if (i>=5) break
}
sum

# 3.2 next
sum <- 0
for(i in 1:10){
  if (i%%2 ==0) next # continue
  print(i)
  sum <- sum+i
}
sum

# apply 함수
# 1. apply 함수의 개념

# 2. apply 함수의 적용
iris[,1:4]
apply(iris[,1:4], 1, mean) # 데이터셋 iris[,1:4], 1 : row 방향, mena : 평균
apply(iris[,1:4], 2, mean) # 데이터셋 iris[,1:4], 2 : col 방향, mena : 평균


# 사용자 정의함수
# 1. 사용자 정의 함수 만들기
# 4.1 사용자 정의 함수를 만들고 사용하기
mymax <- function(x, y){
  num.max <- x
  if (y > x){
    num.max <- y
  }
  return (num.max)
}

mymax(10, 15)

# 4.2 사용자 정의함수
mydiv <- function(x,y=2){ # y값 default
  result <- x/y
  return(result)
}
mydiv(x=10,y=3)
mydiv(10)

# 4.3 함수가 반환하는 결과값이 여러개 일때의 처리
myfunc <- function(x,y){
  val.sum <- x+y
  val.mul <- x*y
  return(list(sum=val.sum, mul=val.mul))
}
result <- myfunc(5,8)
s <- result$sum
m <- result$mul
cat('5+8=',s,'\n')
cat('5*8=',m,'\n')

# 2. 사용자 정의 함수의 저장 및 호출
setwd("Z:/private/github-study/rlang/day1")
source("myfunc.R")

a <- mydiv(20,4)
b <- mydiv(30,4)
a+b
mydiv(mydiv(20,2), 5) # 함수 결과를 파라미터로..


# 조건에 맞는 데이터의 위치 찾기
score <- c(76, 84, 69, 50, 95, 60, 82, 71, 88, 84)
which(score == 69) # 해당 위치 반환
score[which(score == 69)]
max(score)
which.max(score)
min(score)
which.min(score)

idx <- which(score<=80)
score[idx] <- 0  # 동시에 모두 바뀐다..
score


idx <- which(score>=80)
score.high <- score[idx]
score.high

# subset으로 표현현
score <- c(76, 84, 69, 50, 95, 60, 82, 71, 88, 84)
subset(score, score>=80)

subset(st[c('Population', 'Income', 'Area')], Income >= 4500)
subset(st, Income >= 4500, select=c('Income', 'Area'))
subset(st, Income >= 4500)[,c('Income', 'Area')]


idx <- which(iris$Petal.Length > 5.0) # 해당조건의 iris 행 정보를 구함.
idx
iris.big <- iris[idx,]  # 해당 행들의 iris 정보를 저장한다.
iris.big

# 1~4열의 값중 5보다 큰 값의 행과 열의 위치
iris[,1:4]

idx <- which(iris[,1:4]>5.0, arr.ind=T)

# 단일 변수 자료
# 1. 자료의 특성에 따른 분류
# 범주형 자료 vs 연속형 자료

# 1.1 범주형 자료
# 1.2 연속형 자료

# 2. 변수의 개수에 따른 분류
# 단일 변수 자료 (univariate data)
# - 일변량 자료
# 데이터 구조 : 벡터

# 다중 변수 자료 (multivariate data)
# - 다변량 자료, 2개의 변수는 이변량 자료(bivariate data)라고 함
# 데이터 구조 : 매트릭스, 데이터 프레임,  열(column이 하나의 변수


# 단일변수 범주형 자료의 탐색
# 1. 도수 분포표의 작성
favorite <- c('WINTER', 'SUMMER', 'SPRING', 'SUMMER', 'SUMMER',
              'FALL', 'FALL', 'SUMMER', 'SPRING', 'SPRING')
favorite
table(favorite) #도수 분포표 계산
table(favorite)/length(favorite)


# 2. 막대 그래프의 생성
ds <- table(favorite)
barplot(ds, main='favorite season')

ds.new <- ds[c(2,3,1,4)] # 순서 바꿔주기
barplot(ds.new, main='favorite season')

# 3. 원그래프의 작성
ds <- table(favorite)
pie(ds,  main='favorite season')

# 4. 숫자로 표현된 범주형 자료
favorite.color <- c(2,3,2,1,1,2,2,1,3,2,1,3,2,1,2)
ds <- table(favorite.color)
ds
barplot(ds, main='favorite color')
colors <- c('green', 'red', 'blue')
names(ds) <- colors
ds
barplot(ds, main='favorite colors', col=colors)
pie(ds, main='favorite colors', col=colors)

# 단일변수 연속형 자료의 탐색

# 1. 평균과 중앙값

weight <- c(60, 62, 64, 65, 68, 69)
weight.heavy <- c(weight, 120)
weight
weight.heavy

mean(weight)
mean(weight.heavy)

median(weight)
median(weight.heavy)

mean(weight, trim=0.2) # 절사 평균 (상하위 20% 제외)
mean(weight.heavy, trim=0.2) 

# 2. 사분위수

mydata <- c(60, 62, 64, 65, 68, 69, 120)
quantile(mydata)
quantile(mydata, (0:10)/10) # 10% 단위 구간으로 나누어 계산
summary(mydata) # 기본적인 통계지표 표시

# 3. 산포
# 분산, 표준편차
mydata <- c(60, 62, 64, 65, 68, 69, 120)
var(mydata) # 분산
sd(mydata)  # 표준편차
range(mydata) # 값의 범위
diff(range(mydata)) # 최대값, 최소값의 차이

# 4. 히스토그램
dist <- cars[,2]
dist
hist(dist, 
          main="Histogram for 제동거리",
          xlab = "제동거리",
          ylab = "빈도수",
          border="blue",
          col="green",
          las=2,
          breaks=5)

# 5. 상자 그림 (box and whisker plot)
# 사분위수룰 시각화하여 표시

dist <- cars[,2]
boxplot(dist, main='자동차 제동거리')
boxplot.stats(dist)  # 분포 통계치
# $stats : 1~4분위수, Q3+1.5IQR
# $n : 개수
# $conf : notch의 최대, 최소
# $out : 이상치, 특이값




# 6. 그룹이 있는 자료의 상자 그림

# Petal.Length~Species
boxplot(Petal.Length~Species, data=iris, main='품종별 꽃잎의 길이')

# 한 화면에 그래프 여러 개 출력하기
par(mfrow=c(1,3))  # 1x3 화면 가상 분할
barplot(table(mtcars$carb),
        main= "Barplot of Carburetors",
        xlab = "#of carburetors",
        ylab = "frequency",
        col="blue")

barplot(table(mtcars$cyl),
        main= "Barplot of Cylender",
        xlab = "#of Cylender",
        ylab = "frequency",
        col="red")

barplot(table(mtcars$gear),
        main= "Barplot of Gear",
        xlab = "#of gears",
        ylab = "frequency",
        col="green")

par(mfrow=c(1,1)) # 가상화면 분할 해제


# 다중변수 자료
# 1. 두 변수 사이의 산점도

wt <- mtcars$wt
mpg <- mtcars$mpg
plot(wt, mpg, # x축, y축
     main='중량, 연비 그래프',
     xlab='중량',
     ylab='연비(MPG)',
     col='red',
     pch=19)  # pch : 포인트의 종류

# 2. 여러변수들 간의 산점도
vars <- c('mpg', 'disp', 'drat', 'wt')
target <- mtcars[,vars]
head(target)
pairs(target,
     main='Multi Plots')

# 3. 그룹정보가 있는 두 변수의 산점도
iris.2 <- iris[,3:4]
iris$Species
point <- as.numeric(iris$Species) # 종류를 숫자로 바꾸고 point 종류로 표시.
point
color <- c('red', 'green', 'blue') # point의 숫자 종류를 보고 3개의 color로 만듦
plot(iris.2,
     main='Iris Plot',
     pch=c(point),
     col=color[point] 
     )

# 상관분석

# 1. 상관분석과 상관계수
# 피어슨 상관계수, 1, -1에 가까울 수록 x,y의 상관성이 높음

# 2. R을 이용한 상관계수의 계산
beers <- c(5,2,9,8,3,7,3,5,3,5)
bal <- c(0.1,0.03,0.19,0.12,0.04,0.0095,0.07,0.06,0.02,0.05)

tbl <- data.frame(beers,bal) # 1열, 2열로 표시
tbl
plot(bal~beers, data=tbl)  # 산점도
res <- lm(bal~beers, data=tbl) # 회귀식 도출
abline(res)     # 회귀선 
cor(beers,bal)  # 상관계수

cor(iris[,1:4]) # 4개 변수 간 상관성 분석

# 선그래프
# 1. 선그래프의 작성 (p.103)
month <- 1:12
late <-  c(5,8,7,9,4,6,12,13,8,6,6,4)
plot(month, late,
     main="지각생 통계",
     type='l', #그래프의 종류
     lty=1, # 선의 종류(line type) 선택  (p.103)
     lwd=1, # 선의 굵기
     xlab='Month',
     ylab='Late Cnt'
     )



# 다중변수 자료의 변수 중 하나가 연월일과 같이 시간을 나타내는 값을 갖는 경우
# x축을 시간 축으로 하여 선그래프를 그리면 시간의 변화에 따른 자료의 증감 추이를
# 쉽게 확인할 수 있다. 시간의 변화에 따라 자료를 수집한 경우 이를 시계열 자료
# (times series data)라고 한다.

# 2. 복수의 선그래프의 작성
month =1:12
late1 = c(5,8,7,9,4,6,12,13,8,6,6,4)
late2 = c(4,6,5,8,7,8,10,11,6,5,7,3)
plot(month,late1,
     main='Late Students',
     type='b',
     lty=1,
     col='red',
     xlab='Month',
     ylab='Late Cnt',
     ylim=c(1,15)  # y축 값의 (하한, 상한)
     )

lines(month, late2, # line 추가
      type = 'b',
      col = 'blue')

# 추가 예시..
USAccDeaths
years.1973 <- window(USAccDeaths, 1973, c(1973,12))
years.1975 <- window(USAccDeaths, 1975, c(1975,12))
years.1977 <- window(USAccDeaths, 1977, c(1977,12))
years.1973

month  <-  1:12
plot(month,years.1973,
     main='USAccDeaths',
     type='l',
     lty=1,
     col='red',
     xlab='Month',
     ylab='USAccDeaths',
     ylim=c(6000,12000)  # y축 값의 (하한, 상한)
)

lines(month, years.1975, # line 추가
      type = 'l',
      col = 'blue')

lines(month, years.1977, # line 추가
      type = 'l',
      col = 'green')


# 자료의 탐색 실습
# 1. Boston Housing 데이터셋 소개
# * 미국 보스턴 지역의 주택 가격 정보와 주택 가격에 영향을 미치는 여러요소들에 대한
# 정보를 담고 있음
# * 총 14개의 변수로 구성이 되어 있는데, 여기서는 이중에 5개의 변수만 선택하여 분석
# * mlbench 패키지에서 제공
# 변수 : crim(지역의 1인당 범죄율),  rm(주택 1가구당 방의 개수)
#        dis(보스턴의 5개 직업 센터까지의 거리)
#        tax(재산세율), medv(주택 가격)

# 1.1 분석 대상 데이터셋 준비
library(mlbench)
data('BostonHousing')
myds <- BostonHousing[,c('crim', 'rm', 'dis', 'tax', 'medv')]

# 1.2 grp 변수 추가
grp <- c()
for(i in 1:nrow(myds)){
  if(myds$medv[i] >= 25.0){
    grp[i] <- 'H'
  }else if(myds$medv[i] <= 17.0){
    grp[i] <- 'L'
  } else{
    grp[i] <- 'M'
  }
}
grp <- factor(grp)
grp <- factor(grp, levels=c('H', 'M', 'L')) # 레벨의 순서를 H L M -> H M L
myds <- data.frame(myds, grp) # myds에 grp 열 추가
myds

# 1.3 데이터셋의 형태와 기본적인 내용 파악
str(myds)
head(myds)

# 1.4 히스토그램에 의한 관측값의 분포확인
myds

par(mfrow=c(2,3)) # 2x3 가상 화면 분할
for (i in 1:5){
  hist(myds[,i], main=colnames(myds)[i], col='yellow')
}

par(mfrow=c(1,1)) # 1x1 원복


# 1.5 상자그림에 의한 관측값의 분포 확인
par(mfrow=c(2,3)) # 2x3 가상 화면 분할

for (i in 1:5){
  boxplot(myds[,i], main=colnames(myds)[i])
}
par(mfrow=c(1,1)) # 1x1 원복

# 1.6 그룹별 관측값 분포의 확인
boxplot(myds$crim~myds$grp, main='1인당 범죄율')

boxplot(myds$rm~myds$grp, main='방의 개수')

# 1.7 다중 산점도를 통한 변수 간의 상관관계의 확인
pairs(myds[,-6])

# 1.8 그룹 정보를 포함한 변수 간 상관관계의 확인
point <- as.integer(myds$grp) # 점 모양 지정
color <- c('red', 'green', 'blue') # 점의 색 지정 (상위, 중위, 하위그룹)
pairs(myds[,-6], pch=point, col=color[point])

# - 점의 색을 지정하면 산점도에서 그룹별 분포 위치가 뚜렷하게 구분된다.

# 1.9 변수 간 상관계수의 확인
cor(myds[,-6])













