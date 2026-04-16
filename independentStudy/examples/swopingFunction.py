"""
Run with:
manim -pql  --resolution 1920,1080 manimTest.py -o swopingFunction -- --mainScene ./examples/swopingFunction.py
"""

a = ManimList([Node(3), Node(1), Node(2)])
manimScene.swop(a[2], a[0]) # swap the values of the nodes in the array
manimScene.onScreenPrint("a[0] = ", a[0])
manimScene.swop([a,0], [a,2]) # swap the values in the actual array
manimScene.onScreenPrint("a[0] = ", a[0])
manimScene.swop([a,1], a[2])
manimScene.onScreenPrint("a[1] = ", a[1])
manimScene.set([a,1], [a,2])
manimScene.onScreenPrint("a[1] = ", a[1])
manimScene.set(a[1], a[0])
manimScene.onScreenPrint("a[1] = ", a[1])
manimScene.set(a[1], [a,1])
manimScene.onScreenPrint("a[1] = ", a[1])

