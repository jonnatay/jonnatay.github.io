import manim as mn
from manim import *
import numpy as np
from scipy.sparse.linalg import eigsh
from scipy.sparse import csr_matrix
from sortedcontainers import SortedList
import sys
import _collections_abc
import argparse
import traceback
import re

if "--" in sys.argv:
    user_args = sys.argv[sys.argv.index("--") + 1:]
else:
    user_args = []
parser = argparse.ArgumentParser()
parser.add_argument("--mainScene", default="")
parser.add_argument("--script", default="")
args = parser.parse_args(user_args)

#manim -pql --resolution 1920,1080 manimTest.py HelloWorld

#fix odd arrow sizes
#test deleating nodes with pointers to nodes then moving the nodes
#ue multiple pointers from the same node to the same node
#fix adding arrays while nodes exist???
#test pointers to arrays (specificaly moving them)
#fix empty inishalizations???
speed = 0.5
waittime = 0.1
def Main():
    global speed
    global waittime
    if args.mainScene != "" or args.script != "":
        stuffToDo = ""#args.script
        if stuffToDo == "":
            stuffToDo=open(args.mainScene).read()
        start = """global speed
global waittime
"""
        try:
            exec(start+stuffToDo)
        except Exception as e:
            err = traceback.format_exc().split("\n")
            message = [""]
            lins = stuffToDo.split("\n")
            
            for c, i in enumerate(err):
                if re.fullmatch(r"""  File "<string>", line \d+, in .*""", i):
                    lineNumber = int(re.findall(r"""  File "<string>", line (\d+), in .*""", i)[0])-2
                    function = re.findall(r"""  File "<string>", line \d+, in (.*)""", i)[0]
                    message.append(f"{function} line {lineNumber}")
                    for i in range(max(0,lineNumber-3), min(len(lins), lineNumber+4)):
                        pointer = "  "
                        if i == lineNumber-1:
                            pointer = "> "
                        message.append(pointer + "0"*(len(str(min(len(lins), lineNumber+4)))-len(str(i+1))) + str(i+1) + "|" + lins[i])
                    message.append("")
                #if len(message)<1000:
                #    print("short message err was ", err)
            raise Exception("there was an error i think it was somewair here:\n"+"\n".join(message)+"\nthe Error was:\n"+str(e))
            #lineNumber = e.lineNumber
            #raise Exception(f"i think the line the error was on is:\n{(start+stuffToDo)[lineNumber]}")
        """
        try:
            exec(stuffToDo)
               
        except SyntaxError as e:
            print("Syntax error:", e)
        except Exception:
            traceback.print_exc()
            print("\n--- Executed code ---")
            for i, line in enumerate(stuffToDo.splitlines(), 1):
                print(f"{i:3}: {line}")
        """
    
    


    #import heapq
##    g = [Node(i) for i in range(3)]
##    #g[0].append(g[1])
##    #g[1].append(g[0])
##    g[0].append(g[2])
##    g[2].append(g[0])
##    Node(3)
    
    #g[1].append(g[2])
    #g[2].append(g[1])
    #[ManimList([i]) for i in range(5)]
##    manimScene.setAnimationsQuing(True)
##    [ManimList([i]) for i in range(50)]
##    manimScene.setAnimationsQuing(True)
##    ManimList([0])
##    ManimList([1])
##    ManimList([2])
##    manimScene.setAnimationsQuing(False)
##    ManimList([3])
##    ManimList([4])
##    ManimList([5])

##    
##    import random
##    #manimScene.setAnimationsQuing(True)
##    g = [Node(i) for i in range(5)]
##    for i in g:
##        for j in g:
##            if j != i:
##                if random.random() < 0.5:
##                    i.append(j)
##    #manimScene.setAnimationsQuing(False)
##    q = ManimList([g[0]])
##    sean = {str(g[0]): None}
##    while len(q) > 0:
##        t = q[0]
##        manimScene.onScreenPrint(f"searching node {t.getData()}")
##        for n in range(len(t)):
##            i = t[n]
##            if str(i) not in sean:
##                sean[str(i)] = t
##                q.append(i)
##        q.pop(0)

    
##    #[ManimList([i]) for i in range(5)]

    

##    a = Node(0)
##    b = Node(1)
##    a.append(b)
##    a[0]
##    c = Node(2)
##    b.append(c)
##    b[0]
##    a.setData(b)
##    ManimList([2])
##    a.setData(3)
##    ManimList([4])
    
    #ManimList([1])
    #ManimList([Node(0), Node(1), Node(2), Node(3), Node(4)])
    #Node(Node(0))
    #ManimList([1])
    #dd = ManimList([Node(ManimList([Node(Node(0))]))])
##    dd = ManimList([1])
##    d = ManimList([2])
##    dd.append(d)
##    d = ManimList([3])
##    dd.append(d)
##    dd.append(3.5)
##    d = ManimList([4])
##    dd.append(d)
##    dd.pop(0)
##    Node(0)
##    ManimList([5])
##    ManimList([6])
    
##    p = Node(0)
##    for i in range(1, 10):
##        t = Node(i)
##        p.append(t)
##        p = t
    
        
##    root = Node(0)
##    root.append("null")
##    root.append("null")
##    for i in range(1,5):
##        manimScene.onScreenPrint("adding")
##        new = root.rightMost()
##        new.setData(i)
##        new.append("null")
##        new.append("null")
##        manimScene.onScreenPrint("swopping")
##        right = root
##        while len(right) > 0:
##            temp = right[-1]
##            right.reverse()
##            right = temp

    

##    node = Node(0)
##    node2 = Node(1)
##    node3 = Node(2)
##    node4 = Node(3)
##    node5 = Node(4)
##    node.append(node5)
##    node.append(node2)
##    node5 = Node(5)
##    node2.append(node4)
##    node3.append(node4)
##    node3[0] = node
####    node3.insert(0, node)
####    del node3[1]
####    node3.insert(0, Node(6))
    
##    quietData = ["a"]*6+["b", "c", "d", "e", "f", "g"]
##    data = ManimList(quietData)
##   
##    ogtop = 0
##    q = ManimList([[1, ogtop]])
##    keyNextTop = lambda x: x
##    inq = ManimList([-1]*len(data))
##    inq[keyNextTop(ogtop)] = 1
##    while len(q) > 0:
##        #print(q)
##        top = heapq.heappop(q)
##        if top[0] == inq[keyNextTop(top[1])]:
##            d = top[0]+1
##            nxtTop = top[1]+1
##            key = keyNextTop(nxtTop)
##            if inq[key] == -1 or inq[key] > d:
##                inq[key] = d
##                heapq.heappush(q, [inq[key], nxtTop])
##            
##            for i in range(top[1]+1, len(data)):
##                for j in range(0, top[1]):
##                    for k in range(j, j+(i-top[1])):
##                        if data[k] = data[i]
                    
    
##    data = ManimList([12, 11, 13, 5, 6])
##    for i in range(len(data)-1, -1, -1):
##        iv = data[i]
##        for j in range(len(data)-1, i, -1):
##            jv = data[j]
##            if jv < iv:
##                data.pop(i)
##                data.insert(j, iv)
##                break
##
##    print("sorted = ", data)
    
    #a = ManimList([1,4,2, "a", "b"])
    #a *= 3
    #del a[2:4]
    #del a[3]
    #a.reverse()
    #a.sort()
    #a += [1,"b",3]
    #print("mapping = ", a.mapping)
    #a.remove("a")
    
    
    #a.insert(2,"c")
    #a.insert(-1,"d")
    #a.insert(9,"e")
    #a.clear()
    #a.append(1)
    #a.insert(0, 0)
    #a.insert(2, 2)
    
    #a.append("c")
    #a.pop()
    #a.pop(3)
    #a.pop(-2)
    
    #a[3]
    #a[4:]
    #a[:3]
    #a[::-1]
    #a[1:-1:2]
    #a[2] = 3
    #a[1] = 5
manimScene = None
class manimTest(MovingCameraScene):
    def construct(self):
        global manimScene
        manimScene = self
        self.quedAnimations = []
        self.takenRows = {}
        self.camWith = 18
        self.camPos = [5, -3, 0]
        self.camera.frame.move_to(self.camPos)
        self.camera.frame.set(width=self.camWith)
        self.registeredNodes = []
        self.fakeDependencyNumber = -1
        self.globalText = None
        self.isDag = True
        self.queanimations = False
        Main()
        if self.queanimations:
            self.setAnimationsQuing(False)
        self.pause(waittime)
        self.pause(speed)
    def fixCam(self, bounds):
        #print(bounds, self.camPos, self.camWith)
        if bounds[0] > self.camPos[0]*2 or bounds[1] < self.camPos[1]*2:
            self.camPos = [max(bounds[0]/2, self.camPos[0]), min(bounds[1]/2, self.camPos[1]), 0]
            self.camWith = max(max(self.camPos[0], -self.camPos[1]*2)*2+4, self.camWith)
            self.camera.frame.set(width=self.camWith)
            self.camera.frame.move_to(self.camPos)
            print("moving cam to ", self.camPos)
            if self.globalText != None:
                self.quietMoveText(self.globalText, [self.camPos[0],1.1,0])
    def getNextOpenYpos(self):
        ypos = 0
        while ypos in self.takenRows:
            ypos -= 1.1
        return ypos
    def constructArray(self, array, xpos, ypos):
        self.takenRows[ypos] = True
        toPlay = []
        for i, v in enumerate(array):
            toPlay += self.getDrawSquair(xpos+i, ypos, txt=v)
        return toPlay
    #def drawSquair(self, xpos, ypos, txt=""):
    #    self.play(self.CreateMulti(self.getDrawSquair(xpos, ypos, txt)))
    def onScreenPrint(self, *txtt):
        txt = " ".join(list(map(str,list(txtt))))
        print(txt)
        if self.globalText == None:
            self.globalText = self.getTextToDraw(txt=txt)
            self.quietMoveText(self.globalText, [self.camPos[0], 1.1, 0])
            manimScene.playWithEnquedAnimations(self.CreateMulti([self.globalText]))
        else:
            newText = self.getTextToDraw(txt=txt)
            self.AlterText(self.globalText, newText, [self.camPos[0], 1.1, 0], flash=False)
            self.globalText = newText
        manimScene.pause(waittime)
    def getTextToDraw(self, txt=None, fontColor=WHITE, source=None):
        if txt == None:
            txt = ""
        elif isinstance(txt, ManimList):
            return Arrow(
                start=[0,0,0],   # rightmost point of left circle
                end=[-0.5, txt.ypos, 0],     # leftmost point of right circle
                color=fontColor,
                buff=0                         # small gap so arrow doesn’t overlap the circles
            )
        elif isinstance(txt, Node):
            end = txt.position.copy()
            end[1] += 0.5
            arrow = Arrow(
                start=[0,0,0],   # rightmost point of left circle
                end=end+[0],     # leftmost point of right circle
                color=fontColor,
                buff=0                         # small gap so arrow doesn’t overlap the circles
            )
            self.fakeDependencyNumber -= 1
            txt.textDependicyes[self.fakeDependencyNumber] = [arrow, source]

            return [arrow, txt, 1]
        else:
            txt = str(txt)
        return Text(txt, font_size=24, color=fontColor)
    def getDrawSquair(self, xpos, ypos, txt=None):
        #print("xpos = ", xpos, "ypos = ", ypos)
        square = Square(side_length=1, fill_color=BLUE, fill_opacity=0.3, color=GREEN)
        square.shift(RIGHT * xpos)
        square.shift(UP * ypos)
        text = self.getTextToDraw(txt)
        self.quietMoveText(text, [xpos,ypos,0])
        #text.shift(RIGHT * xpos)
        #text.shift(UP * ypos)
        self.fixCam([xpos, ypos])
        return [[square, text]]#[Create(square),Create(text)]#Write(text)]  
        #self.pause(waittime)
    def getDrawCircle(self, xpos, ypos, txt=None, source=None):
        #print("xpos = ", xpos, "ypos = ", ypos)
        circle = Circle(radius=0.5, fill_color=BLUE, fill_opacity=0.3, color=GREEN)
        circle.shift(RIGHT * xpos)
        circle.shift(UP * ypos)
        text = self.getTextToDraw(txt,source=source)
        self.quietMoveText(text, [xpos,ypos,0])
        #text.shift(RIGHT * xpos)
        #text.shift(UP * ypos)
        self.fixCam([xpos, ypos])
        return [circle, text]#[Create(square),Create(text)]#Write(text)]  
        #self.pause(waittime)
    def flaten(self, a, detatchArrows=False):
        ans = []
        #print("flatening ", a, detatchArrows)
        if type(a) != type([]):
            return [a]
        if type(a[-1]) == type(0):
            if not(detatchArrows):
                ans.append(a[0])
            else:
                for j in a[1].textDependicyes:
                    if a[1].textDependicyes[j][0] == a[0]:
                        del a[1].textDependicyes[j]
                        break
                ans.append(a[0])
            return ans
        for i in a:
            if type(i) == type([]):
                if False:#type(i[-1]) == type(0):
                    if not(detatchArrows):
                        ans.append(i[0])
                    else:
                        for j in i[1].textDependicyes:
                            if i[1].textDependicyes[j][0] == i[0]:
                                del i[1].textDependicyes[j]
                                break
                        ans.append(i[0])
                else:
                    ans += self.flaten(i)
            else:
                ans.append(i)
        #print("flatened", a, detatchArrows, "into", ans)
        return ans
    def AnimateMulti(self, toCreate, function, detatchArrows=False):
        temp = self.flaten(toCreate, detatchArrows)
        return [function(i) for i in temp]
    def CreateMulti(self, toCreate):
        temp = self.flaten(toCreate)
        return [Create(i) for i in temp]
    def UnCreateMulti(self, toCreate):
        temp = self.flaten(toCreate, detatchArrows=True)
        return [Uncreate(i) for i in temp]
    def enqAnimation(self, animation):
        self.quedAnimations.append(animation)
    def playWithEnquedAnimations(self, animation):
        if self.queanimations:
            self.enqAnimation(animation)
        else:
            self.quedAnimations += animation
            #print("playing", self.quedAnimations)
            if self.quedAnimations != []:
                self.play(*self.quedAnimations, run_time=speed)
            self.quedAnimations = []
    def pause(self, time):
        if not(self.queanimations):
            self.wait(time)
    def setAnimationsQuing(self, value):
        global speed
        if not(self.queanimations) and value:
            temp = speed
            speed = 0.0666667
            manimScene.playWithEnquedAnimations([])
            speed = temp
        elif not(value):
            self.queanimations = value
            manimScene.playWithEnquedAnimations([])
        self.queanimations = value
        #if True:#not(self.queanimations):
        #    self.playWithEnquedAnimations([])
    def TestRun(self):
        circle = Circle(radius=1, color=GREEN)   # sets the stroke (outline)
        circle.set_fill(GREEN, opacity=1)       # sets fill color and opacity
        circle.shift(LEFT * 3)
        #circle.move_to([2, -1, 0])  # (x=2, y=-1, z=0)
        #self.play(Create(circle))
        circle2 = Circle(radius=1, color=GREEN)   # sets the stroke (outline)
        circle2.set_fill(GREEN, opacity=1)       # sets fill color and opacity
        #self.play(Create(circle2))
        self.play(Create(circle), Create(circle2))
        arrow = Arrow(
            start=circle.get_right(),   # rightmost point of left circle
            end=circle2.get_left(),     # leftmost point of right circle
            color=GREEN,
            buff=0                         # small gap so arrow doesn’t overlap the circles
        )
        self.play(Create(arrow))
        self.pause(2)        
        text = Text("Hello, World!", font_size=72)
        self.play(Write(text))
        self.pause(2)
    def copyText(self, text):
        if isinstance(text, Text):
            return text.copy()
        elif isinstance(text, Arrow):
            return text.copy()
        elif isinstance(text, list):
            temp = [i for i in text]
            temp[0] = self.copyText(text[0])
            return temp[0]
    def findTextLocation(self, text):
        if isinstance(text, Text):
            return text.get_center()
        elif isinstance(text, Arrow):
            return text.get_start()
        elif isinstance(text, list):
            return self.findTextLocation(text[0])
    def moveText(self, text, location):
        if isinstance(text, Text):
            return AnimationGroup(text.animate.move_to(location))
        elif isinstance(text, Arrow):
            return AnimationGroup(text.animate.put_start_and_end_on(location, text.get_end()))
        elif isinstance(text, list):
            end = text[1].position.copy()
            end[1] += 0.5
            return AnimationGroup(text[0].animate.put_start_and_end_on(location, end+[0]))
    def quietMoveText(self, text, location):
        if isinstance(text, Text):
            text.move_to(location)
        elif isinstance(text, Arrow):
            text.put_start_and_end_on(location, text.get_end())
        elif isinstance(text, list):
            end = text[1].position.copy()
            end[1] += 0.5
            text[0].put_start_and_end_on(location, end+[0])
    def AlterText(self, text, newText, centor, flash=True):
        if isinstance(text, list):
            for j in text[1].textDependicyes:
                if text[1].textDependicyes[j][0] == text[0]:
                    #print("found it", j)
                    del text[1].textDependicyes[j]
                    break
            text=text[0]
        if isinstance(newText, list):
            newText=newText[0]
        #newText = manimScene.getTextToDraw(item, fontColor=RED, source=self)
        newPos = text.get_center()
        if isinstance(text, Arrow):
            newPos=text.get_start()
        manimScene.quietMoveText(newText, newPos)#newText.move_to(self.manimSelf[1])
        if flash:
            manimScene.playWithEnquedAnimations([Flash(centor, color=RED, line_length=0.5),
                        TransformMatchingShapes(text, newText)])
        else:
            manimScene.playWithEnquedAnimations([TransformMatchingShapes(text, newText)])
        #self.manimSelf[1] = newText
        manimScene.enqAnimation(AnimationGroup(newText.animate.set_color(WHITE)))
    def FlashText(self, text, centor, returnColor=WHITE):
        if isinstance(text, list):
            text=text[0]
        q=[Flash(centor, color=RED, line_length=0.5),
                AnimationGroup(text.animate.set_color(RED))]
        self.playWithEnquedAnimations(q)
        self.enqAnimation(AnimationGroup((text.animate.set_color(returnColor))))
    def FlashTextArray(self, selfdata, selfmapping):
        q = []
        for j in range(*i.indices(len(selfdata))):
            q.append(Flash(selfmapping[j][0].get_center(), color=RED, line_length=0.5))
            torecoler=selfmapping[j][1]
            if isinstance(torecoler, list):
                torecoler=torecoler[0]
            q.append(AnimationGroup(torecoler.animate.set_color(RED)))
        if q != []:
            manimScene.playWithEnquedAnimations(q)
        for j in range(*i.indices(len(selfdata))):
            torecoler=selfmapping[j][1]
            if isinstance(torecoler, list):
                torecoler=torecoler[0]
            manimScene.enqAnimation(AnimationGroup((torecoler.animate.set_color(WHITE))))
    def RegisterNode(self, registrar):
        self.registeredNodes.append(registrar)
        return len(self.registeredNodes)
    def yOrder(self):
                
        conectionCounts = {}
        nodeLookups = {}
        zeros = []
        for i in self.registeredNodes:
            if i != None:
                conectionCounts[i.id] = 0
                nodeLookups[i.id] = i
        for i in nodeLookups:
            for j in nodeLookups[i].children:
                conectionCounts[j.id] += 1
        for i in nodeLookups:
            if conectionCounts[nodeLookups[i].id] == 0:
                zeros.append(nodeLookups[i])
        visits = 0
        layer = self.getNextOpenYpos()
        tempLayer = layer
        ans = zeros.copy()
        unplaced = {i:True for i in nodeLookups}
        layered = []
        while len(zeros) > 0:#len(unplaced) > 0:
            if len(zeros) == 0:
                layer = tempLayer
                for i in unplaced:
                    zeros.append(nodeLookups[i])
                    ans.append(nodeLookups[i])
                    break
            while len(zeros) > 0:
                visits += len(zeros)
                newZeros = []
                for i in zeros:
                    for j in i.children:
                        if j.id in unplaced:
                            conectionCounts[j.id] -= 1
                            if conectionCounts[j.id] == 0:
                                newZeros.append(j)
                for i in zeros:
                    if i.id in unplaced:
                        del unplaced[i.id]
                        layered.append([i,layer])
                        #i.position[1] = layer
                layer -= 1.1
                zeros = newZeros
            
        if visits != len(nodeLookups):
            #0/0 #this is a graph not a DAG
            def dist(x,y):
                d = ((x[0]-y[0])**2+(x[1]-y[1])**2)**(1/2)
                return d
            if True:
                parents = {i:[] for i in nodeLookups}
                for i in nodeLookups:
                    for j in nodeLookups[i].children:
                        parents[j.id].append(nodeLookups[i])
                layer = self.getNextOpenYpos()
                K = 0.01
                def childAtractor(x, y, k=K):
                    d = dist(x,y)#((x[0]-y[0])**2+(x[1]-y[1])**2+(x[2]-y[2])**2)**(1/2)
                    return k*d*d
                

                maxDeg = 0
                for i in nodeLookups:
                    maxDeg = max(maxDeg, len(nodeLookups[i].children))
                    
                def pointToPointCost(x, y, k=K*(5**3), k2=maxDeg+4):
                    d = dist(x,y)#((x[0]-y[0])**2+(x[1]-y[1])**2+(x[2]-y[2])**2)**(1/2)
                    if d == 0:
                        return k*1000000000
                    ans = k*(1/d)
                    if d > k2:
                        ans += K*((d-k2)**2)
                    return ans
                def getPointToPointCosts(p, node, k=maxDeg+2):
                    ans = 0
                    for i in nodeLookups:
                        if nodeLookups[i] != node:
                            ans += pointToPointCost(p,nodeLookups[i].position, k=K*(k**3))
                    for i in node.children:
                        ans += childAtractor(p,i.position)
                    for i in parents[node.id]:
                        ans += childAtractor(p,i.position)
                        
                    return ans
                def getPointGradiant(p, node):
                    ans = []
                    close = [i.position for i in node.children]
                    for d in range(3):
                        epsilon = 0.00001
                        pl = [i-(epsilon*(c==d)) for c, i in enumerate(p)]
                        pr = [i+(epsilon*(c==d)) for c, i in enumerate(p)]
                        cl=getPointToPointCosts(pl, node)
                        cr=getPointToPointCosts(pr, node)
                        ans.append((cr-cl)/epsilon)
                    return ans
                for _ in range(100):
                    for i, nod in enumerate(nodeLookups):
                        node=nodeLookups[nod]
                        g = getPointGradiant(node.position, node)
                        node.position = [j-g[c] for c, j in enumerate(node.position)]                      

            else:            
                ajasencyMatrix = [[0]*len(nodeLookups) for i in nodeLookups]
                for x, i in enumerate(nodeLookups):
                    for y, j in enumerate(nodeLookups[i].children):
                        ajasencyMatrix[x][y] += 1


                A = csr_matrix(ajasencyMatrix)
                n = len(nodeLookups)
                degrees = np.array(A.sum(axis=1)).flatten()
                D_inv_sqrt = np.diag(1.0 / np.sqrt(degrees + 1e-8))
                L = np.eye(n) - D_inv_sqrt @ A.toarray() @ D_inv_sqrt
                vals, vecs = eigsh(L, k=3, which="SM")
                
                
                #print(vecs)
                #print(nodeLookups)
                
                for i in nodeLookups:
                    nodeLookups[i].position = [vecs[i-1, 1], vecs[i-1, 2]]
                """
                for i in nodeLookups:
                    nodeLookups[i].position = [pos[i][0], pos[i][1]]
                """
            dis = [nodeLookups[i].position for i in nodeLookups]
            dis.sort()
            targetDistance = 2
            minDis = targetDistance if len(dis) < 2 else 9999999
            minPair = [-1, -1]
            s = 0
            e = 0
            bst = SortedList()
            while e < len(dis):
                bst.add(dis[e][::-1])
                while dis[e][0]-dis[s][0]>minDis:
                    bst.remove(dis[s][::-1])
                    s += 1
                
                left = bst.bisect_left([dis[e][1]-minDis, dis[e][0]])
                right = bst.bisect_right([dis[e][1]+minDis, dis[e][0]])
                for i in bst[left:right]:
                    testDis = dist(dis[e], i[::-1])#((dis[e][0]-i[1])**2+(dis[e][1]-i[0])**2)**(1/2)
                    if testDis != 0:
                        if testDis < minDis:
                            minDis = testDis
                        
                            #minPair = [[nodeLookups[nod].data for nod in nodeLookups if dis[e] == nodeLookups[nod].position], [nodeLookups[nod].data for nod in nodeLookups if i[::-1] == nodeLookups[nod].position]]
                        
                e += 1
            minDis /= targetDistance
            #print("minDis = ", minDis)
            #print("minPair = ", minPair)
            for i in nodeLookups:
                #pass
                nodeLookups[i].position = [nodeLookups[i].position[0]/minDis, nodeLookups[i].position[1]/minDis]

            minPos = [0,-layer] if len(nodeLookups) == 0 else [99999,-99999]
            for i in nodeLookups:
                minPos = [min(minPos[0],nodeLookups[i].position[0]), max(minPos[1],nodeLookups[i].position[1])]
            #print("minPos = ", minPos)
            
            #maxPos = [0,0]
            #for i in nodeLookups:
            #    maxPos = [max(maxPos[0],nodeLookups[i].position[0]), min(maxPos[1],nodeLookups[i].position[1])]

            #print("maxPos = ", maxPos)

            topLeft = [0,0]#[5,3]
            #print("layer = ", layer)
            for i in nodeLookups:
                nodeLookups[i].position = [nodeLookups[i].position[0]-minPos[0]+topLeft[0],nodeLookups[i].position[1]-minPos[1]+topLeft[1]+layer]
                #print(f"nodeLookups[{i}].position =", nodeLookups[i].position)
            #print("len(nodeLookups) = ", len(nodeLookups))
            
            return None
        for i in layered:
            i[0].position[1] = i[1]
        return ans
    def xOrder(self, order):
        visited = {}
        self.colum = 0
        def visit(node):
            node.position[0] = manimScene.colum
            manimScene.colum += 1.1
        for i in order:
            i.inorerTraversal(visit, visited)
        return self.colum
    def UpateNodePositions(self):
        
        yorder = self.yOrder()
        self.isDag = yorder != None
        if yorder != None:
            self.xOrder(yorder)
        arr = []
        for i in self.registeredNodes:
            if i != None:
                i.place()
##                arr.append(AnimationGroup(i.manimSelf[0].animate.move_to(i.position + [0])))
##                arr.append(self.moveText(i.manimSelf[1], i.position + [0]))#AnimationGroup(i.manimSelf[1].animate.move_to(i.position + [0])))            
##                self.fixCam(i.position)
##                for indx, j in enumerate(i.children):
##                    start = i.position.copy()
##                    start[1] -= 0.5
##                    end = j.position.copy()
##                    end[1] += 0.5
##                    #print(i.data, j.data, "->", start, end)
##                    arr.append(AnimationGroup(i.manimChilren[indx].animate.put_start_and_end_on(start + [0], end + [0])))


        manimScene.playWithEnquedAnimations(arr)
        manimScene.pause(waittime)
    def swop(self, s, e):
        global speed
        temp = speed
        speed = 0.0666667
        manimScene.playWithEnquedAnimations([])
        speed = temp
        a = None
        b = None
        if type(s) == type([]) and type(s[0]) == ManimList:
            a = s[0].mapping[s[1]][1]
            oa = "s[0].data[s[1]]"
            oat = "s[0].mapping[s[1]][1]"
        if type(s) == Node:
            a = s.manimSelf[1]
            oa = "s.data"
            oat = "s.manimSelf[1]"
        if type(e) == type([]) and type(e[0]) == ManimList:
            b = e[0].mapping[e[1]][1]
            ob = "e[0].data[e[1]]"
            obt = "e[0].mapping[e[1]][1]"
        if type(e) == Node:
            b = e.manimSelf[1]
            ob = "e.data"
            obt = "e.manimSelf[1]"
        al = self.findTextLocation(a)
        bl = self.findTextLocation(b)
        if not(a) or not(b):
            raise Exception("""you did not pass valid tipes in to the swop function. my best guess as to why this happened is you probubly did somthing like:
x = ManimList([1,2,3,4,5])
manimScene.swop(x[0], x[1])

however this is wrong and needs to be switched to:
x = ManimList([1,2,3,4,5])
manimScene.swop([x,0], [x,1])""")
        exec(f"{oa}, {ob} = {ob}, {oa}")
        exec(f"{oat}, {obt} = {obt}, {oat}")
        manimScene.playWithEnquedAnimations([self.moveText(a, bl), self.moveText(b, al)])
        manimScene.pause(waittime)
    def set(self, s, e):
        global speed
        temp = speed
        speed = 0.0666667
        manimScene.playWithEnquedAnimations([])
        speed = temp
        a = None
        b = None
        if type(s) == type([]) and type(s[0]) == ManimList:
            a = s[0].mapping[s[1]][1]
            oa = "s[0].data[s[1]]"
            oat = "s[0].mapping[s[1]][1]"
        if type(s) == Node:
            a = s.manimSelf[1]
            oa = "s.data"
            oat = "s.manimSelf[1]"
        if type(e) == type([]) and type(e[0]) == ManimList:
            b = self.copyText(e[0].mapping[e[1]][1])
            ob = "e[0].data[e[1]]"
            obt = "b"
        if type(e) == Node:
            b = self.copyText(e.manimSelf[1])
            ob = "e.data"
            obt = "b"
        if not(a) or not(b):
            raise Exception("""you did not pass valid tipes in to the set function. my best guess as to why this happened is you probubly did somthing like:
x = ManimList([1,2,3,4,5])
manimScene.set(x[0], x[1])

however this is wrong and needs to be switched to:
x = ManimList([1,2,3,4,5])
manimScene.set([x,0], [x,1])""")
        al = self.findTextLocation(a)
        bl = self.findTextLocation(b)
        exec(f"{oa} = {ob}")
        exec(f"{oat} = {obt}")
        self.add(b)
        print("al =", al)
        manimScene.playWithEnquedAnimations([self.moveText(b, al), self.UnCreateMulti(a)])
        #manimScene.playWithEnquedAnimations([self.CreateMulti(b), self.moveText(b, al), self.UnCreateMulti(a)])
        manimScene.pause(waittime)



class Node:
    def __init__(self, value):
        self.data = value
        self.children = []
        self.manimSelf = manimScene.getDrawCircle(0, manimScene.getNextOpenYpos(), value, source=self)
        self.manimChilren = []
        self.id=manimScene.RegisterNode(self)
        self.position = [-1,0]
        self.oldPos = self.position.copy()
        self.dependicyes={}
        self.dependicyesNode={}
        self.textDependicyes={}
        self.gon = False
        manimScene.playWithEnquedAnimations(manimScene.CreateMulti(self.manimSelf))
        manimScene.UpateNodePositions()
    def checkGon(self):
        if self.gon:
            raise Exception("you already deleated this node just because you can modify it does not mean you should. This is how use after free exploits happen")
    def deleat(self):
        self.checkGon()
        manimScene.setAnimationsQuing(True)
        bad = []
        for i in self.dependicyesNode:
            bad.append(self.dependicyesNode[i])
        for i in bad:
            i.remove(self)
        while len(self) > 0:
            self.pop()
        manimScene.setAnimationsQuing(False)
        manimScene.playWithEnquedAnimations(manimScene.UnCreateMulti(self.manimSelf))
        manimScene.UpateNodePositions()
        self.gon = True
    def place(self):
        self.checkGon()
        #if self.position == self.oldPos:
        #    return
        self.oldPos = self.position.copy()
        arr = []
        arr.append(AnimationGroup(self.manimSelf[0].animate.move_to(self.position + [0])))
        arr.append(manimScene.moveText(self.manimSelf[1], self.position + [0]))#AnimationGroup(i.manimSelf[1].animate.move_to(i.position + [0])))            
        manimScene.fixCam(self.position)
        if False:#????????????????????????/
            for indx, j in enumerate(self.children):
                start = self.position.copy()
                start[1] -= 0.5*manimScene.isDag
                arr.append(manimScene.moveText(self.manimChilren[indx], start + [0]))
                #end = j.position.copy()
                #end[1] += 0.5
                #print(i.data, j.data, "->", start, end)
                #arr.append(AnimationGroup(self.manimChilren[indx].animate.put_start_and_end_on(start + [0], end + [0])))
        #print(f"{self.id}.dependicyes = ", self.dependicyes,"self.dependicyesNode = ", self.dependicyesNode)
        for i in self.dependicyes:
##            if i < 0:
##                if self.dependicyesNode[i] == None:
##                    start = self.dependicyes[i].start
##                else:
##                    start = self.dependicyesNode[i].position.copy()
##                start[1] += 0.5
##            else:
            start = self.dependicyesNode[i].position.copy()
            #start[1] -= 0.5*manimScene.isDag
            end = self.position.copy()
            #end[1] += 0.5*manimScene.isDag
            normal = [end[0]-start[0],end[1]-start[1]]
            lennormal = (normal[0]**2+normal[1]**2)**(1/2)
            normal = [normal[0]/lennormal, normal[1]/lennormal]
            normal = [normal[0]/2, normal[1]/2]
            start = [start[0]+normal[0], start[1]+normal[1]]
            end = [end[0]-normal[0], end[1]-normal[1]]
            #print("moving arrow", i, "on", self.data, self.id, self.dependicyes, "to", start, end)
            arr.append(AnimationGroup(self.dependicyes[i].animate.put_start_and_end_on(start + [0], end + [0])))
        for i in self.textDependicyes:
            start = self.textDependicyes[i][0].get_start()
            if isinstance(self.textDependicyes[i][1], Node):
                start = self.textDependicyes[i][1].position.copy()
            end = self.position.copy()
            end[1] += 0.5*manimScene.isDag
            arr.append(AnimationGroup(self.textDependicyes[i][0].animate.put_start_and_end_on(start + [0], end + [0])))
        manimScene.enqAnimation(arr)
    def __repr__(self):
        if self.gon:
            return "None"
        if type(self.data) == Node and type(self.data.data) == Node and type(self.data.data.data) == Node and type(self.data.data.data.data) == Node:
            return f"<Node {self.data.id}>"#ToAdd
        return repr(self.data)#ToAdd
    def __lt__(self, other):
        self.checkGon()
        return self.data <  self.__cast(other)#ToAdd
    def __le__(self, other):
        if self.gon and other == None:
            return True
        self.checkGon()
        return self.data <= self.__cast(other)#ToAdd
    def __eq__(self, other):
        if self.gon and other == None:
            return True
        self.checkGon()
        return self.data == self.__cast(other)#ToAdd
    def __gt__(self, other):
        self.checkGon()
        return self.data >  self.__cast(other)#ToAdd
    def __ge__(self, other):
        if self.gon and other == None:
            return True
        self.checkGon()
        return self.data >= self.__cast(other)#ToAdd
    def __cast(self, other):#ToAdd
        #self.checkGon()
        if self.gon:
            return None
        return other.data if isinstance(other, Node) else other
    
    def getData(self):
        if self.gon:
            return None
        manimScene.FlashText(self.manimSelf[1], self.manimSelf[0].get_center())
        manimScene.pause(waittime)
        return self.data
    def setData(self, item):
        self.checkGon()
        self.data = item
        
        newText = manimScene.getTextToDraw(item, fontColor=RED, source=self)
        manimScene.AlterText(self.manimSelf[1], newText, self.manimSelf[0].get_center())
        #manimScene.quietMoveText(newText, self.manimSelf[1].get_center())#newText.move_to(self.manimSelf[1])
        #manimScene.playWithEnquedAnimations([Flash(self.manimSelf[0].get_center(), color=RED, line_length=0.5),
        #                TransformMatchingShapes(self.manimSelf[1], newText)])
        self.manimSelf[1] = newText
        #manimScene.enqAnimation(AnimationGroup(newText.animate.set_color(WHITE)))
        manimScene.pause(waittime)
    def __len__(self):
        self.checkGon()
        return len(self.children)
    def __getitem__(self, i):
        self.checkGon()
        manimScene.FlashText(self.manimChilren[i], self.manimChilren[i].get_center(), returnColor=GREEN)
        return self.children[i] #ToAdd
    def __setitem__(self, i, item):
        self.checkGon()
        if item == self.children[i]:
            return
        if self.id in item.dependicyes:
            raise Exception("hay sorry I think you have already connected those two nodes i can not have two connections going from the same node to the same node it would break some internal stuff because i did not consider this might happen")
            0/0#duplicate child
        global speed
        temp = speed
        speed = 0.0666667
        manimScene.playWithEnquedAnimations([])
        speed = temp


        temp = self.children[i].dependicyes[self.id]
        tempn = self.children[i].dependicyesNode[self.id]
        del self.children[i].dependicyes[self.id]
        del self.children[i].dependicyesNode[self.id]
        item.dependicyes[self.id] = temp
        item.dependicyesNode[self.id] = tempn
        #item.dependicyes[self.id] = item.dependicyes[self.children[i].id]
        #item.dependicyesNode[self.id] = item.dependicyesNode[self.children[i].id]
        #del item.dependicyes[self.children[i].id]
        #del item.dependicyesNode[self.children[i].id]
        
        self.children[i] = item
        manimScene.UpateNodePositions()
    def __delitem__(self, i):
        self.checkGon()
        temp = self.manimChilren[i]
        manimScene.enqAnimation(manimScene.UnCreateMulti([temp]))
        del self.manimChilren[i]
        del i.dependicyes[self.id]
        del i.dependicyesNode[self.id]
        del self.children[i]
        manimScene.UpateNodePositions()
    def append(self, item):
        self.checkGon()
        if isinstance(item, Node):
            if self.id in item.dependicyes:
                raise Exception("hay sorry I think you have already connected those two nodes i can not have two connections going from the same node to the same node it would break some internal stuff because i did not consider this might happen")
                0/0#duplicate child
            start=[self.position[0], self.position[1]-0.5*manimScene.isDag]
            end = [item.position[0], item.position[1]+0.5*manimScene.isDag]
            normal = [end[0]-start[0],end[1]-start[1]]
            lennormal = (normal[0]**2+normal[1]**2)**(1/2)
            normal = [normal[0]/lennormal, normal[1]/lennormal]
            normal = [normal[0]/2, normal[1]/2]
            start = [start[0]+normal[0], start[1]+normal[1]]
            end = [end[0]-normal[0], end[1]-normal[1]]
            arrow = Arrow(
                #start=self.manimSelf[0].get_bottom(),   # rightmost point of left circle
                start=start+[0],#[self.position[0], self.position[1]-0.5*manimScene.isDag, 0],
                end=end+[0],#[item.position[0], item.position[1]+0.5*manimScene.isDag, 0],
                #end=item.manimSelf[0].get_top(),     # leftmost point of right circle
                color=GREEN,
                buff=0                         # small gap so arrow doesn’t overlap the circles
            )
            item.dependicyes[self.id] = arrow
            item.dependicyesNode[self.id] = self
            
            manimScene.playWithEnquedAnimations(manimScene.CreateMulti([arrow]))
            self.children.append(item)
            self.manimChilren.append(arrow) 
            manimScene.UpateNodePositions()
        else:
            self.append(Node(item))
            #wrong type add better error hanling
    def insert(self, i, item):
        self.checkGon()
        if isinstance(item, Node):
            if self.id in item.dependicyes:
                raise Exception("hay sorry I think you have already connected those two nodes i can not have two connections going from the same node to the same node it would break some internal stuff because i did not consider this might happen")
                0/0#duplicate child
            start = [self.position[0], self.position[1]-0.5*manimScene.isDag, 0]
            end = [item.position[0], item.position[1]+0.5*manimScene.isDag, 0]
            normal = [end[0]-start[0],end[1]-start[1]]
            lennormal = (normal[0]**2+normal[1]**2)**(1/2)
            normal = [normal[0]/lennormal, normal[1]/lennormal]
            normal = [normal[0]/2, normal[1]/2]
            start = [start[0]+normal[0], start[1]+normal[1]]
            end = [end[0]-normal[0], end[1]-normal[1]]
            arrow = Arrow(
                #start=self.manimSelf[0].get_bottom(),   # rightmost point of left circle
                start=start,#[self.position[0], self.position[1]-0.5*manimScene.isDag, 0],
                end=end,#[item.position[0], item.position[1]+0.5*manimScene.isDag, 0],
                #end=item.manimSelf[0].get_top(),     # leftmost point of right circle
                color=GREEN,
                buff=0                         # small gap so arrow doesn’t overlap the circles
            )
            item.dependicyes[self.id] = arrow
            item.dependicyesNode[self.id] = self
            manimScene.playWithEnquedAnimations(manimScene.CreateMulti([arrow]))
            self.children.insert(i, item)
            self.manimChilren.insert(i, arrow) 
            manimScene.UpateNodePositions()
        else:
            0/0#wrong type add better error hanling
    def pop(self, i=-1):
        self.checkGon()
        manimScene.enqAnimation(manimScene.UnCreateMulti([self.manimChilren.pop(i)]))
        ans = self.children.pop(i)
        del ans.dependicyes[self.id]
        del ans.dependicyesNode[self.id]
        #item.dependicyes.remove(self)#slow
        manimScene.UpateNodePositions()
        return ans
    def remove(self, item):
        self.checkGon()
        self.pop(self.index(item))
    def index(self, target):
        self.checkGon()
        for p, i in enumerate(self.children):
            if i == target:
                return p
        return -1
    def reverse(self):
        self.checkGon()
        self.children.reverse()
        manimScene.UpateNodePositions()
    def inorerTraversal(self, visit, visited={}):
        self.checkGon()
        if self.id in visited:
            return
        visited[self.id] = True
        for i in self.children[:len(self.children)//2]:
            i.inorerTraversal(visit, visited)
        visit(self)
        for i in self.children[len(self.children)//2:]:
            i.inorerTraversal(visit, visited)
    def leftMost(self):
        self.checkGon()
        if self.children == []:
            return self
        return self.children[0].leftMost()
    def rightMost(self):
        self.checkGon()
        if self.children == []:
            return self
        return self.children[-1].rightMost()


    
#!!!!!!!!maby replaced all instances of UserList with ManimList bug test!!!!!!!!!!!!!!
class ManimList(list):#_collections_abc.MutableSequence):
    """A more or less complete user-defined wrapper around list objects."""
    def __init__(self, initlist=None):
        self.data = []
        if initlist is not None:
            # XXX should this accept an arbitrary sequence?
            if type(initlist) == type(self.data):
                self.data[:] = initlist
            elif isinstance(initlist, ManimList):
                self.data[:] = initlist.data[:]
            else:
                self.data = list(initlist)
                
        self.ypos = manimScene.getNextOpenYpos()
        self.mapping = manimScene.constructArray(self.data, 0, self.ypos)
        if len(self.mapping) != 0:
            manimScene.playWithEnquedAnimations(manimScene.CreateMulti(self.mapping))
            manimScene.pause(waittime)
        manimScene.UpateNodePositions()
    def __repr__(self): return repr(self.data)#ToAdd
    def __lt__(self, other): return self.data <  self.__cast(other)#ToAdd
    def __le__(self, other): return self.data <= self.__cast(other)#ToAdd
    def __eq__(self, other): return self.data == self.__cast(other)#ToAdd
    def __gt__(self, other): return self.data >  self.__cast(other)#ToAdd
    def __ge__(self, other): return self.data >= self.__cast(other)#ToAdd
    def __cast(self, other):#ToAdd
        return other.data if isinstance(other, ManimList) else other
    def __contains__(self, item): return item in self.data#ToAdd
    def __len__(self): return len(self.data)#ToAdd
    def __getitem__(self, i):
        if isinstance(i, slice):
            manimScene.FlashTextArray(self.data, self.mapping)
            manimScene.pause(waittime)
            
            return self.__class__(self.data[i])
        else:
            #q = [Flash(self.mapping[i][0].get_center(), color=RED, line_length=0.5),
            #     AnimationGroup(self.mapping[i][1].animate.set_color(RED))]
            #manimScene.playWithEnquedAnimations(q)
            #manimScene.enqAnimation(AnimationGroup((self.mapping[i][1].animate.set_color(WHITE))))
            manimScene.FlashText(self.mapping[i][1], self.mapping[i][0].get_center())
            manimScene.pause(waittime)
            
            return self.data[i]
    def __setitem__(self, i, item):
        self.data[i] = item
        
        newText = manimScene.getTextToDraw(item, fontColor=RED)
        manimScene.AlterText(self.mapping[i][1], newText, self.mapping[i][0].get_center())
        #manimScene.quietMoveText(newText, self.mapping[i][1].get_center())#newText.move_to(self.mapping[i][1])
        #manimScene.playWithEnquedAnimations([Flash(self.mapping[i][0].get_center(), color=RED, line_length=0.5),
        #                TransformMatchingShapes(self.mapping[i][1], newText)])
        self.mapping[i][1] = newText
        #manimScene.enqAnimation(AnimationGroup(newText.animate.set_color(WHITE)))
        manimScene.pause(waittime)
    def __delitem__(self, i):#warning
        if isinstance(i, slice):
            # compute the range of indices to remove
            # pop from the end so indices don't shift
            start, stop, step = i.indices(len(self.data))
            indices = range(start, stop, step)
            for j in sorted(list(indices))[::-1]:
                self.pop(j)
        else:
            # single index
            self.pop(i)
        
        #del self.data[i]
    def __add__(self, other):#ToAdd?
        if isinstance(other, ManimList):
            return self.__class__(self.data + other.data)
        elif isinstance(other, type(self.data)):
            return self.__class__(self.data + other)
        return self.__class__(self.data + list(other))
    def __radd__(self, other):#ToAdd?
        if isinstance(other, ManimList):
            return self.__class__(other.data + self.data)
        elif isinstance(other, type(self.data)):
            return self.__class__(other + self.data)
        return self.__class__(list(other) + self.data)
    def __iadd__(self, other):
        oldLength = len(self.data)
        
        if isinstance(other, ManimList):
            self.data += other.data
        elif isinstance(other, type(self.data)):
            self.data += other
        else:
            self.data += list(other)
            
        newStuff = []
        first = self.mapping[0][0].get_center()
        for i, v in enumerate(self.data):
            if i >= oldLength:
                newStuff += manimScene.getDrawSquair(first[0]+i, first[1], txt=v)
        manimScene.playWithEnquedAnimations(manimScene.CreateMulti(newStuff))
        manimScene.pause(waittime)
        self.mapping += newStuff

            
        return self
    def __mul__(self, n):#ToAdd?
        return self.__class__(self.data*n)
    __rmul__ = __mul__
    def __imul__(self, n):
        if n == 0:
            self.clear()
            return
        if self.mapping != []:
            newStuff = []
            first = self.mapping[0][0].get_center()
            for j in range(n-1):
                for i, v in enumerate(self.data):
                    newStuff += manimScene.getDrawSquair(first[0]+i, first[1], txt=v)
            manimScene.play(manimScene.CreateMulti(newStuff), run_time=0.0666667)
            self.mapping += newStuff
            arr = []
            for c, i in enumerate(self.mapping):
                newPos = i[0].get_center()
                newPos[0] = first[0]+c*1
                arr.append(AnimationGroup(i[0].animate.move_to(newPos)))
                arr.append(manimScene.moveText(i[1], newPos))#AnimationGroup(i[1].animate.move_to(newPos)))
            manimScene.playWithEnquedAnimations(arr)
            manimScene.pause(waittime)
        
        self.data *= n
        return self
    def __copy__(self):#ToAdd
        inst = self.__class__.__new__(self.__class__)
        inst.__dict__.update(self.__dict__)
        # Create a copy and avoid triggering descriptors
        inst.__dict__["data"] = self.__dict__["data"][:]
        return inst
    def append(self, item):
        self.data.append(item)
        
        if False:#self.mapping == []:
            self.mapping = manimScene.constructArray(self.data, 0)
            manimScene.playWithEnquedAnimations(manimScene.CreateMulti(self.mapping))
        else:
        #print("self.mapping = ", self.mapping)
            placePos = [len(self.mapping), self.ypos]#self.mapping[-1][0].get_center()
            #placePos[0] += 1
            newSquair = manimScene.getDrawSquair(placePos[0], placePos[1], item)
            manimScene.playWithEnquedAnimations(manimScene.CreateMulti(newSquair))
            self.mapping += (newSquair)
        #print("self.mapping = ", self.mapping)
        manimScene.pause(waittime)
    def insert(self, i, item):
        self.data.insert(i, item) 
        
        if self.mapping == []:
            self.mapping = manimScene.constructArray(self.data, 0)
            manimScene.playWithEnquedAnimations(manimScene.CreateMulti(self.mapping))
        else:
            ii = (i if i >= 0 else len(self.mapping)+i)
            #print("self.mapping = ", self.mapping)
            placePos = self.mapping[-1][0].get_center()
            placePos[0] += 1
            newSquair = manimScene.getDrawSquair(placePos[0], placePos[1], item)
            newSquair[0][1].shift(RIGHT * -(len(self.mapping)-ii))
            newText2 = newSquair[0][1]
            newItems = manimScene.CreateMulti(newSquair)
            manimScene.playWithEnquedAnimations([newItems[0]])
            self.mapping += (newSquair)
            newText = newItems[1]
            arr = []
            for j in range(len(self.mapping)-2, ii-1, -1):
                #manimScene.playWithEnquedAnimations([AnimationGroup(self.mapping[j+1][1].animate.move_to(self.mapping[j][0].get_center()))])
                arr.append(manimScene.moveText(self.mapping[j][1], self.mapping[j+1][0].get_center()))#AnimationGroup(self.mapping[j][1].animate.move_to(self.mapping[j+1][0].get_center())))
                self.mapping[j+1][1] = self.mapping[j][1]
            manimScene.playWithEnquedAnimations(arr)
            
            manimScene.playWithEnquedAnimations([newText])
            self.mapping[ii][1] = newText2
            #self.mapping += (newSquair)
            #print("self.mapping = ", self.mapping)
        manimScene.pause(waittime)
        
        
        #print("self.data = ", self.data)
    def pop(self, i=-1):
        #manimScene.playWithEnquedAnimations(manimScene.UnCreateMulti(self.mapping.pop()))
        #print("self.mapping = ", self.mapping)
        #print("self.mapping = ", self.mapping)
        manimScene.playWithEnquedAnimations(manimScene.UnCreateMulti(self.mapping[i][1]))
        arr = []
        for j in range((i if i >= 0 else len(self.mapping)+i), len(self.mapping)-1):
            #manimScene.playWithEnquedAnimations([AnimationGroup(self.mapping[j+1][1].animate.move_to(self.mapping[j][0].get_center()))])
            arr.append(manimScene.moveText(self.mapping[j+1][1], self.mapping[j][0].get_center()))#AnimationGroup(self.mapping[j+1][1].animate.move_to(self.mapping[j][0].get_center())))
            self.mapping[j][1] = self.mapping[j+1][1]
        manimScene.playWithEnquedAnimations(arr)
        manimScene.playWithEnquedAnimations(manimScene.UnCreateMulti(self.mapping[-1][0]))
        self.mapping.pop()
        #print("self.mapping = ", self.mapping)
        
        manimScene.pause(waittime)
        return self.data.pop(i)
    def remove(self, item):#warning
        self.pop(self.index(item))
        
        #self.data.remove(item)
    def clear(self):
        manimScene.playWithEnquedAnimations(manimScene.UnCreateMulti(self.mapping))
        self.mapping = []
        manimScene.pause(waittime)
        
        self.data.clear()
    def copy(self): return self.__class__(self)#ToAdd?
    def count(self, item): return self.data.count(item)#ToAdd
    def index(self, item, *args): return self.data.index(item, *args)#ToAdd
    def reverse(self):
        arr = []
        for i, v in enumerate(self.mapping):
            arr.append(manimScene.moveText(self.mapping[i][1], self.mapping[len(self.mapping)-i-1][0].get_center()))#AnimationGroup(self.mapping[i][1].animate.move_to(self.mapping[len(self.mapping)-i-1][0].get_center())))            
        self.mapping = [[i[0],j[1]] for i, j in zip(self.mapping, self.mapping[::-1])]
        manimScene.playWithEnquedAnimations(arr)
        manimScene.pause(waittime)
        self.data.reverse()
    def sort(self, *args, **kwds):
        ogmap = {}
        for c, i in enumerate(self.data):
            if str(i) not in ogmap:
                ogmap[str(i)] = []
            ogmap[str(i)].append(c)
        for i in ogmap:
            ogmap[i] = ogmap[i][::-1]
        self.data.sort(*args, **kwds)
        
        backup = [i[1] for i in self.mapping]
        for i, v in enumerate(self.data):
            self.mapping[i][1] = backup[ogmap[str(v)].pop()]
        arr = []
        for i in self.mapping:
            arr.append(manimScene.moveText(i[1], i[0].get_center()))#AnimationGroup(i[1].animate.move_to(i[0].get_center())))            
        manimScene.playWithEnquedAnimations(arr)
        manimScene.pause(waittime)
            
    def extend(self, other):#ToAdd
        if isinstance(other, ManimList):
            self.data.extend(other.data)
        else:
            self.data.extend(other)

