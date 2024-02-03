import sys

cmds = [
        "setblock ~ ~1 ~ command_block{auto:1,Command:\\\\\'fill ~ ~ ~ ~ ~-3 ~ air\\\\\'}"
]
cmds += [l.strip() for l in open(sys.argv[1])]
cmds += ["kill @e[type=command_block_minecart,distance=..1]"]
passengers = ",".join([f"{{id:command_block_minecart,Command:\'{cmd}\'}}" for cmd in cmds])

ttext = "Setup"
tcolor = "gold"

cmd = "summon falling_block ~ ~1 ~ {Time:1,BlockState:{Name:redstone_block},Passengers:[{id:falling_block,Passengers:[{id:falling_block,Time:1,BlockState:{Name:activator_rail},Passengers:[" + passengers + "]}]}]}"
print("give @p command_block{display:{Name:'[{\"text\":\"" + ttext + "\",\"color\":\"" + tcolor + "\",\"italic\":\"false\"}]'},BlockEntityTag:{Command:\"" + cmd + "\",auto:1b}}")
