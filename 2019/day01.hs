convInt :: String -> Int
convInt x = read x :: Int

calculate :: Int -> Int
calculate x = div x 3 - 2

recurse :: Int -> Int
recurse x =
  if x > 0
    then x + recurse (calculate x)
    else 0

main = do
  input <- readFile "inputs/1"
  let ln = map convInt (lines input)
  part1 ln
  part2 ln

part1 input =
  print (sum (map calculate input))

part2 input =
  print (sum (map (recurse . calculate) input))
