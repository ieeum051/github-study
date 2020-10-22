# R 변수와 백터
# 1. 산술연산과 주석
5+8
3+(4*5)
a<-10
print(a)

# 2. 산술연산 함수

# 산술연산
# 나머지는 타언어와 동일, %% - 나눗셈의 나머지

# 기본연산
# log(), sqrt(), max(), min(), abs(), factorial()
# sin(), cos(), tan()

log(10)+5
sqrt(25)
max(5,3,2)

# 1. 변수의 개념
# 2. 변수명 지정
# 3. 변수에 값 저장 및 확인
# 4. 변수의 자료형
# 숫자형 : 1, 2, 3
# 문자형 : "TOM"
# 논리형 : TRUE, FALSE, - T, F 도 가능
# 특수값 : NULL, NA, NaN, Inf, -Inf

# NULL : 정의되어있지 않음을 의미, 자료형도 없고 길이도 0
# NA : 결측값 (missing value)
# NaN : 수학적으로 정의가 불가능한값. ( sqrt(-3))

# 5. 변수의 값 변경

# 1. 벡터의 개념
# 1차원 형태의 데이터를 저장할 수 있는 저장소 

# 2. 벡터 만들기 
x<-c(1,2,3) # 숫자형 백터
typeof(x)
y<-c("a", "b", "c") # 문자형 백터
typeof(y)
z<-c(TRUE, FALSE, TRUE) # 논리형 백터
typeof(z)

# 2.1. 연속적인 숫자로 이루어진 벡터의 생성
v1 <- 50:90
v1
v2<-c(1,2,4, 50:90)
v2

# 2.2. 일정한 간격의 숫자로 이루어진 벡터 생성
v3 <- seq(1,101,3) # 1 ~ 101, 간격 3
v3
v4 <- seq(0.1, 1.0, 0.1)
v4

# 2.3. 반복된 숫자로 이루어진 백터 생성
v5 <- rep(1, times=5) 
v5
v6 <- rep(1:5, times=5) # 전체를 반복
v6
v7 <- rep(c(1,5,9), times=3)
v7
v8 <- rep(c(1,2,3), each=2) # 각각을 반복
v8
v9 <- rep(c(1,2,3), each=2, times=3) 
v9

# 3. 백터의 원소값에 이름 지정
score <- c(90, 85, 70) # 성적 데이터
score
names(score)
names(score) <- c("John", "Tom", "Jane") # 각 성적에 이름을 부여
names(score)
score  # 이름과 함께 출력

# 4. 백터에서 원소값 추출
d <-c(1,4,3,7,8)
d[1]
d[2]
d[6] # NA

# 4.1. 벡터에서 여러개의 값을 한번에 추출하기
d <- c(1,4,3,7,8)
d[c(1,3,5)]
d[1:3]
d[seq[1,5,2]]
d[-2] # 2번째값 제외하고 출력
d[-c(3:5)] # 3~5번째 값은 제외하고 출력

# 4.2. 벡터에서 이름으로 값을 추출하기
GNP <- c(2090, 2450, 960)
GNP
names(GNP) <- c("korea", "japan", 'nepel')
GNP
GNP[1]
GNP["korea"]
GNP[c("korea", "japan")]

# 5. 백터에 저장된 원소값 변경
v1 <- c(1,5,7,8,9)
v1
v1[c(1,5)] <- c(10,20)
v1

# 1. 벡터와 숫자값 연산
d <- c(1,4,3,7,8)
2*d
d-5
3*d+4

# 2. 벡터와 벡터간의 연산
x <- c(1,2,3)
y <- c(4,5,6)
x+y
x*y
z <- x+y # 연산을 통해 새로운 벡터 생성
z
# 3. 벡터에 적용 가능한 함수
# sum, mean, median, min/max, var, sd, sort, range, length

d <- c(1,2,3,4,5,6,7,8,9)

sort (d, decreasing=F) # sort (d, T), sort (T, d)
sort (d, decreasing=T)

# 4. 벡터에 논리연산자 사용
d <- c(1,2,3,4,5,6,7,8,9)
d >= 5
d[d>5] 
sum(d>5) # 몇개인지 
sum(d[d>5]) # 합이 얼만지
d==5

cond <- d>5 & d<8
d[cond]

# 1. 리스트 (파이썬의 dictionary와 List의 짬뽕)
# 서로다른 자료형의 값들을 1차원 배열에 저장하고 다룰 수 있도록 해준다.

ds <- c(90, 85, 70, 84)
my.info <- list(name="tom", age=60, status=TRUE, score=ds)
my.info
my.info[1] # name, tom을 다 보여줌
my.info[[1]] # name은 skip
my.info$name
my.info[[4]]


# 2. 팩터 (for 범주형 자료)
# 문자 데이터가 저장된 벡터의 일종
# 성별, 혈액형, 선호 정당 등과 같이 저장할 문자값들이 몇 종류로 정해져 있을때 사용
# 팩터형은 쉽게 새로운 범주를 추가하거나, 범주가 다른 두 팩터를 합칠 수 없다. 



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


#  R의 매트릭스와 데이터 프레임

# 1. 매트릭스의 개념
# - 매트릭스(matrix) : 모든 셀의 값들이 동일한 자료형
# - 데이터프레임(data frame) : 자료형이 다른 컬럼들로 구성


# 2. 매트릭스 만들기
# 2.1. 기본적인 메트릭스 만들기

z <- matrix(1:20, nrow=4, ncol=5)
z

# 2.2. 메트릭스에 저장될 값들을 행 방향으로 채우기
z2 <- matrix(1:20, nrow=4, ncol=5, byrow=T) # byrow=T 추가됨
z2

# 2.3. 기존 메트릭스에 벡터를 추가하여 새로운 메트릭스 만들기

x <- 1:4
y <- 5:8
z <- matrix(1:20, nrow=4, ncol=5)
m1 <- cbind(x,y) # x와 y를 열 방향으로 결합하여 매트릭스 생성
m1
m2 <- rbind(x,y) # x와 y를 행 방향으로 결합하여 매트릭스 생성
m2
m3 <- rbind(m2,y) # m2에 y를 행 방향으로 추가함.
m3
m4 <- cbind(z,x) # z 매트릭스에 x값을 열방향으로 추가함
m4

# 3. 매트릭스에서의 값 추출
# 3.1. 인덱스 값을 이용하여 메트릭스에서의 값 추출하기
z <- matrix(1:20, nrow=4, ncol=5)
z
z[2,3] # 2행 3열
z[2,] # 2행 모든 값

# 3.2. 매트릭스에서의 여러 개의 값을 동시에 추출하기
z <- matrix(1:20, nrow=4, ncol=5)
z

z[2,1:3] # 2행의 1~3 열
z[,c(1,4)]

# 4. 매트릭스의 행과 열에 이름 지정
# 4.1. 매트릭스의 행과 열에 이름을 지정하는 방법
score <- matrix(c(90,85,69,78,
                  85,96,49,95,
                  90,80,70,60),
                  nrow=4, ncol=3)
score
rownames(score) <- c('John', 'Tom', 'Mark', 'Jane')
colnames(score) <- c('English', 'Math', 'Science')
score
# 4.2. 행과 열에 지정한 이름을 이용하여 매트릭스 값 추출하기

score['John', 'Math']
score['Tom', c('Math', 'Science')] # Tom의 Math, Science성적
score['Mark',] # Mark의 모든 성적
score[, 'English'] # 모든 학생의 영어 성적
rownames(score)
colnames(score)
colnames(score)[2]

# 데이터 프레임
# 매트릭은 같은 형태지만 데이터 프레임은 다른 형태의 데이터도 가능

# 1. 데이터 프레임의 개념
# 2. 데이터 프레임 만들기
city <-  c("Seoul", "Tokyo", "Washington")
rank <- c(1,3,2)
city.info <- data.frame(city, rank)
city.info

# 3. iris 데이터셋
# R에서 제공하는 실습용 데이터 셋중의 하나로 데이터 프레임 형식
# 150 그루의 붓꽃에 대해 4개 분야의 측정 데이터와 품종 정보를 결합하여 만든 데이터셋
iris[,c(1,2)]
iris[,c("Sepal.Length", "Species")]
iris[1:5,]
iris[1:5, c(1,3)]


# 메트릭스와 데이터프레임 다루기
# 1. 데이터셋의 기본 정보 확인
# 1.2. iris 데이터셋의 추가적인 내용 확인하기
# * 매트릭스와 데이터 프레임은 모두 2차원 형태의 데이터를 저장하는 자료구조이기 때문에 
#   다루는 방법이 대부분 동일

dim(iris) # 행과 열의 개수
nrow(iris) # 행의 개수
ncol(iris) # 열의 개수
colnames(iris) # 열 이름 출럭, names()와 결과 동일
head(iris) # 앞 행 일부 출력
tail(iris) # 마지막 부분의 행 일부 출력

str(iris) #  데이터셋 요약 정보보기
iris[,5] # 품종 데이터만 보기
unique(iris[,5]) # 중복 제거
table(iris[,"Species"]) # 종류별 행의 개수 세기

# 2. 매트릭스와 데이터프레임에서 사용하는 함수
# 2.1. 행별, 열별 합계와 평균 계산

colSums(iris[,-5]) # 열별 합계, -5 : 5열은 품종이므로 제외
colMeans(iris[,-5]) # 열별 평균
rowSums(iris[,-5]) # 행별 합계
rowMeans(iris[,-5]) # 행별 평균

# 2.2. 
# 2.3. 행과 열과 방향 전환 : t
z <- matrix[1:20, nrow=4, ncol=5]
z
t(z)  # 행과 열의 방향전환 


# 2.4. 조건에 맞는 행과 열의 값 추출 : subset
# matrix는 잘 안됨. dataframe으로 전환 후 사용해야함.
IR.1 <-  subset(iris, Species == "setosa")
IR.1
IR.2 <-  subset(iris, Sepal.Length > 5.0 & Sepal.Width > 4.0)
IR.2


# 2.5. 매트릭스와 데이터프레임에 산술 연산
a <- matrix(1:20, 4, 5)
b <- matrix(21:40, 4, 5)
a
b

2*a
b-5
2*a + 3*b

a+b
b-a
b/a
a*b

a <- a*3
b <- b-5

# 3. 매트릭스와 데이터프레임의 자료구조 확인

# 3.1. 매트릭스와 데이터프레임의 자료구조 확인
class(iris)




# 3.2. 매트릭스와 데이터 프레임의 자료구조 변환
# a. 자료 구조 확인
class(iris)  
class(state.x77)
is.matrix(iris3)
is.data.frame(iris3)
is.matrix(state.x77)
is.data.frame(state.x77)

# b. 변환
# 매트릭스 -> 데이터프레임
st <- data.frame(state.x77)
head  # 윗쪽 행 6줄 
class(st)

# 데이터프레임 -> 매트릭스
iris.m <- as.matrix(iris[,1:4])
iris.m
head(iris.m)
class(iris.m)

# 4. 데이터프레임의 열 추출
# - 모든 방식이 데이터 프레임 가능, 가장 활용도 높음.
# - 벡터, 매트릭스 제한적

# 1. 파일 형식 변환
class(iris)
iris[,"Species"]  # 결과=백터, 매트릭스(2차원 이니까)와 데이터프레임 모두 가능 
class(iris[,"Species"]) # 팩터
iris[,5]    
iris["Speicies"]   # 결과=데이터프레임만 가능
iris[5]
class(iris[5])  # 데이터 프레임

iris$Species       # 결과=벡터, 데이터프레임만 가능 (1차원이니까.)
class(iris$Species) # 팩터


# 2. 파일 데이터 읽기
setwd("Z:\private\github-study\rlang\day1")
air <- read.csv("airquality.csv", header=T)
head(air)

my.iris <- subset(iris, Species='Setosa')


# 3. 파일 데이터 쓰기
# row.names=F : 행 번호를 붙이지 말라.
write.csv(my.iris, "my_iris.csv", row.names=F)






















