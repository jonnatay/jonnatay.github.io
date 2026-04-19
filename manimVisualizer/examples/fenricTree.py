"""
Run with:
manim -pql  --resolution 1920,1080 manimTest.py -o fenricTree -- --mainScene ./examples/fenricTree.py
"""
import random
seed = random.random()
print("seed = ", seed)
random.seed(seed)

class fenricTree:
    def __init__(self, n):
        self.lis = ManimList([0]*(n+1))
        self.f = (2**len(bin(n)))-1
    def lastOne(self, x):
        return ((x^self.f)+1)&x
    def inc(self, pos, delta):
        i = pos+1
        while i < len(self.lis):
            self.lis[i] += delta
            i += self.lastOne(i)
    def prefexSum(self, pos):
        ans = 0
        i = pos+1
        while i > 0:
            ans += self.lis[i]
            manimScene.onScreenPrint(f"result = {ans}")
            i -= self.lastOne(i)
        return ans

length = 8
fentree = fenricTree(length)
for i in range(10):
    p = int(random.random()*length)
    if (int(random.random()*2)):
        v = int(random.random()*20)-10
        manimScene.onScreenPrint(f"incrimenting position {p} by {v}")
        fentree.inc(p, v)
    else:
        manimScene.onScreenPrint(f"prefex summing position {p}")
        fentree.prefexSum(p)
