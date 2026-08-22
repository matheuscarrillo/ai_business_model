import os

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

import logging
import time

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


def Connection():
    environment_path = ".env"
    load_dotenv(dotenv_path=environment_path)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY nao foi encontrada no arquivo .credentials")

    model_name = os.getenv("MODEL_NAME")
    if not model_name:
        raise ValueError("MODEL_NAME nao foi encontrado no arquivo .env")

    logger.info("Model Name Enviroment Variable: %s", model_name)
    return ChatOpenAI(
        model=model_name,
        # api_key=api_key,
    )

__all__ = ["Connection"]