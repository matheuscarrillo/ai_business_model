import asyncio
from agents.global_agent.prompt import SYSTEM_PROMPT_ORCH
from langchain.messages import HumanMessage, AIMessage, SystemMessage
from graph.graph import AppAgent
from utils.connection import Connection
from utils.agent_state import AgentState
import warnings
warnings.filterwarnings("ignore")

import logging
import time 

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

async def main():
    start = time.monotonic()

    llm = Connection()

    logger.info("ChatOpenAI initialized successfully.")
    logger.info("Model Name: %s", llm.model_name)
    logger.info("Starting the graph execution.")

    graph = AppAgent(llm=llm)
    config_memory = {"configurable": {"thread_id": "usuario1"}}
    graph = graph.build_graph()
    while True:
        question = input("Digite sua pergunta: ")
        result = await graph.ainvoke(
                            {
                                "messages": [
                                    HumanMessage(content=question)
                                ],
                                "question_user": question
                            },
                            config=config_memory
                        )

        end = time.monotonic()
        latency = int((end - start)*1000)
        logger.info(f"Final Answer: {result['answers_final']}, Latency: {latency}ms")
        logger.info(f"Final Answer (JSON): {result}")

        state = graph.get_state(config_memory)

        print("\n========== CHECKPOINT ==========")

        for msg in state.values.get("messages", []):
            print(
                f"{type(msg).__name__}: {msg.content}"
            )

        print("================================\n")

if __name__ == "__main__":
    asyncio.run(main())