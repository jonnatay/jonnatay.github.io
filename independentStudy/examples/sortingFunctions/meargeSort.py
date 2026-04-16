"""
Run with:
manim -pql  --resolution 1920,1080 manimTest.py -o meargeSort -- --mainScene ./examples/sortingFunctions/meargeSort.py
"""
import random
seed = random.random()
print("seed = ", seed)
random.seed(seed)

manimScene.setAnimationsQuing(True)
x = ManimList([])
for i in range(10):
    x.append(int(random.random()*100))
manimScene.setAnimationsQuing(False)
le = len(x)

temp1 = ManimList(["*"]*(le//2+1))
temp2 = ManimList(["*"]*(le//2+1))


def coppySection(s, e, lis):
    global x
    for j, i in enumerate(range(s,e)):
        manimScene.swop([lis, j], [x, i])
def meargeSort(s, e):
    global x
    global temp1
    global temp2
    global le
    global meargeSort
    global coppySection
    if e-s <= 1:
        return
    manimScene.onScreenPrint(f"mearging the {s} to {e}")
    midle = (e+s)//2
    meargeSort(s, midle)
    meargeSort(midle, e)
    coppySection(s, midle, temp1)
    l1 = midle-s
    coppySection(midle, e, temp2)
    l2 = e-midle
    a = 0
    b = 0
    an = temp1[a]
    bn = temp2[a]
    pl = s
    while True:
        if an <= bn:
            manimScene.swop([x, pl], [temp1, a])
            pl += 1
            a += 1
            if a < l1:
                an = temp1[a]
            else:
                break
        else:
            manimScene.swop([x, pl], [temp2, b])
            pl += 1
            b += 1
            if b < l2:
                bn = temp2[b]
            else:
                break
    for i in range(a, l1):
        manimScene.swop([x, pl], [temp1, i])
        pl += 1
    for i in range(b, l2):
        manimScene.swop([x, pl], [temp2, i])
        pl += 1
    
meargeSort(0, le)


