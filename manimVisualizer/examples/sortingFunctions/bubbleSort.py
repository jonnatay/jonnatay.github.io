"""
Run with:
manim -pql  --resolution 1920,1080 manimTest.py -o boobleSort -- --mainScene ./examples/sortingFunctions/boobleSort.py
"""
import random
seed = random.random()
print("seed = ", seed)
random.seed(seed)

manimScene.setAnimationsQueuing(True)
x = ManimList([])
for i in range(6):
    x.append(int(random.random()*100))
manimScene.setAnimationsQueuing(False)
le = len(x)

for s in range(0,le):
    last = x[0]
    noSwap = True
    for i in range(0, le-1):
        num = x[i+1]
        if last > num:
            noSwap = False
            manimScene.swap([x, i], [x, i+1])
        else:
            last = num
    if noSwap:
        break


