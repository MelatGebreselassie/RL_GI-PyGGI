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
import numpy as np



class MyProgram(AbstractProgram):
   
    def epsilon_greedy(self, eps):
        j = max(self.rewards, key=self.rewards.get)
        p = np.random.random()
        
        if p < eps:
            while (True):
                j2 = random.choice(self.possible_edits)
                if (j2 != j):
                    return j2
        else:
            return j


    def create_edit(self, patch=None):
        print("rewards", self.rewards)
        actions = dict.fromkeys(self.possible_edits, 1)
        for _ in range(1000):
            
            epsilon = 0.1 #ref: Santos Mignon et al.
            discount_factor = 0
            learning_rate = 0.01 

            operator = self.epsilon_greedy(epsilon)
            
            try:
                edit = operator.create(self)
            except KeyError:
                pass
            self.last_edit_type = operator
            

            if (edit is not None):
                return edit
        raise AssertionError('Failed to create a valid edit of type {}'.format(operator))
     
 

        def compute_fitness(self, result, return_code, stdout, stderr, elapsed_time):
            try:
                runtime, pass_all = stdout.strip().split(',')
                runtime = float(runtime)
                if not pass_all == 'true':
                    result.status = 'PARSE_ERROR'
                else:
                    result.fitness = runtime
            except:
                result.status = 'PARSE_ERROR'