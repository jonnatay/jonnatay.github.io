"""
run with:
docker build -t manimtest .
docker run --rm manimtest manim helloManim.py HelloManim -- --script " yay"

"""

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
parser.add_argument("--script", default="")
args = parser.parse_args(user_args)
class HelloManim(Scene):
    def construct(self):
        text = Text("Hello, Manim!" + args.script)
        self.play(Write(text))
        self.wait(1)
