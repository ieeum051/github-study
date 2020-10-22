-- map 함수와 동일하게 동작하는 mymap 함수를 구현해 보세요.
-- > mymap (\x->x*2) [1,2,3,4]
-- [2,4,6,8]

mymap :: (a ->b) -> [a] -> [b]
mymap _ [] = []
mymap f (x:xs) = f x : mymap f xs