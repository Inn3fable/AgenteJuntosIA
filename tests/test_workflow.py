from backend.graph.workflow import AgentWorkflow
from backend.graph.nodes import AgentNodes
from backend.graph.routers import AgentRouters



class FakeTriageService:


    def analyze(self, question):

        return {

            "decision":
            "AUTO_RESOLVER",

            "urgency":
            "BAJA",

            "missing_fields":
            []

        }



class FakeRAGService:


    def ask(self, question):

        return {

            "answer":
            "Respuesta encontrada",

            "citations":
            [],

            "success":
            True

        }



def create_workflow():

    nodes = AgentNodes(

        triage_service=
        FakeTriageService(),

        rag_service=
        FakeRAGService()

    )


    routers = AgentRouters()


    workflow = AgentWorkflow(

        nodes,

        routers

    )


    return workflow.build()



def test_auto_resolver():


    app = create_workflow()


    result = app.invoke(

        {

            "question":
            "¿Cuál es el procedimiento?"

        }

    )


    assert result["answer"] == "Respuesta encontrada"


    assert result["final_action"] == "auto_resolver_exitoso"