from pyggi.tree.edits import NodeDeletion, NodeInsertion, NodeReplacement 

class MultilineStatementDeletion(NodeDeletion):
    NODE_TYPE = "multiline_stmt"