import os

from fastapi import BackgroundTasks, Depends, FastAPI

from app.dependencies.common import get_db_service, get_llm_service
from app.models.assignment import Assignment
from app.models.submission import Submission
from app.services.auth_service import AuthService
from app.services.db_service import DatabaseService
from app.services.llm_service import LLMService
from app.tasks import generate_and_upload_samples

app = FastAPI()
ENV = os.environ.get("ENV", "dev")

SUPABASE_JWT_SECRET = os.environ.get("SUPABASE_JWT_SECRET", "")


@app.get("/")
async def root():
    return {"message": "Hello World"}


# user_id: int, title: str, prompt: str, character_length: int,
@app.post("/user/{user_id}/assignments/")
async def create_assignment(
    user_id: str,
    new_assignment: Assignment,
    background_tasks: BackgroundTasks,
    db_service: DatabaseService = Depends(get_db_service),
    current_user=Depends(AuthService.get_current_user),
):
    # Takes into account the user_id who is creating the assignment
    # Store the assignment and generate 5 sample
    # responses, store them with assignment_id

    AuthService.authorize_user(current_user, user_id)

    print("user authorized")

    assignment_id = db_service.create_assignment(
        user_id, new_assignment.title, new_assignment.prompt, new_assignment.word_limit
    )

    print("assignment created")
    # now start the background task to generate and upload the sample responses

    background_tasks.add_task(
        generate_and_upload_samples,
        user_id,
        assignment_id,
        new_assignment.prompt,
        new_assignment.word_limit,
    )

    return {"assignment_id": assignment_id}


@app.post("/user/{user_id}/assignments/{assignment_id}/compare/")
async def compare_text(
    user_id: str,
    assignment_id: int,
    submission: Submission,
    db_service: DatabaseService = Depends(get_db_service),
    llm_service: LLMService = Depends(get_llm_service),
    current_user=Depends(AuthService.get_current_user),
):
    # Based on user_id, compare the text with stored sample responses and return similarity score
    AuthService.authorize_user(current_user, user_id)

    embedding = await llm_service.get_embedding(submission.text)

    result = await db_service.check_submission(user_id, assignment_id, embedding)

    return result
