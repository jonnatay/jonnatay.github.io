"""
Run with:
manim -pql  --resolution 1920,1080 manimTest.py -o radixSort -- --mainScene ./examples/sortingFunctions/radixSort.py
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

manimScene.setAnimationsQuing(True)
redx = [ManimList([f"s{i}"]) for i in range(10)]
manimScene.setAnimationsQuing(False)

for p in range(2):
    manimScene.onScreenPrint(f"p = {10**p}")
    for i in range(le-1, -1, -1):
        num = x[i]
        n=(num//(10**p))%10
        manimScene.setAnimationsQuing(True)
        redx[n].append("*")
        manimScene.swop([x, i], [redx[n], -1])
        manimScene.setAnimationsQuing(False)
    s = 0
    for r in redx:
        while len(r) > 1:
            manimScene.setAnimationsQuing(True)
            manimScene.swop([x, s], [r, -1])
            s += 1
            r.pop()
            manimScene.setAnimationsQuing(False)
            
