from pyggi.tree.edits import NodeDeletion, NodeInsertion, NodeReplacement 

class expressionStatementInsertion(NodeInsertion):
    NODE_PARENT_TYPE = 'block'
    NODE_TYPE = "expression"