import random
block_list = {
    "orangeRicky": [
        ["..x", "xxx"],
        ["x..", "x..", "xx."],
        ["xxx", "x.."],
        [".xx", "..x", "..x"]]}


print(block_list["orangeRicky"][2])

rotation = random.randint(0, len(block_list["orangeRicky"]) - 1)
print(rotation)
