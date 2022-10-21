import Data.Maybe
import Util

type Intersection = Maybe Pos

type Line = (Pos, Pos)

type Move = (Int, Int)

type Pos = (Int, Int)

add :: Pos -> Pos -> Pos
add a b = (fst a + fst b, snd a + snd b)

parse :: String -> ([Move], [Move])
parse input = do
  let ln = lines input
  let a = head ln
  let b = last ln
  (parseLine a, parseLine b)

parseLine :: String -> [Move]
parseLine input = do
  let splits = split input ','
  map parseMove splits

parseMove :: String -> Move
parseMove input
  | head input == 'D' = (0, read (tail input))
  | head input == 'U' = (0, negate (read (tail input)))
  | head input == 'R' = (read (tail input), 0)
  | head input == 'L' = (negate (read (tail input)), 0)

movesLines :: Pos -> [Move] -> [Line]
movesLines _ [] = []
movesLines pos [last] = [(pos, pos `add` last)]
movesLines pos (next : more) = (pos, pos `add` next) : movesLines (pos `add` next) more

between :: Int -> Int -> Int -> Bool
between a b x
  | a < x && x < b = True
  | a > x && x > b = True
  | otherwise = False

intersects :: (Line, Line) -> Intersection
intersects (a, b)
  -- If both lines are horizontal (or both are vertical) then we can assume
  -- that they don't intersect.
  | ah == bh = Nothing
  | ah && between b1y b2y a1y && between a1x a2x b1x = Just (b1x, a1y)
  | bh && between a1y a2y b1y && between b1x b2x a1x = Just (a1x, b1y)
  | otherwise = Nothing
  where
    a1x = fst (fst a)
    a1y = snd (fst a)
    b1x = fst (fst b)
    b1y = snd (fst b)
    a2x = fst (snd a)
    a2y = snd (snd a)
    b2x = fst (snd b)
    b2y = snd (snd b)
    ah = a1x /= a2x
    bh = b1x /= b2x

intersections :: [Line] -> [Line] -> [Pos]
intersections a b = do
  let pairs = [(x, y) | x <- a, y <- b]
  mapMaybe intersects pairs

manhattan :: Pos -> Int
manhattan (x, y) = abs x + abs y

contains :: Pos -> Line -> Bool
contains pos line
  | horiz && snd pos == snd (fst line) && between (fst (fst line)) (fst (snd line)) (fst pos) = True
  | not horiz && fst pos == fst (fst line) && between (snd (fst line)) (snd (snd line)) (snd pos) = True
  | otherwise = False
  where
    horiz = fst (fst line) /= fst (snd line)

distance :: [Line] -> Pos -> Int
distance [] _ = error "no collision found"
distance (l : ls) pos
  | contains pos l = inlineDistance l pos
  | otherwise = lineLength l + distance ls pos
  where
    inlineDistance ((x1, y1), _) (x2, y2) = abs (x1 - x2) + abs (y1 - y2)
    lineLength ((x1, y1), (x2, y2)) = abs (x1 - x2) + abs (y1 - y2)

totalDistance :: [Line] -> [Line] -> Pos -> Int
totalDistance a b pos = distance a pos + distance b pos

main = do
  rawInput <- readFile "inputs/3"
  let input = parse rawInput
  let alines = movesLines (0, 0) (fst input)
  let blines = movesLines (0, 0) (snd input)
  print (part1 alines blines)
  print (part2 alines blines)

part1 a b = minimum (map manhattan (intersections a b))

part2 a b = minimum (map (totalDistance a b) (intersections a b))
