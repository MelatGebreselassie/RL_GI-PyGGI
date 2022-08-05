from pyggi.tree.edits import NodeDeletion, NodeInsertion, NodeReplacement 

class MultilineStatementInsertion(NodeInsertion):
    NODE_PARENT_TYPE = 'block'
    NODE_TYPE = "multiline_stmt"