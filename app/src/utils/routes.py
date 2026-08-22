from enum import Enum
from typing import List, Literal
from pydantic import BaseModel

AgentNameList = Literal[
    "agente_placa_solar",
    "agente_controlador_carga",
    "agente_bateria",
    "agente_inversor",
]

class AgentName(str, Enum):

    agente_placa_solar = "agente_placa_solar"
    agente_controlador_carga = "agente_controlador_carga"
    agente_bateria = "agente_bateria"
    agente_inversor = "agente_inversor"

    def agents() -> List[str]:
        return [agent.value for agent in AgentName]

    @property
    def description(self) -> str:
        descriptions = {
            AgentName.agente_placa_solar: "Agente especializado em fornecer informações sobre placas solares, incluindo tipos, eficiência, instalação e manutenção.",
            AgentName.agente_controlador_carga: "Agente especializado em fornecer informações sobre controladores de carga, incluindo tipos, funcionamento, instalação e manutenção.",
            AgentName.agente_bateria: "Agente especializado em fornecer informações sobre baterias, incluindo tipos, capacidade, vida útil, instalação e manutenção.",
            AgentName.agente_inversor: "Agente especializado em fornecer informações sobre inversores, incluindo tipos, eficiência, instalação e manutenção.",
        }

        return descriptions[self]

    @property
    def assunto(self) -> str:
        assuntos = {
            AgentName.agente_placa_solar: "Placas Solares",
            AgentName.agente_controlador_carga: "Controladores de Carga",
            AgentName.agente_bateria: "Baterias",
            AgentName.agente_inversor: "Inversores",
        }

        return assuntos[self]