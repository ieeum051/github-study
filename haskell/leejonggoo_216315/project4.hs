-- 다음 코드는 Tree를 타입으로 설계한 코드 입니다.
data Tree a = Empty | Node a (Tree a) (Tree a) deriving (Show, Read, Eq)

-- 4-1. tree에 항목을 추가하는 insertTree 함수 를 만들어 보세요.
{-
> insertTree 10 Empty
Node 10 Empty Empty
> insertTree 20 (Node 10 Empty Empty)
Node 10 Empty (Node 20 Empty Empty)
-}

-- 4-2. tree에 항목이 있는지 검색하는 elemTree 함수를 만들어 보세요.
{-
> st = [1,3,5,7,2,4,6,8]
> tree = foldr insertTree Empty st
> elemTree 5 tree
True
> elemTree 15 tree
False
-}

insertTree :: Int -> Tree Int -> Tree Int
insertTree a Empty  = Node a Empty Empty
insertTree a (Node b tree_c tree_d) = Node b tree_c (insertTree a tree_d)
 
st = [1,3,5,7,2,4,6,8]
tree = foldr insertTree Empty st

elemTree :: Int -> Tree Int -> Bool
elemTree a Empty = False
elemTree a (Node b tree_c tree_d)
 | a == b = True
 | otherwise = elemTree a tree_c || elemTree a tree_d

