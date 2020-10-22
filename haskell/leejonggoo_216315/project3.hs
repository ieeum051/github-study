-- 과제 3. substr 함수 구현하기
-- 부분 문자열을 구하는 substr 함수를 구현해 보세요
-- > substr "abcdef" 1 3
-- “bcd”

substr :: [Char] -> Int -> Int -> [Char]
substr [] _ _ = []
substr (x:xs) st end
 | end < 1 = []
 | st < 1 = x: substr xs st (end-1)
 | otherwise = substr xs (st-1) (end-1)