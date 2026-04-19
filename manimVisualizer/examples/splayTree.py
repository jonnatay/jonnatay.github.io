"""
Run with:
manim -pql  --resolution 1920,1080 manimTest.py -o splayTree -- --mainScene ./examples/splayTree.py
"""


class splayTree:
    def __init__(self):
        self.root = Node("*")
    def splay(self, node, path):
        if len(path) == 0:
            self.root = node
            return
        par = path.pop()
        left = par[0] == node
        if len(path) == 0:
            if left:
                #manimScene.setAnimationsQuing(True)
                par[0] = node[1]#set
                node[1] = par
                #manimScene.setAnimationsQuing(False)
            else:
                #manimScene.setAnimationsQuing(True)
                par[1] = node[0]#set
                node[0] = par
                #manimScene.setAnimationsQuing(False)
            self.root = node
        else:
            par2 = path.pop()
            left2 = par2[0] == par
            if left and left2:
                #manimScene.setAnimationsQuing(True)
                par2[0] = par[1]#set
                par[1] = par2
                par[0] = node[1]
                node[1] = par
                #manimScene.setAnimationsQuing(False)
            if not(left) and not(left2):
                #manimScene.setAnimationsQuing(True)
                par2[1] = par[0]#set
                par[0] = par2
                par[1] = node[0]
                node[0] = par
                #manimScene.setAnimationsQuing(False)
            if not(left) and left2:
                #manimScene.setAnimationsQuing(True)
                par2[0] = node[1]#set
                par[1] = node[0]
                node[0] = par
                node[1] = par2
                #manimScene.setAnimationsQuing(False)
            if left and not(left2):
                #manimScene.setAnimationsQuing(True)
                par2[1] = node[0]#set
                par[0] = node[1]
                node[1] = par
                node[0] = par2
                #manimScene.setAnimationsQuing(False)
            if len(path) != 0:
                left3 = path[-1][0] == par2
                if left3:
                    path[-1][0] = node
                else:
                    path[-1][1] = node
            self.splay(node, path)
    def insert(self, value):
        self.insertHelper(value, self.root, [])
    def insertHelper(self, value, pos, path):
        if pos.getData() == "*":
            pos.setData(value)
            pos.append(Node("*"))
            pos.append(Node("*"))
            self.splay(pos, path)
        elif pos < value:
            path.append(pos)
            self.insertHelper(value, pos[1], path)
        elif pos > value:
            path.append(pos)
            self.insertHelper(value, pos[0], path)
    def deleat(self, value):
        self.deleatHelper(value, self.root, [])
    def deleatHelper(self, value, pos, path):
        if pos.getData() == value:
            rep = pos
            if pos[0].getData() != "*":
                path.append(pos)
                #print("left")
                rep = self.kthMostChild(1, pos[0], path)
            elif pos[1].getData() != "*":
                path.append(pos)
                #print("right")
                rep = self.kthMostChild(0, pos[1], path)
            #print("pos = ", pos, "rep = ", rep)
            if pos != rep:
                #print("swoping")
                manimScene.swop(rep, pos)
                #path.append(pos)
                self.deleatHelper(value, rep, path)
            else:
                pos.pop().deleat()
                pos.pop().deleat()
                
                pos.setData("*")
                if len(path) > 0:
                    self.splay(path.pop(), path)
                
        elif pos < value:
            path.append(pos)
            self.deleatHelper(value, pos[1], path)
        elif pos > value:
            path.append(pos)
            self.deleatHelper(value, pos[0], path)
    def kthMostChild(self, k, pos, path):
        if pos[k] != "*":
            path.append(pos)
            return self.kthMostChild(k, pos[k], path)
        return pos



spTree = splayTree()
manimScene.onScreenPrint(f"inserting 5")
spTree.insert(5)
manimScene.onScreenPrint(f"inserting 3")
spTree.insert(3)
manimScene.onScreenPrint(f"inserting 2")
spTree.insert(2)
manimScene.onScreenPrint(f"inserting 7")
spTree.insert(7)
manimScene.onScreenPrint(f"inserting 4")
spTree.insert(4)
manimScene.onScreenPrint(f"inserting 8")
spTree.insert(8)
manimScene.onScreenPrint(f"inserting 6")
spTree.insert(6)
manimScene.onScreenPrint(f"inserting 1")
spTree.insert(1)
manimScene.onScreenPrint(f"inserting 3")
spTree.insert(3)
manimScene.onScreenPrint(f"inserting 9")
spTree.insert(9)
manimScene.onScreenPrint(f"deleating 1")
spTree.deleat(1)
manimScene.onScreenPrint(f"deleating 2")
spTree.deleat(2)
manimScene.onScreenPrint(f"deleating 3")
spTree.deleat(3)
manimScene.onScreenPrint(f"deleating 4")
spTree.deleat(4)
manimScene.onScreenPrint(f"deleating 5")
spTree.deleat(5)
manimScene.onScreenPrint(f"deleating 6")
spTree.deleat(6)
manimScene.onScreenPrint(f"deleating 7")
spTree.deleat(7)
manimScene.onScreenPrint(f"deleating 8")
spTree.deleat(8)
manimScene.onScreenPrint(f"deleating 9")
spTree.deleat(9)

