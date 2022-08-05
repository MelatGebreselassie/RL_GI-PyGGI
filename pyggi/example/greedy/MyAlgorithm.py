import argparse
import copy
from distutils.log import error
import random
import numpy as np
import matplotlib.pyplot as plt
from pyggi.base import Patch, AbstractProgram
from pyggi.line import LineProgram
from pyggi.line import LineReplacement, LineInsertion, LineDeletion
from pyggi.tree.edits import NodeDeletion, NodeInsertion, NodeReplacement 
from pyggi.tree import SrcmlEngine
from pyggi.tree import StmtReplacement, StmtInsertion, StmtDeletion
from pyggi.algo import FirstImprovement
# import numpy as np
class MyAlgorithm(FirstImprovement):
    def hook_evaluation(self, patch, run, accept, best):
        super().hook_evaluation(patch, run, accept, best)
        if(self.program.last_edit_type is not None):
            reward = 0
            if (run.status == "SUCCESS"):
                reward = 1
            self.rewards(self.program.last_edit_type, reward)
        self.program.last_edit_type = None
        self.program.logger.info('log file')
        print(run)
        

    def rewards(self, operator, reward):
        print("reward before", self.program.rewards[operator])
        alpha = 0.85 #ref: Mansour et al.
        self.program.rewards[operator] = self.program.rewards[operator] + alpha* (reward - self.program.rewards[operator])
        print("reward after", self.program.rewards[operator])