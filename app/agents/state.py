from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    messages: List[str]
    intent: Optional[str]
    name: Optional[str]
    email: Optional[str]
    platform: Optional[str]
    response: Optional[str]