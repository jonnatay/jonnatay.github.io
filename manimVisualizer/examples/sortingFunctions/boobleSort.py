"""
Run with:
manim -pql  --resolution 1920,1080 manimTest.py -o boobleSort -- --mainScene ./examples/sortingFunctions/boobleSort.py
"""
import random
seed = random.random()
print("seed = ", seed)
random.seed(seed)

manimScene.setAnimationsQuing(True)
x = ManimList([])
for i in range(6):
    x.append(int(random.random()*100))
manimScene.setAnimationsQuing(False)
le = len(x)

for s in range(0,le):
    last = x[0]
    noSwop = True
    for i in range(0, le-1):
        num = x[i+1]
        if last > num:
            noSwop = False
            manimScene.swop([x, i], [x, i+1])
        else:
            last = num
    if noSwop:
        break


