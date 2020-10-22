# . 아래의 내용을 이용하여 코드를 작성하시오

# >score
 
# m  f
# 
# [1,] 10 21
# 
# [2,] 40 60
# 
# [3,] 60 70
# 
# [4,] 20 30
 
# (1). 위와 같은 내용의 매트릭스 score를 생성하여 출력
m <- c(10,40,60,20)
f <- c(21,60,70,30)
score <- matrix(c(m,f), nrow=4, ncol=2)
colnames(score) <- c('m', 'f')
score

# (2). score의 열 이름을 각각 male, female로 바꾸어 출력
colnames(score) <- c('male', 'female')
score
 
# (3). 2행의 모든 값 출력
score[2,]
 
# (4). female의 모든 값 출력
score[,'female']
 
# (5). 3행 2열의 값 출력
score[3,2]
 
# 2. R의 데이터셋 state.x77 데이터셋을 이용하여 코드를 작성하시오
 
# (1).  state.x77을 변환하여 st에 데이터프레임으로 변환
st <- as.data.frame(state.x77)
# (2).  st 출력
st 
# (3).  st의 행의 개수와 열의 개수를 출력
dim(st)
 
# (4).  st의 요약 정보 출력
str(st) 

# (5).  st의 행별 합계와 평균 출력
rowSums(st)
rowMeans(st)
 
# (6).  st의 열별 합계와 평균 출력
colSums(st)
colMeans(st)
 
# (7).  Florida 주의 모든 정보 출력
st['Florida',]
 
# (8).  50개 주의 수입(Income) 출력
st[,'Income']

# (9).  Texas 주의 면적(Area) 출력
st['Texas', 'Area']
 
# (10).인구(population)가 5,000 이상인 주의 데이터만 출력
subset(st, Population >= 5000)

# (11).수입이 4,500 이상인 주의 인구, 수입, 면적 
st <- as.data.frame(state.x77)

subset(st[c('Population', 'Income', 'Area')], Income >= 4500) 
subset(st, Income >= 4500, select=c('Income', 'Area')) # ext. solution 1
subset(st, Income >= 4500)[,c('Income', 'Area')] # ext. solution 2
 
# (12).전체 면적(Area)이 100,000 이상이고 결빙일수(Frost)가 120 이상인 주의 정보 출력
subset(st, Area >= 100000 & Frost > 120)

# (13).문맹률(Illiteracy)이 2.0이상인 주의 평균 수입이 얼마 인지 출력
subset(st, Illiteracy >=2.0)
colMeans(subset(st, Illiteracy >=2.0)['Income'])

mean(subset(st, Illiteracy>=2.0)$Income) # ext. solution
 
# (14).기대수명(Life Exp)이 가장 높은 주는 어디 인지 출력
rownames(subset(st, st['Life Exp'] == max(st['Life Exp'])))


# (15).Pennsylvania 주보다 수입이 높은 주들을 출력
rownames(subset(st, Income > st['Pennsylvania', 'Income']))

# 3.10명의 몸무게를 저장한 벡터가 아래와 같다
weight <-c(69,50,55,71,89,64,59,70,71,80)

# (1). 몸무게가 가장 큰 값은 몇 번째에 인지 출력
max(weight)
which(weight == max(weight) )
 
# (2). 몸무게가 61에서 69 사이인 값을 몇 번째에 있는 지 출력
which(weight > 61 & weight < 69 )

# (3). 몸무게가 60 이하인 값들만 추출하여 weight.2에 저장하고 출력
weight.2 <- weight[which(weight <= 60 )]
weight.2

