import os
from abc import ABC, abstractmethod
from typing import Dict, List

import numpy as np
from dotenv import load_dotenv
from supabase_py import Client, create_client


# this is designed with user-awareness in mind. We assume we know who the user is
# But we don't assume that the user is authorized to do anything
class DatabaseService(ABC):
    @abstractmethod
    def create_assignment(
        self, user_id: str, title: str, prompt: str, word_limit: int
    ) -> int:
        """
        Save an assignment associated with a user.

        Args:
            user_id (str): ID of the user creating the assignment.
            title (str): Title of the assignment.
            prompt (str): Assignment prompt.
            word_limit (int): Word limit for the assignment.

        Returns:
            int: The ID of the saved assignment.
        """
        pass

    @abstractmethod
    def get_assignment(self, user_id: str, assignment_id: int) -> Dict:
        """
        Fetch an assignment based on user_id and assignment_id.

        Args:
            user_id (str): ID of the user.
            assignment_id (int): ID of the assignment to fetch.

        Returns:
            Dict: The metadata of the fetched assignment.
        """
        pass

    @abstractmethod
    def save_sample_response(
        self,
        user_id: str,
        assignment_id: int,
        response_text: str,
        embedding: np.ndarray,
    ) -> int:
        """
        Save a sample response for a given assignment associated with a user.

        Args:
            user_id (str): ID of the user saving the response.
            assignment_id (int): ID of the assignment.
            response_text (str): Text of the response.
            embedding (np.ndarray): Embedding of the response text.

        Returns:
            int: ID of the saved sample response.
        """
        pass

    @abstractmethod
    def check_submission(
        self, user_id: str, assignment_id: int, embedding: np.ndarray
    ) -> List[Dict]:
        """
        Check a submission's similarity against sample responses.

        Args:
            user_id (str): ID of the user checking the submission.
            assignment_id (int): ID of the assignment for the submission.
            embedding (np.ndarray): Embedding of the submission text.

        Returns:
            List[Dict]: Top 3 similar sample responses.
        """
        pass


class MockDBService(DatabaseService):
    def __init__(self) -> None:
        super().__init__()

    def create_assignment(
        self, user_id: str, title: str, prompt: str, word_limit: int
    ) -> int:
        # returns assignment_id
        return 0

    def get_assignment(self, user_id: str, assignment_id: int) -> Dict:
        # returns the assignment metadata
        # and returns the embeddings of the sample responses

        return {
            "id": assignment_id,
            "created_at": "2021-08-15T18:00:00.000000Z",
            "user_id": user_id,
            "title": "Test Assignment",
            "prompt": "This is a test assignment",
            "word_limit": 100,
        }

    def save_sample_response(
        self,
        user_id: str,
        assignment_id: int,
        response_text: str,
        embedding: np.ndarray,
    ) -> int:
        # returns a sample_response)id
        return 0

    def check_submission(
        self, user_id: str, assignment_id: int, embedding: np.ndarray
    ) -> List[Dict]:
        # Checks if the submission is similar to the sample responses
        # returns the top 3 similar sample responses
        return []


class Supabase(DatabaseService):
    def __init__(self) -> None:
        super().__init__()
        load_dotenv()
        url: str = os.environ.get("SUPABASE_URL", "")
        key: str = os.environ.get("SUPABASE_KEY", "")
        if not url or not key:
            raise Exception("Supabase credentials not found")

        self.supabase: Client = create_client(url, key)

    def create_assignment(
        self, user_id: str, title: str, prompt: str, word_limit: int
    ) -> int:
        # TODO: Make sure that the user_id is valid

        if word_limit < 0:
            raise Exception("Word limit cannot be negative")
        elif word_limit > 1000:
            raise Exception("Word limit cannot be greater than 1000")

        response = (
            self.supabase.table("assignments")
            .insert(  # type: ignore
                {
                    "user_id": user_id,
                    "title": title,
                    "prompt": prompt,
                    "word_limit": word_limit,
                }
            )
            .execute()
        )

        if (
            "data" not in response
            or not response["data"]
            or not isinstance(response["data"], list)
        ):
            raise RuntimeError("Failed to create assignment record.")

        assignment_id = response["data"][0]["id"]

        if not assignment_id or not isinstance(assignment_id, int):
            raise RuntimeError("Invalid assignment_id returned from database.")

        return assignment_id

    def get_assignment(self, user_id: str, assignment_id: int) -> Dict:
        # returns the assignment metadata
        # and returns the embeddings of the sample responses

        response = (
            self.supabase.table("assignments")
            .select("*")  # type: ignore
            .eq("user_id", user_id)
            .eq("id", assignment_id)
            .single()
            .execute()
        )

        if "data" not in response or not response["data"]:
            raise RuntimeError(f"No assignment found with id: {assignment_id}")

        return response["data"]

    def save_sample_response(
        self,
        user_id: str,
        assignment_id: int,
        response_text: str,
        embedding: np.ndarray,
    ) -> int:
        # returns a sample_response)id

        try:
            self.get_assignment(user_id, assignment_id)
        except RuntimeError:
            raise RuntimeError(f"No assignment found with id: {assignment_id}")

        response = (
            self.supabase.table("responses")
            .insert(  # type: ignore
                {
                    "assignment_id": assignment_id,
                    "response_text": response_text,
                    "embedding": embedding.tolist(),  # Convert np.ndarray to list for database storage
                }
            )
            .execute()
        )

        if "data" not in response or not response["data"]:
            raise RuntimeError("Failed to save sample response.")

        sample_response_id = response["data"][0]["id"]

        if not sample_response_id or not isinstance(sample_response_id, int):
            raise RuntimeError("Invalid sample_response_id returned from database.")

        return sample_response_id

    def check_submission(
        self, user_id: str, assignment_id: int, embedding: np.ndarray
    ) -> List[dict]:
        # Checks if the submission is similar to the sample responses
        # returns the top 3 similar sample responses

        return []
