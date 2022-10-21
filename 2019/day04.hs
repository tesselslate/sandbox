import Util

parse :: String -> [Int]
parse input = do
  let splits = split input '-'
  [read (head splits) .. read (last splits)]

neverDecreases :: [Int] -> Bool
neverDecreases [a, b] = a <= b
neverDecreases (a : b) = a <= head b && neverDecreases b

hasAdjacent :: [Int] -> Bool
hasAdjacent [a, b] = a == b
hasAdjacent (a : b : c) = a == b || hasAdjacent (b : c)

-- This solution is pretty lame but I gave up on using a recursive function
-- for this.
twoAdjacent :: [Int] -> Bool
twoAdjacent [a, b, c, d, e, f] =
  (a == b && b /= c)
    || (a /= b && b == c && c /= d)
    || (b /= c && c == d && d /= e)
    || (c /= d && d == e && e /= f)
    || (d /= e && e == f)

valid :: [Int] -> Bool
valid pw = hasAdjacent pw && neverDecreases pw

valid2 :: [Int] -> Bool
valid2 pw = twoAdjacent pw && neverDecreases pw

main = do
  rawInput <- readFile "inputs/4"
  let input = parse rawInput
  print (part1 input)
  print (part2 input)

part1 range = length (filter valid (map digits range))

part2 range = length (filter valid2 (map digits range))
