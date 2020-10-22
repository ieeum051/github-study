import Data.Char
import Data.Time.Calendar
import Data.Time.Calendar.WeekDate

border = "-----------------------------------------------------"
day_week = "Mon\tTue\tWed\tThr\tFri\tSat\tSun"
top_frame = border ++ "\n" ++ day_week ++ "\n" ++ border

mkCalData :: Int -> Int -> Int -> [Int]
mkCalData a b c
 | a == 7 = mkCalData 0 b c
 | a > 0 = 0 : mkCalData (a-1) b c
 | c >= b  = b : mkCalData a (b+1) c
 | otherwise = []

mkCalStr :: Int -> [Int] -> String
mkCalStr _ [] = ""
mkCalStr a (x:xs)
 | a == 0 = "\n" ++ mkCalStr 7 (x:xs)
 | x == 0 = "\t" ++ mkCalStr (a-1) xs
 | otherwise = (show x) ++ "\t" ++ mkCalStr (a-1) xs

genCalendar :: Integer -> Int -> String
genCalendar year month = top_frame ++ "\n" ++ (mkCalStr 7 $ mkCalData start_at 1 day_cnt)
    where day_cnt = gregorianMonthLength year month
          start_at = digitToInt $ last $ showWeekDate $ fromGregorian year month 01

main = do
    putStrLn("Plz type year (ex> 2020) : ")
    year <- getLine
    putStrLn("Plz type month (ex> 1, 2, 3) : ")
    month <- getLine
    putStrLn ("Calendar In " ++ year ++ "/" ++ month)
    putStrLn (genCalendar (read year::Integer) (read month::Int) )