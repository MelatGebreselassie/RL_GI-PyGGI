from pyggi.tree.edits import NodeDeletion, NodeInsertion, NodeReplacement 
class MultilineStatementReplacement(NodeReplacement):
    NODE_TYPE = "multiline_stmt"