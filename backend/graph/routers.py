from typing import Literal
from backend.graph.state import AgentState


def route_triage(state: AgentState) -> Literal["auto_resolver", "abrir_ticket", "pedir_info"]:
    decision = state.get("decision") or (state.get("triage").decision if state.get("triage") else None)

    if decision in ["AUTO_RESOLVER", "AUTO RESOLVER"]:
        return "auto_resolver"
    elif decision in ["PEDIR_INFO", "PEDIR INFO"]:
        return "pedir_info"
    elif decision in ["ABRIR_TIKECT", "ABRIR TIKECT", "ABRIR TICKET"]:
        return "abrir_ticket"

    return "abrir_ticket"


def route_auto_resolver(state: AgentState) -> Literal["__end__", "abrir_ticket", "pedir_info"]:
    if state.get("rag_success", False):
        return "__end__"

    final_action = state.get("final_action") or state.get("decision")
    if final_action == "PEDIR_INFO":
        return "pedir_info"

    return "abrir_ticket"