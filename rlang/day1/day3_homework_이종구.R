# 1.R의 mtcars 데이터 셋을 사용하여 R 코드를 작성하시오

# (1). wt(중량)의 평균값, 중앙값, 절사평균값(절사범위:15%), 표준편차를 각각 출력
wt = mtcars$wt
mean(wt)
median(wt)
mean(wt, trim=0.15)
sd(wt)

# (2). wt의 통계요약 출력
summary(mtcars$wt)

# (3). cyl(실린더수)에 대해 도수분포표(빈도수)를 출력
cyl = mtcars$cyl
table(cyl)

# (4). 3번 데이터를 막대 그래프로 출력
barplot(table(cyl), main='실린더 수')

# (5). wt의 히스토그램 출력

hist(wt, 
     main="Histogram for 중량",
     xlab = "중량",
     ylab = "빈도수",
     border="blue",
     col="green",
     las=2,
     breaks=5)

# (6). wt의 상자그림 출력
boxplot(wt, main='boxplot for 중량')


# (7). disp(배기량)에 대한 상자그림 출력
disp = mtcars$disp
boxplot(disp, main='boxplot for 배기량')

# (8). gear(기어수)를 그룹 정보로 하여 mpg(연비)자료에 대해 상자 그림 출력
boxplot(mpg~gear,data=mtcars, main='그룹별')

# 2.R의 AirPassengers 데이터셋은 1949년~1960년 사이의 항공승객수를 월별로 나타낸
# 것이다. AirPassengers 데이터셋에서 1949, 1955, 1960년의 월별 승객수를 선그래프로
# 작성하여 출력(3개년도의 선의 색을 다르게 출력)

AirPassengers.1949 <- window(AirPassengers, 1949, c(1949,12))
AirPassengers.1955 <- window(AirPassengers, 1955, c(1955,12))
AirPassengers.1960 <- window(AirPassengers, 1960, c(1960,12))

top = max(c(max(AirPassengers.1949), max(AirPassengers.1955), max(AirPassengers.1960)))
bottom = min(c(min(AirPassengers.1949), min(AirPassengers.1955), min(AirPassengers.1960)))

month  <-  1:12
plot(month,AirPassengers.1949,
     main='USAccDeaths',
     type='o',
     lty=1,
     col='red',
     xlab='Month',
     ylab='USAccDeaths',
     ylim=c(bottom, top) 
)

lines(month, AirPassengers.1955, # line 추가
      type='o',
      col = 'blue')

lines(month, AirPassengers.1960, # line 추가
      type='o',
      col = 'green')


# 3. R의 airquality데이터 셋을 사용하여 R 코드를 작성하시오
airquality

# (1). airquality를 AQ에 저장
AQ <- airquality

# (2). AQ에서 열별로 NA의 개수를 출력
this.na = c()
for(i in 1:ncol(AQ)){
  this.na <- c(this.na, sum(is.na(AQ[,i])))
}
names(this.na) <- colnames(AQ)
this.na

# (3). AQ에서 행별로 NA의 개수를 출력
for(i in 1:nrow(AQ)){
  cat(rownames(AQ)[i],  sum(is.na(AQ[i,])), '\n')
}

# (4). AQ에서 NA를 포함하지 않은 행들만 출력
AQ[which(complete.cases(AQ)),]

# (5). AQ에서 NA를 NA가 속한 열의 평균값으로 치환하여 AQ2에 저장하고 출력
AQ2 <- AQ
for(i in 1:ncol(AQ) ){
  mean_wo_na = mean(AQ[,i], na.rm=T)
  # AQ2[which(is.na(AQ[,i])), i] <- mean_wo_na  # 둘다 가능, which 나 is나..
  AQ2[is.na(AQ[,i]), i] <- mean_wo_na
}
AQ2
#---------------------





























