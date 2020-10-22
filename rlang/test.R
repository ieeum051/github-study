5+8
3+(4*5)
a<-10
print(a)

library(ggplot2) # 설치한 패키지 불러오기

# 산술연산
# 나머지는 타언어와 동일
# %% - 나눗셈의 나머지

# 기본연산 (p.19)
# log(), sqrt(), max(), min(), abs(), factorial()
# sin(), cos(), tan()


log(10)+5
sqrt(25)
max(5,3,2)

a<-10
b<-20
c<-a+b
print(c)

# 변수의 자료형 (p.22)
# 숫자형 : 1, 2, 3
# 문자형 : "TOM"
# 논리형 : TRUE, FALSE
# 특수값 : NULL, NA, NaN, Inf, -Inf

# 백터의 이해 

x<-c(1,2,3) # 숫자형 백터
y<-c("a", "b", "c") # 문자형 백터
z<-c(TRUE, FALSE, TRUE) # 논리형 백터
x
y
z

w <- c(1,2,3,"a", "b", "c") # 문자 백터로 변환됨
w  

# 백터 생성
v1 <- 50:90
v1
v2<-c(1,2,4, 50:90)
v2

# 일정간격으로 이루어진 백터생성
v3 <- seq(1,101,3) # 1 ~ 101, 간격 3
v3
v4 <- seq(0.1, 1.0, 0.1)
v4

# 2.3 반복된 숫자로 이루어진 백터 생성
v5 <- rep(1, times=5)
v5
v6 <- rep(1:5, times=5)
v6
v7 <- rep(c(1,5,9), times=3)
v7

# 3 백터의 원소값에 이름 지정
score <- c(90, 85, 70) # 성적 데이터
score
names(score)
names(score) <- c("John", "Tom", "Jane") # 각 성적에 이름을 부여
names(score)
score  # 이름과 함께 출력


# 4 백터에서 원소값 출력
d <-c(1,4,3,7,8)
d[1]
d[2]
d[6] # NA

# 4.1 백터에서 여러개의 값을 한번에 추출하기
d <- c(1,4,3,7,8)
d[c(1,3,5)]
d[1:3]
d[seq[1,5,2]]
d[-2] # 2번째값 제외하고 출력
d[-c(3:5)] # 3~5번째 값은 제외하고 출력

# 4.2 백터에서 이름으로 값을 추출하기


# 벡터 연산
# 1. 벡터와 숫자값 연산

# 2. 벡터와 벡터 간의 연산

# 3. 벡터에 적용가능한 함수
# sum, mean, median, max, min, var, sd, sort, range, length
# sort (d, decreasing=FALSE/TRUE)


# 4. 벡터에 논리연산자 적용
# 다른거 다 똑같다.  |, &


d <- c(1,2,3,4,5,6,7,8,9)
d >= 5
d[d>5] 
sum(d>5) # 몇개인지 
sum(d[d>5]) # 합이 얼만지
d==5

cond <- d>5 & d<8
d[cond]

# 리스트와 팩터
# 1. 리스트 (파이썬의 dictionary와 List의 짬뽕)
# 서로다른 자료형의 값들을 1차원 배열에 저장하고 다룰 수 있도록 해준다.
ds <- c(90, 85, 70, 84)
my.info <- list(name="tom", age=60, status=TRUE, score=ds)
my.info
my.info[[1]]
my.info$name
my.info[[4]]


# 2. 팩터
# 문자 데이터가 저장된 벡터의 일종
# 성별, 혈액형, 선호 정당 등과 같이 저장할 문자값들이 몇 종류로 정해져 있을때 사용

bt <- c('A', 'B','B','O','AB','A')
bt.new <- factor(bt)
bt
bt.new # 값과 함게 중복이 제거된 levels 값을 보여준다.
bt[5]
bt.new[5] # 개별 값과 함게 중복이 제거된 levels
levels(bt.new)
as.integer(bt.new) # 팩터의 문자값을 숫자로 바꾸어 출력
bt.new[7] <- 'B'
bt.new











































