import os

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


def create_chat_model() -> ChatOpenAI:
    environment_path = ".env"
    load_dotenv(dotenv_path=environment_path)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY nao foi encontrada no arquivo .credentials")

    model_name = os.getenv("MODEL_NAME")
    if not model_name:
        raise ValueError("MODEL_NAME nao foi encontrado no arquivo .env")

    return ChatOpenAI(
        model=model_name,
        # api_key=api_key,
    )


llm = create_chat_model()

__all__ = ["ChatOpenAI"]