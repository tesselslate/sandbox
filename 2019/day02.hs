import Util

add :: (Int, [Int]) -> [Int]
add (index, list) = listSet (list !! (index + 3), (list !! (list !! (index + 1))) + (list !! (list !! (index + 2)))) list

mul :: (Int, [Int]) -> [Int]
mul (index, list) = listSet (list !! (index + 3), (list !! (list !! (index + 1))) * (list !! (list !! (index + 2)))) list

run :: Int -> [Int] -> [Int]
run index list
  | (list !! index) == 1 = run (index + 4) (add (index, list))
  | (list !! index) == 2 = run (index + 4) (mul (index, list))
  | (list !! index) == 99 = list
  | otherwise = [-1] -- should never happen

try :: (Int, Int) -> [Int] -> Int
try (noun, verb) list = head (run 0 (listSet (1, noun) (listSet (2, verb) list)))

main = do
  input <- readFile "inputs/2"
  let opcodes = listSet (1, 12) (listSet (2, 2) (map read (split input ',')))
  print (part1 opcodes)
  print (part2 opcodes)

part1 opcodes = head (run 0 (listSet (1, 12) (listSet (2, 2) opcodes)))

desired = 19690720

part2 opcodes = do
  let pair = head [(n, v) | n <- [0 .. 99], v <- [0 .. 99], try (n, v) opcodes == desired]
  100 * fst pair + snd pair
