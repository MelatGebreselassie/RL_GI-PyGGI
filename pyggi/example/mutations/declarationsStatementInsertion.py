from pyggi.tree.edits import NodeDeletion, NodeInsertion, NodeReplacement 

class declarationsStatementInsertion(NodeInsertion):
    NODE_PARENT_TYPE = 'block'
    NODE_TYPE = "declarations"