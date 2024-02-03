# mapless-practice
`mapless-practice` is a small utility to generate seeds for practicing
mapless Buried Treasure, which is a strategy for Minecraft speedruns.
It makes use of the wonderful [cubiomes](http://github.com/cubitect/cubiomes)
library to do so.

This only checks for a buried treasure within a few chunks of the world
spawn. It does no filtering to ensure that there are no other nearby
structures which may show up as false positives on the pie chart.

If you need a lot of mapless practice seeds, this is far faster than
running the JustLearnTreasure filter on repl.it.

# Cubiomes

Build with commit [95723f9](https://github.com/Cubitect/cubiomes/tree/95723f90bbac8ebc258ab83c5ee77eb9776e4b9f).
Clone it to a directory called cubiomes in this directory.
