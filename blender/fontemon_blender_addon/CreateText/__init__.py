from .CreateTextOperator import CreateTextOperator
from .CreateTextPanel import CreateTextPanel, CreateTextItemsPanel
from .EditTextOperator import EditTextOperator
from .EditTextPanel import EditTextPanel
from ..Plugin import MultiplePluginHolder

class CreateText(MultiplePluginHolder):
    plugins = (CreateTextOperator,
               CreateTextPanel,
               CreateTextItemsPanel,
               EditTextOperator,
               EditTextPanel,
               
               )
