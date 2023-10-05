import asyncio
import os
from abc import ABC, abstractmethod
from typing import List

import aiohttp
import numpy as np


class LLMService(ABC):
    @abstractmethod
    async def generate_samples(
        self, prompt: str, word_limit: int, n: int = 1
    ) -> List[str]:
        pass

    @abstractmethod
    async def get_embedding(self, text: str) -> np.ndarray:
        pass


class MockLLMService(LLMService):
    async def generate_samples(self, prompt: str, word_limit: int, n=1) -> List[str]:
        return ["This is a sample response." for _ in range(n)]

    async def get_embedding(self, text: str) -> np.ndarray:
        return np.random.randn(1536)


class OpenAILLMService(LLMService):
    async def generate_samples(
        self, prompt: str, word_limit: int, n: int = 1
    ) -> List[str]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}",
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": prompt},
            ],
            "n": n,
            "temperature": 1.5,
        }

        url = "https://api.openai.com/v1/chat/completions"

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 429:
                    await asyncio.sleep(2)
                    return await self.generate_samples(prompt, word_limit, n)
                response_data = await response.json()

        samples = [s["message"]["content"].strip().replace("\n", " ") for s in response_data["choices"]]  # type: ignore
        return samples

    async def get_embedding(self, text: str) -> np.ndarray:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}",
        }

        data = {"input": text, "model": "text-embedding-ada-002"}

        url = "https://api.openai.com/v1/embeddings"

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 429:
                    await asyncio.sleep(2)
                    return await self.get_embedding(text)
                response_data = await response.json()

        embedding = np.array(response_data["data"][0]["embedding"])

        return embedding
