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

class MySrcmlEngine(SrcmlEngine):
    TAG_RENAME = {
            'stmt': {'break', 'continue', 'return', 'goto'},

            'multiline_stmt': {'do', 'for', 'if', 'switch', 'while'},

            'declarations': {'decl_stmt'},

            'expression': {'expr_stmt'}
            
        }

    TAG_FOCUS = {'block', 'stmt', 'multiline_stmt', 'declarations', 'expression'}


    PROCESS_LITERALS = False
    PROCESS_OPERATORS = False