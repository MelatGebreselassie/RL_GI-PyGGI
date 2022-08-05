from .. import config as pyggi_config

from .abstract_engine import AbstractTreeEngine
if pyggi_config.enable_astor:
    from .astor_engine import AstorEngine
from .xml_engine import XmlEngine
from .srcml_engine import SrcmlEngine
from .program import TreeProgram
# from .edits import MultilineStatementDeletion, MultilineStatementInsertion, MultilineStatementReplacement
from .edits import StmtReplacement, StmtInsertion, StmtDeletion, StmtMoving
from .edits import TextSetting, TextWrapping
from .edits import ComparisonOperatorSetting, ArithmeticOperatorSetting
from .edits import NumericSetting, RelativeNumericSetting
from .edits import NodeDeletion, NodeInsertion, NodeReplacement 