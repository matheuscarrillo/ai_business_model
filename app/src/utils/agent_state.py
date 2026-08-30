from operator import add
from typing import Annotated, List, Any
from pydantic import BaseModel, Field
from utils.routes import AgentName, AgentNameList
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


def append_or_reset(current: list[str], new: Any) -> list[str]:

  if new == "__RESET__":
      return []

  return current + new

class AgentState(BaseModel):
  question_user: str = Field(
     default_factory=str,
    description="Pergunta do usuario que sera respondida pelo agente global.",
    )

  messages: Annotated[List[BaseMessage], add_messages] = Field(default_factory=list)

  latency: Annotated[List[dict], append_or_reset] = Field(
     default_factory=list,
     description="Lista de latencias de cada agente",
  )
  
  specialist_selected: Annotated[List[AgentNameList], append_or_reset] = Field(
    default_factory=list,
    description="Lista de especialistas selecionados pelo agente global.",
  )

  reasoning: List[str] = Field(
    default_factory=list,
    description=(
      "Explicacao, na mesma posicao do especialista, sobre o motivo da selecao de cada especialista."
    ),
  )

  refining_question: str = Field(
    default_factory=str,
        description="Pergunta refinada pelo agente global para o especialista.",
    )

  response_agent_spec: Annotated[list[dict], append_or_reset] = Field(
    default_factory=list,
    description=(
        "Lista de respostas dos especialistas, na mesma posicao do especialista."
      ),
    )

  answers_final: str = Field(
    default_factory=str,
        description="Resposta final do agente parecerista, baseada nas respostas dos especialistas.",
    )