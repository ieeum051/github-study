-- 다음은 이름과 점수를 튜플의 리스트로 표현한 코드 입니다.
-- [(“Kim”, 60), (“Park”,80), (“Choi”, 70), (“Lee”, 90), (“Jung”, 85)]
-- 이중에서 점수가 80점이상(80점 포함)인 항목만 가진 리스트를 구하는 코드를 작성해 보세요.
-- 2-1. 리스트 통합(list comprehension )으로 만들어 보세요
-- 2-2. filter 와 람다 표현식으로 만들어 보세요
-- 2-3. filter 와 함수 합성(function composition)으로 만들어 보세요.
input = [("Kim", 60), ("Park",80), ("Choi", 70), ("Lee", 90), ("Jung", 85)]

ans21 = [(x, y) | (x, y) <- input, y > 80]
ans22 = filter (\(x, y) -> y > 80) input
ans23 = filter ((>80) . snd) input

