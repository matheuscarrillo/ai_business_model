from utils.connection import ChatOpenAI
from utils.outputs import ResponseAgentOrch, ResponseAgentSpec, ResponseAgentConsolidator
from agents.global_agent.prompt import SYSTEM_PROMPT_ORCH
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from graph.graph import run_agents
import warnings
warnings.filterwarnings("ignore")

import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

graph = run_agents()
result = graph.invoke({"question_user": "Qual é o tipo de placa solar mais eficiente e qual controlador de carga devo usar para um sistema de energia solar residencial?"})
logger.info(result["answers_final"])