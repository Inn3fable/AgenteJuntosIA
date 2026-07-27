from backend.graph.nodes import AgentNodes



class FakeTriage:


    def analyze(self,q):

        return "AUTO"



class FakeRAG:


    def ask(self,q):

        return {

            "answer":"respuesta",

            "citations":[],

            "success":True
        }




def test_auto_resolver():


    nodes = AgentNodes(
        FakeTriage(),
        FakeRAG()
    )


    result = nodes.auto_resolver(
        {
            "question":"test"
        }
    )


    assert result["answer"]=="respuesta"

    assert result["rag_success"] is True