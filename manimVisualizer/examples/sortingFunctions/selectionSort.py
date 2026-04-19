"""
Run with:
manim -pql  --resolution 1920,1080 manimTest.py -o selectionSort -- --mainScene ./examples/sortingFunctions/selectionSort.py
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
    manimScene.onScreenPrint(f"finding the {s+1}th smallest")
    mn = 9999999999
    mnLoc = -1
    for i in range(s, le):
        num = x[i]
        if num < mn:
            mn = num
            mnLoc = i
            manimScene.onScreenPrint(f"curent min = {mn}")
    manimScene.swop([x, s], [x, mnLoc])


