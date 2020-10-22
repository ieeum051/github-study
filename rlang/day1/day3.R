# 데이터 전처리

# 1. 결측값의 개념
# 결측값(missing value), 통계조사에서 응답자가 어떤 문항에 대해 응답을 안했다고 하면
# 그 문항의 데이터값은 결측값
# 처리방법 : 1) 제거, 2) 추정

# 2. 벡터의 결측값 처리
# 2.1 결측값의 특성과 존재 여부 확인

z <- c(1,2,3,NA, 5, NA, 8)
sum(z)
is.na(z)
sum(is.na(z))
sum(z, na.rm=T) # na.rm : NA를 제외하고 합계를 계산

# 2.2 결측값 대체 및 제거
z1 <- c(1,2,3,NA,5,NA,8)
z2 <- c(5,8,1,NA, 3, NA, 7)
z1[is.na(z1)] <- 0 # NA를 0으로 치환
z1
z3 <- as.vector(na.omit(z2)) # na.omit : NA를 제거하고 새로운 벡터 생성
z3

# 3. 매트릭스와 데이터프레임의 결측값 처리
# 3.1 결측값이 포함된 데이터프레임 생성
x <- iris
x[1,2] <- NA;x[1,3] <- NA
x[2,3] <- NA;x[3,4] <- NA
head(x)

# 3.2 데이터프레임의 열별 결측값 확인

# for문을 이용한 방법
for (i in 1:ncol(x)){
  this.na <- is.na(x[,i]) # 각각의 항목의 T,F 를 벡터로 생성
  cat(colnames(x)[i], '\t', sum(this.na), '\n')
}

ds <- iris
ds[1,2] <- NA;ds[1,3] <- NA
ds[2,3] <- NA;ds[3,4] <- NA

idx <- c()
for(i in 1:nrow(x)){
  if(sum(is.na(ds[i,])) > 0){
    idx <- c(idx, i)
  }
}
ds[idx,]

cnt <- 0
for(i in 1:nrow(ds)){
  if(sum(is.na(ds[i,])) > 0){
    cnt <- cnt + 1
  }
}
cnt


 
# apply를 이용한 방법
col_na <- function(y){
  return(sum(is.na(y)))
}
na_count <- apply(x, 2, FUN=col_na) # x의 2(열, column)의 값을 col_na로 전달, 열 각각의 벡터 생성
na_count

# 3.3 데이터프레임의 행별 결측값 확인
rowSums(is.na(x))
sum(rowSums(is.na(x))>0)

sum(is.na(x)) # 데이터셋 전체에서 NA갯수

# 3.4 결측값을 제외하고 새로운 데이터셋 만들기
head(x)
x[!complete.cases(x),] # NA가 파함된 행들 출력, complete.cases 는 NA없는 행들
y <- x[complete.cases(x),]
head(y)

# 특이값
# 1. 특이값의 개념
# 특이값의 분류 기준
# a. 논리적으로 확인 (범위가 1~7인데 9, 몸무게인데 마이너스)
# b. 상식을 벗어난 값이 있는지 (나이가 120살)
# c. boxplot 

# 2. 특이값의 추출 및 제거
# 2.1 상자그림을 통한 특이값 확인
st <- data.frame(state.x77)
st$Income
boxplot(st$Income)
boxplot.stats(st$Income)
boxplot.stats(st$Income)$out # max(st$Income) 와 동일

# 2.2 특이값을 포함한 행 제거
out.val <- boxplot.stats(st$Income)$out
st$Income[st$Income %in% out.val] <- NA # st$Income %in% out.val 
head(st)
newdata <- st[complete.cases(st),] # NA가 포함된 행(alaska) 제거
head(newdata)

# 데이터 정렬
# 1. 벡터의 정렬
v1 <- c(1,7,6,8,4,2,3)
order(v1) # 정렬에 맞게 색인만
# 왜 order가 필요한가? index를 가지고 있으면 축 자체를 이동시킬 수 있다.
# 예> 매트릭스 행렬에서 하나의 column만 sorting하면 나머지 column의 정보가 어긋나진다.
# 


v1 <- sort(v1)
v1
v2 <- sort(v1,decreasing=T)
v2

# 2. 매트릭스와 데이터프레임 정렬
head(iris)
order(iris$Sepal.Length)
iris[order(iris$Sepal.Length),] # Sepal.Length에 따라 모든 columne이 정렬됨.
iris[order(iris$Sepal.Length, decreasing=T),] # 기본은 오름, 내림은 옵션필요

iris.new <- iris[order(iris$Sepal.Length, decreasing=T),]

head(iris.new)
iris[order(iris$Species, decreasing=T, iris$Petal.Length),] # 정렬기준이 2개
iris[order(iris$Species, decreasing=T, -iris$Petal.Length),] # - 는 역방향

#  데이터 프레임 변경후
st <- data.frame(state.x77)
st[order(st$Population),]
st[order(st$Income, decreasing=T),]

# for 문 이용 10개 추출
new_st <- st[order(st$Illiteracy), ]  
for (i in 1:10){
  cat(rownames(new_st[i, ]), new_st[i, ]$Illiteracy, '\n') 
}

# head 사용 - 훨씬 깔끔
head(st[order(st$Illiteracy), ], n=10)['Illiteracy']


st2 <- state.x77 # 매트릭스
st2[order(st2[,'Population']),]
st2[order(st2[,'Income'], decreasing=T),]

# 그냥 가져오는 방법
new_st <- st2[order(state.x77[,'Illiteracy']),]
new_st[1:10, 'Illiteracy']





# 데이터 분리와 선택

# 1. 데이터 분리
sp <- split(iris, iris$Species) 
sp
class(sp) # 리스트 
summary(sp)
sp$setosa # setosa에 대한 데이터 확인

# 2. 데이터 선택
subset(iris, Species == 'setosa')
subset(iris, Sepal.Length > 7.5)
subset(iris, Sepal.Length >5.1 & Sepal.Width > 3.9)
subset(iris, Sepal.Length > 7.6, select = c(Petal.Length, Petal.Width))


# 데이터 샘플링과 조합
# 1. 데이터 샘플링
# 복원추출 (추출한 대상을 다시 복원), 비복원추출 (추출한 대상은 제외)
# 1.1 숫자를 임의로 추출하기
x <- 1:100
y <- sample(x, size=10, replace=F) # 비복원 추출
y

# 1.2 행을 임의로 추출하기
idx <- sample(1:nrow(iris), size=60, replace=FALSE) #replace : 복원 여부
iris.50 <- iris[idx,]
dim(iris.50) # 행과 열의 개수 확인
head(iris.50)

# 1.3 set.seed()함수 이해하기
sample(1:20, size=5)
sample(1:20, size=5)
sample(1:20, size=5)

set.seed(100) # 난수에 대한 seed 값
sample(1:20, size=5)
set.seed(100)
sample(1:20, size=5)
set.seed(100)
sample(1:20, size=5)

head(iris)
table(iris$Species)

# 내가 푼 방식
setosa <- subset(iris, Species =='setosa')
setosa[sample(1:nrow(setosa), 10),]

versicolor <- subset(iris, Species =='versicolor')
versicolor[sample(1:nrow(versicolor), 10),]

virginica <- subset(iris, Species =='virginica')
virginica[sample(1:nrow(virginica), 10),]

# 강사
idx <- sample(1:50, 10)
iris.10 <- rbind(setosa[idx,], versicolor[idx,], virginica[idx,])
iris.10




# 2. 데이터 조합
# 조합(combination) : 글자 그대로 주어진 데이터값들 중에서 몇개씩 짝을 지어 추출하는 작업

combn(1:5, 3) 

x <- c('red', 'green', 'blue', 'black', 'white')
com <- combn(x,2)
com

for(i in 1:ncol(com)){
  cat(com[,i], '\n')
}

unique(iris$Species) # 중복제외
species <- unique(iris$Species)
combn(species,2)

# 1. 데이터 집계(aggregate)
# 1.1 iris 데이터셋에서 각 변수의 품종별 평균출력
# * 2차원 데이터는 데이터 그룹에 대해서 합계나 평균을 계산해야하는 일이 많음
#   이와 같은 작업을 집계(aggregation)이라고 함.

# by=list(iris$Species), iris$Species는 팩터
agg <- aggregate(iris[,-5], by=list(iris$Species), FUN=mean) 
agg

# 데이터 집계와 병합
# 1.1 iris 데이터셋에서 각 변수의 품종별 표준편차 출력

# 그냥하면 Group.1 이던 값이 '표준편차' 로 뀜
aggregate(iris[,-5], by=list(표준편차=iris$Species), FUN=sd) 
aggregate(iris[,-5], by=list(iris$Species), FUN=sd)

# 1.2 mtcars 데이터셋에서 각 변수의 최댓값 출력
head(mtcars)
aggregate(mtcars, by=list(cyl=mtcars$cyl, vs=mtcars$vs), FUN=max)

# 데이터 집계와 병합
# 2. 데이터 병합
# 병합(merge) : 분리된 데이터 파일을 공통 컬럼을 기준으로 하나로 합치는 작업
x <- data.frame(name=c('a','b','c'), math=c(90,80,40))
y <- data.frame(name=c('a','b','d'), korean=c(15,60,90))
x
y

z <- merge(x,y,by=c('name')) # 병합의 기준이 'name, 일치하는 데이터만 merge하여 생성
z

x <- data.frame(name=c('a','b','c'), math=c(90,80,40))
y <- data.frame(sname=c('a','b','d'), korean=c(15,60,90))
merge(x,y,by.x=c('name'),by.y=c('sname')) # 각각의 다른 열 이름의 공통값을 일치시키도록 

