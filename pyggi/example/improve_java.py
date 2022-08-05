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

# ================================================================================
# Experimental protocol
# ================================================================================

class MultilineStatementDeletion(NodeDeletion):
    NODE_TYPE = "multiline_stmt"

class MultilineStatementInsertion(NodeInsertion):
    NODE_PARENT_TYPE = 'block'
    NODE_TYPE = "multiline_stmt"

class MultilineStatementReplacement(NodeReplacement):
    NODE_TYPE = "multiline_stmt"


class declarationsStatementDeletion(NodeDeletion):
     
    NODE_TYPE = "declarations"

class declarationsStatementInsertion(NodeInsertion):
    NODE_PARENT_TYPE = 'block'
    NODE_TYPE = "declarations"

class declarationsStatementReplacement(NodeReplacement):
    NODE_TYPE = "declarations"


class expressionStatementDeletion(NodeDeletion):
    NODE_TYPE = "expression"

class expressionStatementInsertion(NodeInsertion):
    NODE_PARENT_TYPE = 'block'
    NODE_TYPE = "expression"

class expressionStatementReplacement(NodeReplacement):
    NODE_TYPE = "expression"



class ExpProtocol:
    def __init__(self):
        self.nb_epoch = 10
        self.search = None
        self.program = None

    def run(self):
        if self.program is None:
            raise AssertionError('Program not specified')
        if self.search is None:
            raise AssertionError('Search not specified')

        self.search.config['warmup'] = 3
        self.search.program = self.program

        logger = self.program.logger
        result = []
        default_result = {'stop': None, 'best_patch': []}
        try:
            for epoch in range(self.nb_epoch):
                result.append(default_result)
                logger.info('========== EPOCH {} =========='.format(epoch+1))
                self.search.reset()
                self.search.run()
                r = copy.deepcopy(self.search.report)
                r['diff'] = self.program.diff(r['best_patch'])
                result[epoch] = r
                logger.info('')
        except KeyboardInterrupt:
            result[epoch]['stop'] = 'keyboard interrupt'

        logger.info('========== REPORT ==========')
        for epoch in range(len(result)):
            logger.info('==== Epoch {} ===='.format(epoch+1))
            logger.info('Termination: {}'.format(result[epoch]['stop']))
            if result[epoch]['best_patch']:
                logger.info('Best fitness: {}'.format(result[epoch]['best_fitness']))
                logger.info('Best patch: {}'.format(result[epoch]['best_patch']))
                logger.info('Diff:\n{}'.format(result[epoch]['diff']))
        self.program.remove_tmp_variant()


# ================================================================================
# Target software specifics
# ================================================================================
class MyAlgorithm(FirstImprovement):
    # Update the action-value estimate
    
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
        #reward
        alpha = 0.85 #ref: Mansour et al.
        # q_value = 0
        #Temporal Difference update - literature references
        # temporal_difference = reward + (discount_factor * np.max(q_values[self.possible_edits[j]])) - old_q_value

        #updating the new reward value - 
        self.program.rewards[operator] = self.program.rewards[operator] + alpha* (reward - self.program.rewards[operator])
        
        print("reward after", self.program.rewards[operator])
        
        # new_q_value = 0
        # q_values[self.possible_edits[j]] = new_q_value

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

        # cumulative_average = np.cumsum(data) / (np.arange(N) + 1)

    def create_edit(self, patch=None):
        print("rewards", self.rewards)
        actions = dict.fromkeys(self.possible_edits, 1)
        for _ in range(1000):
            #needs changing later this is where the selection takes place with self.reward - using the reward in hook evaluation
            # operator = random.choice(self.possible_edits)
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
     
        # print('Selection complete!')

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

class MyLineProgram(LineProgram, MyProgram):
    def setup(self, config):
        self.target_files = ["Triangle.java"]
        self.test_command = "./run.sh"
        self.possible_edits = [LineReplacement, LineInsertion, LineDeletion]



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


# ================================================================================
# Main function
# ================================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PYGGI Improvement Example')
    parser.add_argument('--mode', type=str, default='tree')
    parser.add_argument('--epoch', type=int, default=30,
        help='total epoch(default: 30)')
    parser.add_argument('--iter', type=int, default=100,
        help='total iterations per epoch(default: 100)')
    args = parser.parse_args()

    if args.mode == 'line':
        program_klass = MyLineProgram
    elif args.mode == 'tree':
        program_klass = MyTreeProgram
    else:
        raise RuntimeError('Invalid mode: {}'.format(args.mode))

    # setup protocol
    protocol = ExpProtocol()
    protocol.nb_epoch = args.epoch
    protocol.search = MyAlgorithm()
    protocol.search.stop['fitness'] = 100
    protocol.search.stop['steps'] = args.iter
    protocol.program = program_klass('../pyggi_moead/pyggi/sample/Triangle_fast_java')

    # run experiments
    protocol.run()
