from backend.graph.state import AgentState


def test_agent_state():

    state: AgentState = {

        "question":"¿Cómo actualizar información?",

        "triage":None,

        "answer":None,

        "citations":[],

        "rag_success":False,

        "final_action":None
    }


    assert state["question"] == "¿Cómo actualizar información?"

    assert state["rag_success"] is False