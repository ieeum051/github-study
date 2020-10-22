class XFunctor f where  -- f는 타입 생성자다.(Maybe 같은)
    xfmap :: (a->b) -> f a -> f b


instance XFunctor Maybe where
    xfmap f (Just x) = Just (f x) -- xfmap 구현

instance XFunctor [] where
  xfmap _ [] = []
  xfmap f (x:xs) = f x : xfmap f xs -- xfmap 구현    