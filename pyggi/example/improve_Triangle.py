import argparse
import copy
from distutils.log import error
import random
from pyggi.base import Patch, AbstractProgram
#-- Epsilon Greedy
from greedy import ExpProtocol, MyAlgorithm, MyProgram, MySrcmlEngine, MyTreeProgram


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
    protocol.program = program_klass('../sample/Triangle_fast_java')

    # run experiments
    protocol.run()
