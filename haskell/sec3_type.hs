-- Section 3. Type & Type class

-- 타입 만들기

convert :: Double->Double
covert m = m * 1.093613

-- 가독성 확보
-- 기존 타입 활용
type Meter = Double 
type Yard = Double
convert2 :: Meter -> Yard
covert2 m = m * 1.093613

-- 기존 타입을 새로운 타입으로
newtype Meter = Meter Double  -- 앞에 newtype와 생성자 (Meter ) 추가
newtype Yard = Yard Double -- Yard 3

-- 테스트 함수
foo :: Meter->Int
foo m = 0 -- foo $ Meter 3 -- Meter 3을 data constructor라고 함.

getValue :: Meter -> Double -- Meter 3에서 3을 가져올 때
getValue (Meter m) = m  -- 이렇게 만드는 것이 중요함.

-- 3. 타입 클래스의 인스턴스로 만들기

-- 3-1. Meter 타입 출력하기
newtype Meter = Meter Double deriving Show -- deriving 지시어를 사용하여 Show 타입 인스턴스로 만들었다.

-- 3-1. instance 구문 
-- 화면에서 출력되는 형식을 변경한다.
newtype Meter = Meter Double
newtype Yard = Yard Double

instance Show Yard where
    show (Yard y) = show y ++ " yd"

instane Show Meter where
    show (Meter m) = show m ++ " meter"

-- Meter를 Yard로 변경
-- m을 조작하는 방식에 주목
convert :: Meter -> Yard
convert (Meter m) = Yard (m * 1.093613)

-- data를 활용한 새로운 타입 만들기
data Point = Point Double Double
data Point = Point Double Double deriving Show
-- data Shape = Circle Double Double Double | Rectangle Double Double Double deriving Show
data Shape = Circle Point Double | Rectangle Point Point deriving Show

-- 면적을 구하는 함수
area :: Shape -> Double
area (Circle _ r) = 3.14 * r ^ 2
area (Rectangle (Point x1 y1) (Point x2, y2)) = (x2-x1) * (y2 - y1)

-- record 구문
data People = People String Int String deriving Show

getName :: People -> String
getName (People n _ _) = n

getAge :: People -> Int
getName (People _ n _) = n

data People = People {name::String,
                      age::Int,
                      addr::String} deriving Show

{-
name (People "kim" 2 "seould")
name People {age=2, name="kim", addr="seoul"}
-}

-- 필드가 없는 생성자
data Bool = True | False
data Week = Mon | Tue | Wed | Thu | Fri | Sat | Sun deriving (Show, Eq ,Enum)

-- 3-2. 타입생성자 / 타입 파라미터
data Shape a = Rectangle a a a a deriving Show

-- Shape a 를 타입 생성자라로 부름.
area :: Num a => Shape a-> a
area (Rectangle x1 y1 x2 y2) = (x2 - x1) * (y2 - y1)

-- Maybe (타입 생성자)
-- data Maybe a = Nothing | Just a

next :: Num a => a -> Maybe a
next x
 | x > 5 = Just $ succ x
 | otherwise = Nothing


getValue :: Maybe Int -> Int
getValue (Just m) = m
getValue Nothing = 0


-- Example (재귀적인 데이터 구조)

data List = Empty | Node Int List deriving Show
-- Empty는 데이터가 없는 경우
-- Node 10 $ Node 20 Empty

data List a = Empty | Node a (List a) deriving Show

-- 특수 문자로 생성자 만들기
-- Node => :+

-- Empty  == []
-- 1:[] == 1:+Empty

data List a = Empty | :+ a (List a) deriving Show
-- 특수문자는 중위 연산자이므로  :+ a --> a :+
data List a = Empty | a :+ (List a) deriving Show
{-
10 :+ Empty
20 :+ (10 :+ Empty)
-}

--원래 리스트와 유사 
-- Empty == []
-- 1:[] == 1:+Empty

-- foldr을 사용한 하스켈 리스트 요소를 List에 넣기
r1 = foldr (:+) Empty [1,2,3,4]

-- List에 요소가 있는지 검색 -- elem
-- myFind 5 (4 :+ Empty )-- myFind 5 List
-- 
myFind :: (Eq a) => a -> List a -> Bool
myFind _ Empty = False
myFind v (f:+st)
  | v == f = True
  | otherwise = myFind v st

