from langgraph.graph import StateGraph  # type: ignore
from typing import TypedDict, Optional
from backend.agents import roadmap_node, tutorial_node, exercise_node, review_node

class AgentState(TypedDict):
    topic: str
    level: str
    user_id: int
    roadmap: Optional[str]
    tutorial: Optional[str]
    exercise: Optional[str]
    code: Optional[str]
    review: Optional[str]

def create_graph():
    builder = StateGraph(AgentState)
    builder.add_node("roadmap", roadmap_node)
    builder.add_node("tutorial", tutorial_node)
    builder.add_node("exercise", exercise_node)
    builder.add_node("review", review_node)
    builder.set_entry_point("roadmap")
    builder.add_edge("roadmap", "tutorial")
    builder.add_edge("tutorial", "exercise")
    builder.add_edge("exercise", "review")
    builder.set_finish_point("review")
    return builder.compile()
