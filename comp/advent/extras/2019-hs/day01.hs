calculate :: Int -> Int
calculate x = div x 3 - 2

recurse :: Int -> Int
recurse x =
  if x > 0
    then x + recurse (calculate x)
    else 0

main = do
  input <- readFile "inputs/1"
  let ln = map read (lines input)
  print (part1 ln)
  print (part2 ln)

part1 input = sum (map calculate input)

part2 input = sum (map (recurse . calculate) input)
