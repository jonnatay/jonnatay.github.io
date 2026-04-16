"""
Run with:
manim -pql  --resolution 1920,1080 manimTest.py -o quickSort -- --mainScene ./examples/sortingFunctions/quickSort.py
"""
import random
seed = random.random()
print("seed =", seed)
random.seed(seed)

manimScene.setAnimationsQuing(True)
x = ManimList([])
for i in range(6):
    x.append(int(random.random()*100))
manimScene.setAnimationsQuing(False)
le = len(x)

def quickSort(s, e):
    global x
    global le
    global quickSort
    if e-s <= 1:
        return
    pivit = x[e-1]
    manimScene.onScreenPrint(f"sorting the {s} to {e} pivit = {pivit}")
    a = s
    b = e-2
    while a <= b:
        while x[a] < pivit:
            a += 1
        while a <= b and x[b] > pivit:
            b -= 1
        if a < b:
            manimScene.swop([x, a], [x, b])
            a += 1
            b -= 1
    manimScene.swop([x, e-1], [x, a])
    quickSort(s, a)
    quickSort(a+1, e)
    
quickSort(0, le)


