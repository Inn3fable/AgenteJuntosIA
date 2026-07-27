from langgraph.graph import StateGraph, END, START
from backend.graph.nodes import GraphNodes
from backend.graph.routers import route_triage, route_auto_resolver
from backend.graph.state import AgentState


def build_workflow(graph_nodes: GraphNodes):
    workflow = StateGraph(AgentState)

    workflow.add_node("triaje", graph_nodes.triaje_node)
    workflow.add_node("auto_resolver", graph_nodes.auto_resolver_node)
    workflow.add_node("abrir_ticket", graph_nodes.abrir_ticket_node)
    workflow.add_node("pedir_info", graph_nodes.pedir_info_node)

    workflow.add_edge(START, "triaje")

    workflow.add_conditional_edges(
        "triaje",
        route_triage,
        {
            "auto_resolver": "auto_resolver",
            "abrir_ticket": "abrir_ticket",
            "pedir_info": "pedir_info"
        }
    )

    workflow.add_conditional_edges(
        "auto_resolver",
        route_auto_resolver,
        {
            "__end__": END,
            "abrir_ticket": "abrir_ticket",
            "pedir_info": "pedir_info"
        }
    )

    workflow.add_edge("abrir_ticket", END)
    workflow.add_edge("pedir_info", END)

    return workflow.compile()