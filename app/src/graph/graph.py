from utils.outputs import ResponseAgentOrch, ResponseAgentSpec, ResponseAgentConsolidator
from agents.global_agent.prompt import SYSTEM_PROMPT_ORCH
from agents.specialist_agent.prompt import SYSTEM_PROMPT_SPEC
from agents.consolidator_agent.prompt import SYSTEM_PROMPT_CONS
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from utils.agent_state import AgentState
from utils.routes import AgentName, AgentNameList
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

import logging
import time

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

class AppAgent:
    def __init__(self, llm):
        self.dict_latency = {}
        self.llm = llm

    def start_graph_config(self, state: AgentState):

        logger.info("Starting graph configuration.")

        return {
            "specialist_selected": [],
            "latency": "__RESET__",
            "reasoning": [],
            "refining_question": "",
            "response_agent_spec": "__RESET__",
            "answers_final": "",
        }

    # NODES
    def agent_orchestrator(self, state:AgentState):

        logger.info("Executando orquestrador")

        start = time.monotonic()
        # Define the structured output for the orchestrator agent
        structured_llm = self.llm.with_structured_output(ResponseAgentOrch)

        # Invoke the LLM with the system prompt and a sample user message
        response = structured_llm.invoke([
            SystemMessage(content=SYSTEM_PROMPT_ORCH),
            HumanMessage(content=state.question_user),
        ])
        end = time.monotonic()

        latency = int((end - start)*1000)

        logger.info("Orchestrator sucessfully.")

        self.dict_latency.update({"agent_orchestrator": latency})

        return {"specialist_selected": response.selected_specialist,
                "reasoning": response.reasoning,
                "refining_question": response.refining_question,
                "latency": [{"agent_orchestrator": latency}]}

    def create_specialist_agent(self,agent_name: AgentName):

        def agent_specialist(state: AgentState):

            nome_assunto = AgentName(agent_name).name

            logger.info(
                "Executando especialista: %s",
                nome_assunto
            )

            start = time.monotonic()

            structured_llm = self.llm.with_structured_output(ResponseAgentSpec)

            system_prompt = SYSTEM_PROMPT_SPEC.format(
                nome_assunto=nome_assunto
            )

            response = structured_llm.invoke([
                                        SystemMessage(content=system_prompt),
                                        *state.messages,
                                    ])

            end = time.monotonic()

            latency = int((end - start)*1000)

            logger.info(f"Specialist {nome_assunto} successfully")

            self.dict_latency.update({f"agent_{agent_name.value}": latency})

            return {"response_agent_spec" : [{
                "agent_spec": agent_name.value, 
                "answers_specialist": response.answers_specialist,
                "kbs_selected": response.kbs_selected,
            }], "latency": [{"agent_{agent_name.value}": latency}]}

        return agent_specialist

    def agent_consolidator(self, state:AgentState):

        start = time.monotonic()
        structured_llm = self.llm.with_structured_output(ResponseAgentConsolidator)
        
        response_agent_spec = state.response_agent_spec
        
        answers_specialist = [spec["answers_specialist"][0] for spec in response_agent_spec]
        answers_specialist = "\n\n".join(answers_specialist)
        response = structured_llm.invoke([
            SystemMessage(content=SYSTEM_PROMPT_CONS),
            HumanMessage(content=state.refining_question),
            AIMessage(content=answers_specialist),
        ])
        logger.info("Consolidator successfully.")

        end = time.monotonic()
        latency = int((end - start)*1000)

        return {
                "answers_final": response.answers_final, 
                "latency": [{"agent_consolidator": latency}],
                "messages": [
                    AIMessage(content=response.answers_final)
                ]
        }
    # EDGES
    def conditional_edge(self, state: AgentState) -> list[str]:
        """Retorna dinamicamente os agentes selecionados pelo orquestrador."""

        valid_agents = {agent.value for agent in AgentName}

        return [
            agent
            for agent in state.specialist_selected
            if agent in valid_agents
        ]

    def build_graph(self):

        
        graph = StateGraph(AgentState)
        graph.add_node("agent_orchestrator", self.agent_orchestrator)

        for agent in AgentName:
            graph.add_node(agent.value, self.create_specialist_agent(agent))

        graph.add_node("agent_consolidator", self.agent_consolidator)
        graph.add_node("start_graph_config", self.start_graph_config)

        graph.set_entry_point("start_graph_config")
        graph.add_edge("start_graph_config", "agent_orchestrator")
        graph.add_conditional_edges(
            "agent_orchestrator",
            self.conditional_edge,
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

        checkpointer = InMemorySaver()
        graph = graph.compile(checkpointer=checkpointer)

        logger.info("Graph compiled successfully.")

        return graph
__all__ = ["AppAgent"]