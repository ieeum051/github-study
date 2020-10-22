-- monad

f1nf2 n = case f1 n of 
            Nothing -> Nothing
            Just nn -> f2 nn


-- 실패의 가능성이 있는 함수들을 중첩해서 호출하면 상당히 복잡해 진다.

f1nf2 n = do
          nn <- f1 n -- 실패의 가능성을 고려한다.
          f2 nn

-- f1 4 => [0,1,2,3]
f1 :: Int -> [Int]
f1 n = [0..n-1]

-- 인자로 저달된 요소의 +1, -1값을 구하고 싶다.
f2 :: Int -> [Int]
f2 n = [n+1, n-1]

f1nf2 :: Int -> [Int]
f1nf2 n = concat (map f2 (f1 n))

f1nf2 n = do
          nn <- f1 n
          f2 nn


-- 비교 
af1nf2 :: Int -> Maybe Int
af1nf2 = do
         nn <- af1 n -- 실패의 가능성을 고려한 연산 (af1 nothing이면 af2에도 nothing이 입력됨
         af2 nn


bf1nf2 :: Int -> [Int]
bf1nf2 n = do
           nn <- bf1 n -- 복수의 요소를 고려한 연산
           bf2 nn

-- 똑같은 <- 연산이 문맥에 따라 다른 연산을 수행하게 된다. 이것을 모나드라함.
-- Maybe Monad : Int <- Maybe Int
-- List Monad : Int <- [Int]

-- 파이프라인 연산

bf1nf2 :: Int -> [Int]
bf1nf2 n = bf1 n >>= bf2  -- 좀더 간단하게..


-- IO Monad : String <- IO String
-- 부작용을 가질 수 있음.

main  = putStrLn "Hello"
main = do
    name <- getLine -- 순수함수가 아님. 이 함수는 부작용을 가질 수 있음을 나타냄
    putStrLn name


main = do
       name <- getLine
       addr <- getLine
       putStrLn(name ++ " " + addr)








