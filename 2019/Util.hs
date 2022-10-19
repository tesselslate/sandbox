module Util (listSet, split) where

listSet :: Int -> Int -> [Int] -> [Int]
listSet index value list = take index list ++ [value] ++ drop (index + 1) list

split :: String -> Char -> [String]
split str delim = realSplit delim str ""

-- Internal
realSplit :: Char -> String -> String -> [String]
realSplit _ "" "" = [""]
realSplit _ "" current = [current]
realSplit delim (c : str) current
  | c == delim = current : realSplit delim str ""
  | otherwise = realSplit delim str (current ++ [c])
