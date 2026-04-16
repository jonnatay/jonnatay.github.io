"""
Run with:
manim -pql  --resolution 1920,1080 manimTest.py -o BFS -- --mainScene ./examples/BFS.py 
"""
import random
seed = random.random()
print("seed = ", seed)
random.seed(seed)

manimScene.setAnimationsQuing(True)
nodes = [Node(i) for i in range(10)]
for source in nodes:
    for destination in nodes:
        if destination != source:
            if random.random() < 0.2:
                source.append(destination)

manimScene.setAnimationsQuing(False)
q = ManimList([nodes[0]])
sean = {str(nodes[0]): None}
while len(q) > 0:
    top = q[0]
    manimScene.onScreenPrint(f"searching node {top.getData()}")
    for i in range(len(top)):
        conection = top[i]
        if str(conection) not in sean:
            sean[str(conection)] = top
            q.append(conection)
    q.pop(0)

