run with:
manim -pql  --resolution 1920,1080 manimTest.py -- --mainScene <your file here with the .py>
Or for on Mac you can optionally use the slow bad way:
./dockerRunInstructions <your file here with the .py>
Example:
manim -pql  --resolution 1920,1080 manimTest.py -o videoName -- --mainScene manimTestUserSide.py
For example code check the examples folder

how to make an array:
	replace any array declarations you wish to visualize with ManimList(<the normal array declaration>)
	all other array functionality works the same

Nodes:
	node constructor: Node(<starting value>)
	access child nodes the same you would a array
	get data with: <node variable>.getData()
        Set data with: <node variable>.setData(<new data>)
	use .deleat() to delete a node
Visual helps
	onscreen display with: manimScene.onScreenPrint(<string to display>)
	pause animation rendering with manimScene.setAnimationsQuing(True)
	unpause animation rendering with manimScene.setAnimationsQuing(False)
	set playback speed with speed = <new speed in seconds>
	set animation pause time with waittime = <new time between animations>
	manimScene.swop(<Node/[<ManimList>, <location>]>, <Node/[<ManimList>, <location>]>) swops things see examples/swopingFunction for examples of how to use
	manimScene.set(<Node/[<ManimList>, <location>]>, <Node/[<ManimList>, <location>]>) sets the first thing to the second see examples/swopingFunction for examples of how to use
	with 2d arrays do not visualize the outer array

Tips for visible legibility:
	minimize unnecessary get operations by storing the results in helper variables
	use the swop and set functions whenever possible
	use onScreenPrint to help the user track the most current most important variables and the current state of the program 
	allocate array memory ahead of time whenever possible to prevent visually unpleasant memory leaks
	use * to denote an empty value
	use manimScene.setAnimationsQuing to group steps together
List of already imported stuff:
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


Advanced:
	we add 2 lines to the start of your code meaning all error messages are 2 lines off in there location
	Deleated nodes can only be used when checking == None casting types(to witch you will get None) and getting data(to witch you will get None)
	manimScene is the main Scene and contains:
		.quedAnimations -> a list of currently unplayed animations
		.takenRows -> a dictionary of rows to avoid putting stuff on
		.camWith -> the current width of the screen (note changing this does not change the width)
		do not put non displayable objects like spaces or empty strings in as any data
	you are running within an exec command inside of the manimTest.py script files are accessed with that as your current directory and there are some odd scope bugs such as:
		.imports can not be used when using an itorater for example the following code fails:
		import random
		[random.random() for i in range(1)]
		.global variables (including your own function) can not be accessed in functions with out the explicit global keyword for example replace the following code:
		
		x = 5
		def stuff():
			x += 1
		stuff()

		with:

		x = 5
		def stuff():
			global x
			x += 1
		stuff()







