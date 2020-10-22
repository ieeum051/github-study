-- module import

import Data.List
import Data>List (nub) -- numb만 import

-- 이름 충돌을 방지하기 위해 qualified를 붙이면 full name으로 사용해야함.
-- ex> Data.List.sort [3,13,7,9,6]
import qualified Data.List  


-- 각 자릿수의 합이 15가 되는 최초의 숫자는:
import Data.Char
import Data.List

-- digitToSum : 1423 -> 10
digitToSum :: Int -> Int
-- digitToSum x = .....; -- 일반적인 함수 구현
digitToSum = sum . map digitiToInt . show -- 함수 합성
-- 1423 => "1423" => [1 4 2 3] => 10

-- calcTo 15 ==> ???
calcTo :: Int->Maybe Int
--calcTo n = find (조건함수) [1..] -- 
calcTo n = find (\x-> digitToSum x == n) [1..] -- 




