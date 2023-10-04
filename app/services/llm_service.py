from abc import ABC, abstractmethod

import numpy as np


class LLMService(ABC):
    @abstractmethod
    def generate_sample(self, assignment_id: int, prompt: str, word_limit: int) -> str:
        pass

    @abstractmethod
    def get_embedding(self, text: str) -> np.ndarray:
        pass


class MockLLMService(LLMService):
    def generate_sample(self, assignment_id: int, prompt: str, word_limit: int) -> str:
        return "This is a sample response."

    def get_embedding(self, text: str) -> np.ndarray:
        return np.random.randn(1536)
