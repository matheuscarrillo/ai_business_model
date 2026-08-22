from utils.outputs import ResponseAgentOrch, ResponseAgentSpec, ResponseAgentConsolidator
from agents.global_agent.prompt import SYSTEM_PROMPT_ORCH
from agents.specialist_agent.prompt import SYSTEM_PROMPT_SPEC
from agents.consolidator_agent.prompt import SYSTEM_PROMPT_CONS
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from utils.agent_state import AgentState
from utils.routes import AgentName, AgentNameList
from utils.connection import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START, END

import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


llm = ChatOpenAI()


# NODES
def agent_orchestrator(state:AgentState):

    # Define the structured output for the orchestrator agent
    structured_llm = llm.with_structured_output(ResponseAgentOrch)

    # Invoke the LLM with the system prompt and a sample user message
    ai_msg = structured_llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT_ORCH),
        HumanMessage(content=state.question_user),
    ])

    response = ai_msg
    logger.info("Orchestrator sucessfully.")

    return {"specialist_selected": response.selected_specialist,
            "reasoning": response.reasoning,
            "refining_question": response.refining_question}

def create_specialist_agent(agent_name: AgentName):

    def agent_specialist(state: AgentState):

        nome_assunto = AgentName(agent_name).name

        logger.info(
            "Executando especialista: %s",
            nome_assunto
        )

        structured_llm = llm.with_structured_output(ResponseAgentSpec)

        system_prompt = SYSTEM_PROMPT_SPEC.format(
            nome_assunto=nome_assunto
        )

        response = structured_llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=state.refining_question),
        ])

        logger.info(f"Specialist {nome_assunto} successfully")

        return {"response_agent_spec" : [{
            "agent_spec": agent_name, 
            "answers_specialist": response.answers_specialist,
            "kbs_selected": response.kbs_selected,
        }]}

    return agent_specialist

def agent_consolidator(state:AgentState):

    structured_llm = llm.with_structured_output(ResponseAgentConsolidator)
    
    response_agent_spec = state.response_agent_spec
    
    answers_specialist = [spec["answers_specialist"][0] for spec in response_agent_spec]
    answers_specialist = "\n\n".join(answers_specialist)
    response = structured_llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT_CONS),
        HumanMessage(content=answers_specialist),
    ])
    logger.info("Consolidator successfully.")

    return {"answers_final": response.answers_final}

# EDGES
def conditional_edge(state: AgentState) -> list[str]:
    """Retorna dinamicamente os agentes selecionados pelo orquestrador."""

    valid_agents = {agent.value for agent in AgentName}

    return [
        agent
        for agent in state.specialist_selected
        if agent in valid_agents
    ]

def run_agents():

    graph = StateGraph(AgentState)
    graph.add_node("agent_orchestrator", agent_orchestrator)

    for agent in AgentName:
        graph.add_node(agent.value, create_specialist_agent(agent))

    graph.add_node("agent_consolidator", agent_consolidator)


    graph.add_edge(START, "agent_orchestrator")
    graph.add_conditional_edges(
        "agent_orchestrator",
        conditional_edge,
        {
            agent.value: agent.value
            for agent in AgentName
        }
    )

    for agent in AgentName:
        graph.add_edge(
            agent.value,
            "agent_consolidator"
        )

    graph.add_edge("agent_consolidator", END)
    
    graph = graph.compile()

    logger.info("Graph compiled successfully.")

    return graph
__all__ = ["run_agents"]