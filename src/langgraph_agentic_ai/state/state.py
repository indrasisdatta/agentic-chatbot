

from typing import Annotated, List, TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    """
    Represents the structure of the state used in the graph
    """
    messages: Annotated[List, add_messages]