# tasks.py
from celery_app import celery_app

from app.dependencies.common import get_llm_service
from app.services.llm_service import (
    LLMService,
)  # Assuming llm_service.py defines LLMService


@celery_app.task
def generate_and_upload_samples(assignment_id, prompt, word_limit):
    llm_service: LLMService = get_llm_service()

    # Now use llm_service to generate and upload sample responses
