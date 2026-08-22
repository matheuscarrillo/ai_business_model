from operator import add
from typing import Annotated, List
from pydantic import BaseModel, Field
from utils.routes import AgentName, AgentNameList

class AgentState(BaseModel):
  question_user: str = Field(
    default="",
    description="Pergunta do usuario que sera respondida pelo agente global.",
    )
  
  specialist_selected: List[AgentNameList] = Field(
    default_factory=list,
    description="Lista de especialistas selecionados pelo agente global.",
  )

  reasoning: List[str] = Field(
    default_factory=list,
    description=(
      "Explicacao, na mesma posicao do especialista, sobre o motivo da selecao de cada especialista."
    ),
  )

  latency: Annotated[list[dict], add] = Field(
    default_factory=list,
    description=(
      "Lista de dicionarios contendo informacoes sobre a latencia de cada agente."
    )
  )

  refining_question: str = Field(
      default="",
        description="Pergunta refinada pelo agente global para o especialista.",
    )

  response_agent_spec: Annotated[list[dict], add] = Field(
      default_factory=list,
      description=(
        "Lista de respostas dos especialistas, na mesma posicao do especialista."
      ),
    )

  answers_final: str = Field(
        default="",
        description="Resposta final do agente parecerista, baseada nas respostas dos especialistas.",
    )