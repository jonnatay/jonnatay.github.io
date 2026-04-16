"""
Run with:
manim -pql  --resolution 1920,1080 manimTest.py -o heapSort -- --mainScene ./examples/sortingFunctions/heapSort.py
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

def shiftDown(pos):
    global shiftDown
    global x
    global le
    if pos*2+1 >= le:
        return
    child = pos*2+1
    selfNum = x[pos]
    childNum=x[child]
    if pos*2+2 < le:
        childPlusNum = x[child+1]
        if childNum < childPlusNum:
            child += 1
            childNum = childPlusNum
    if childNum > selfNum:
        #x[pos], x[child] = childNum, selfNum
        manimScene.swop([x, pos], [x, child])
        shiftDown(child)

manimScene.onScreenPrint("heapafying")
for i in range(le//2,-1,-1):
    manimScene.onScreenPrint(f"heapafying {x[i]}")
    shiftDown(i)
print(x)
while le > 0:
    le -= 1
    #xz = x[0]
    #manimScene.onScreenPrint(f"dequing {xz}")
    xl = x[le]
    #x[0], x[le] = xl, xz
    manimScene.swop([x, 0], [x, le])
    manimScene.onScreenPrint(f"downShifting {xl}")
    shiftDown(0)
print(x)


