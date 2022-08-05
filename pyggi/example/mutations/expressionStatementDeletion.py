from pyggi.tree.edits import NodeDeletion, NodeInsertion, NodeReplacement 

class expressionStatementDeletion(NodeDeletion):
    NODE_TYPE = "expression"