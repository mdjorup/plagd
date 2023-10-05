import re

import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray):
    cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
    return cos_sim


def word_limit_to_tokens(word_limit: int) -> int:
    return int(word_limit * 4 / 3)


def condense_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()
