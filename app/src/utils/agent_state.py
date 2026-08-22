from pydantic import BaseModel, Field, Append


class AgentState(BaseModel) -> AgentState:
  question_user: str = Field(
    default="",
    description="Pergunta do usuario que sera respondida pelo agente global.",
    )
  
  specialist_selected: list[str] = Field(
    default_factory=list,
    description="Lista de especialistas selecionados pelo agente global.",
  )

  reasoning: list[str] = Field(
    default_factory=list,
    description=(
      "Explicacao, na mesma posicao do especialista, sobre o motivo da selecao."
    ),
  )

  latency: Append[list[dict]] = Field(
    default_factory=list,
    description=(
      "Lista de dicionarios contendo informacoes sobre a latencia de cada agente."
    ),

    refining_question: str = Field(
      default="",
        description="Pergunta refinada pelo agente global para o especialista.",
    )

    answers_specialist: Append[list[str]] = Field(
      default_factory=list,
      description=(
        "Lista de respostas dos especialistas, na mesma posicao do especialista."
      ),
    )

    kbs_selected: Append[list[dict]] = Field(
        default_factory=list,
        description=(
            "Lista de dicionarios contendo informacoes sobre as bases de conhecimento "
            "selecionadas pelo agente global."
        ),
    )

    answers_final: str = Field(
        default="",
        description="Resposta final do agente parecerista, baseada nas respostas dos especialistas.",
    )   
  
__all__ = ["AgentState"]