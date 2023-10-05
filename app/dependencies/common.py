import os

from dotenv import load_dotenv

from app.services.db_service import DatabaseService, MockDBService, Supabase
from app.services.llm_service import LLMService, MockLLMService, OpenAILLMService

load_dotenv()

DEV_MODE: bool = os.environ.get("ENV", "dev") == "dev"


def get_db_service() -> DatabaseService:
    if DEV_MODE:
        return MockDBService()
    return Supabase()


def get_llm_service() -> LLMService:
    if DEV_MODE:
        return MockLLMService()
    return OpenAILLMService()
