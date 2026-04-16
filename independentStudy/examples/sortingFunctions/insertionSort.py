"""
Run with:
manim -pql  --resolution 1920,1080 manimTest.py -o insertionSort -- --mainScene ./examples/sortingFunctions/insertionSort.py
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

for s in range(1,le):
    n = x[s]
    manimScene.onScreenPrint(f"inserting {n}")
    for i in range(s-1, -1, -1):
        if n < x[i]:
            manimScene.swop([x, i+1], [x, i])
        else:
            break


