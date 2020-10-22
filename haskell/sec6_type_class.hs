-- type class
isSame1 :: Int->Int->Bool
isSame1 x y = ( x == y)

isSame2 :: (Eq a) => a->a->Bool
isSame1 x y = ( x == y)


-- 타입 클래스
-- 타입이 가져야하는 특정 동작을 정의한 인터페이스
-- Int, Double, String, Bool 은 Eq 타입 클래스의 인스턴스


-- 사용자 정의 타입 클래스
-- BoolConvertible

-- 타입 클래스 만들기
-- class 타입 클래스 이름 타입파라미터 where
--    동작을 정의한 함수 선언들

class BoolConvertible a where
    isTrue :: a -> Bool -- BoolConvertible은 반드시 isTrue 함수가 있어야한다.
    isFalse :: a -> Bool
    isFalse x = not (isTrue x) -- default 구현
    isTrue x = not (isFalse x)

-- 일반화 함수
-- check 0 1 => 1
-- check 3 2 => 3
check :: (BoolConvertible a) => a->a->a
check x y = if isTrue x then x else y

-- 아직 인스턴스를 안 만듬, 타입 클래스 인스턴스가 필요함
-- Int 타입을 BoolConvertible 타입 클래스의 인스턴스로 만들기

instance BoolConvertible Int Where
    isTrue 0 = False
    isTrue x = True


-- Functor, Applicative, Monad

-- Functor 타입 클래스
class Functor f where  -- f는 타입 생성자다.(Maybe 같은)
    fmap :: (a->b) -> f a -> f b




mod 10 3 
mod 10.3 3.1 -- 오류

fmap (*2) [2]
fmap (*2) [2,1,3]
fmap (*2) (2:Int) -- 오류 발생

echo : Maybe Int -> Maybe Int
echo x = x

class XFunctor f where  -- f는 타입 생성자다.(Maybe 같은)
    xfmap :: (a->b) -> f a -> f b

-- Maybe를 xFunctor의 인스턴스로 만들기
instance XFunctor Maybe where
    xfmap f (Just x) = Just (f x) -- xfmap 구현

instance XFunctor [] where
    xfmap _ [] = []
    xfmap f (x:xs) = f x : xfmap f xs -- xfmap 구현

-- xfmap (*2) (Just 2)

-- Applicative, Monad
-- <*> 함수
[ (+1), (*3)] <*> [1,2,3] -- [1,2,3]에 대해 (+1) 연산수행하고 
-- (*3) 연산 수행하고 하나로 합침. 이를 위한 명령어가 <*> 임
(+3) <*> 3 -- 에러 발생, 리스트, Maybe, Io에서만 사용가능

-- >>== 연산자, 
-- 모나드 타입 클래스의 인스턴스 타입에만 사용할 수 있다. (리스트, Maybe, IO)
[1,2,3] >>= (\x -> [x, -x]) -- 
Just 3 >>= (\x -> Just (x *3)) -- 각각의 특성에 맞게 사용가능

:i Monad
:i Applicative





