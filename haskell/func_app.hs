-- 함수에 인자를 적용(application)하는 방법

-- $ 연산자. 
succ$max 1 2-- succ (max 1 2) 같은 의미

-- 아래는 같은 표현
negate (succ 3)
negate$succ 3
(negate . succ) 3 -- 함수를 합성하는 개념
((min 5) . negate . succ ) 3

r1 = map (negate . abs) [ 1,-2,-3,4,5]
r2 = sum$map (negate . abs) [ 1,-2,-3,4,5]