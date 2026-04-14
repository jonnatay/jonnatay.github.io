"""
Run with:
manim -pql  --resolution 1920,1080 manimTest.py -o videoName -- --mainScene manimTestUserSide.py
"""
import random
seed = random.random()
print("seed = ", seed)
random.seed(seed)

import time

x = Node(1)
x = Node(2)
print("x = ", x.getData())
x.deleat()
def crash(y):
    y<9
#crash(x)
