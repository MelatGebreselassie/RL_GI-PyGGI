import argparse
import copy
from distutils.log import error
import random
import numpy as np
import matplotlib.pyplot as plt
from pyggi.tree import StmtReplacement, StmtInsertion, StmtDeletion
from greedy import MyProgram
from mutations import MultilineStatementDeletion, MultilineStatementReplacement, MultilineStatementInsertion
from mutations import expressionStatementDeletion, expressionStatementInsertion, expressionStatementReplacement
from mutations import declarationsStatementDeletion, declarationsStatementInsertion, declarationsStatementReplacement
from greedy import MySrcmlEngine
import numpy as np

class MyTreeProgram(MyProgram):
    def setup(self, config):
        self.target_files = ["Triangle.java.xml"]
        self.test_command = "./run.sh"
        self.possible_edits = [StmtReplacement, StmtInsertion, StmtDeletion, MultilineStatementDeletion, MultilineStatementInsertion, MultilineStatementReplacement, declarationsStatementDeletion, declarationsStatementInsertion,declarationsStatementReplacement, expressionStatementDeletion,expressionStatementInsertion,expressionStatementReplacement]

        self.rewards = {StmtReplacement:1, StmtInsertion:1, StmtDeletion:1, MultilineStatementDeletion:1, MultilineStatementInsertion:1, MultilineStatementReplacement:1, declarationsStatementDeletion:1, declarationsStatementInsertion:1,declarationsStatementReplacement:1, expressionStatementDeletion:1,expressionStatementInsertion:1,expressionStatementReplacement:1}

        self.last_edit_type = None

    @classmethod
    def get_engine(cls, file_name):
        return MySrcmlEngine