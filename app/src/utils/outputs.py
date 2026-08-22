from operator import add
from typing import Annotated, Literal, List
from pydantic import BaseModel, Field
from utils.routes import AgentName, AgentNameList



class ResponseAgentOrch(BaseModel):
    selected_specialist: List[AgentNameList] = Field(
        description="Lista de especialistas selecionados pelo agente global.",
        )

    reasoning: List[str] = Field(
        description=(
        "Explicacao, na mesma posicao do especialista, sobre o motivo da selecao de cada especialista."
        ),
    )

    refining_question: str = Field(
        description="Pergunta do usuário refinada para enviar ao especialista.",
    )


class ResponseAgentSpec(BaseModel):

    answers_specialist: List[str] = Field(
        description=(
            "Resposta do especialista"
        ),
    )

    kbs_selected: List[str] = Field(
        description=(
            "Bases de conhecimento selecionadas pelo especialista."
        ),
    )

class ResponseAgentConsolidator(BaseModel):
    answers_final: str = Field(
        description="Resposta final do agente parecerista, baseada nas respostas dos especialistas.",
    )