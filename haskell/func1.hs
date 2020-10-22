

addPair :: Num a => (a, a) -> (a, a) -> (a, a)
addPair (x1, y1)(x2, y2) = (x1 + x2, y1 + y2)

myHead :: [a] -> a
myHead [] = error "empty list"
myHead (x:xs) = x

-- list의 처음 두개를 더하는 함수
addTwo :: Num a => [a] -> a
addTwo [] = error "empty"
addTwo (x:[]) = error "empty2"
addTwo (x:y:xs) = x + y

-- 문자열의 첫번째 요소가 공백이면 리턴
-- 공백이 아닌 경우 공백을 추가한 문자열 리턴

addSpace :: [Char] -> [Char]
addSpace str@(' ':xs) = str
addSpace xs = ' ':xs

-- case  표현식

translate :: Int -> String
translate x = "result " ++ case x of 1 -> "One"
                                     2 -> "Two"
                                     3 -> "Three"
                                     _ -> "Sorry"

-- Guard
grade :: Int -> Char
grade score
 | score < 60 = 'F'
 | score > 90 = 'A' 
 | otherwise = 'B'

grade2 :: Double -> Double -> Char
grade2 s1 s2
 | score < minScore = 'F'
 | score > maxScore = 'A' 
 | otherwise = 'B'
 where score = (s1 + s2) /2
       minScore = 60
       maxScore = 90


say [] = []
say (x:xs) = xs ++ [x]

factorial :: Int -> Int
factorial 1 = 1
factorial n = n * factorial (n-1)

-- myrepeat :: a -> a
-- myrepeat a = a : myrepeat a

-- myreverse :: [a] -> [a]
-- myreverse [] = []
-- myreverse (x:xs) = myreverse xs ++ x

foo :: Int -> Int
foo x = x

goo :: Int -> (Int -> Int)
goo x = foo

add3 :: Int -> Int -> Int -> Int
add3 x y z = x + y + z

add2 = add3 0

-- Section
kmToMeter = (*1000)
hoo = (+5)

-- higher-order function 고차함수
-- 인자를 함수로 받거나 전달하는 함수
applyTwice :: (a->a)->a->a
applyTwice f x = f (f x) -- 인자가 1개인 함수가 f에 들어감

-- applyTwice (+5) 3  -- 인자 2개 함수를 전달하는 방법
-- applyTwice (\x->x*2) 5 -- (\x->x*2)람다 표현식 '\'로 시작한다.
-- applyTwice ((\x->x*y)3) 5 -- (\x->x*2)람다 표현식 '\'로 시작한다.

r6 = zipWith (zipWith (+)) [[1,2], [3,4], [5,6]] [[10,20], [30,40], [50,60]]

myzipWith :: (a -> b -> c)->[a]->[b]->[c]
myzipWith _ _ [] = []
myzipWith _ [] _ = []
myzipWith f (x:xs) (y:ys) = f x y : myzipWith f xs ys


