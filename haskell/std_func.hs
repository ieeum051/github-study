

z1 = zipWith (+) [1,2,3,4] [5,6,7,8]
z2 = zipWith max [1,8,9,3] [2,3,7,8]
z3 = zipWith (++) ["A", "B", "C"] ["A", "Y", "Z"]
z4 = zipWith (*) (replicate 3 1) [1..]
z5 = zipWith (zipWith (*)) [[1,2],[3,4],[5,6]] [[10,20],[30,40],[50,60]]


fi1 = filter ( < 10) (filter even [1..20])
fi2 = filter (`elem`['a'..'z']) "I am a boy"
-- fi2 = filter 
fi3 = filter (\x ->if x `mod` 3 == 0 then True else False) [1..100]

myfilter :: (a->Bool) [a] -> [a]
myfilter p (x:xs)
  | p x = x : myfilter p xs
  | otherwise = myfilter p xs

-- (\x -> x+1) 3
-- zipWith

-- flip

-- map

-- filter