import os

from fastapi import Depends, FastAPI

from app.dependencies.common import get_db_service
from app.models.assignment import Assignment
from app.services.auth_service import AuthService
from app.services.db_service import DatabaseService

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

    return {"assignment_id": assignment_id}


@app.post("/user/{user_id}/assignments/{assignment_id}/compare/")
async def compare_text(user_id: int, assignment_id: int, text: str):
    # Based on user_id, compare the text with stored sample responses and return similarity score
    pass
