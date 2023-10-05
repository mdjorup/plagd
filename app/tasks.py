import asyncio

from app.dependencies.common import get_db_service, get_llm_service


async def generate_and_upload_samples(
    user_id: str, assignment_id: int, prompt: str, word_limit: int
):
    llm_service = get_llm_service()
    db_service = get_db_service()

    # clean up prompt
    prompt = prompt.strip().replace("\n", " ")
    # remove double spaces
    prompt = " ".join(prompt.split())

    samples = await llm_service.generate_samples(prompt, word_limit, 2)

    async def handle_sample(sample):
        embedding = await llm_service.get_embedding(sample)
        db_service.save_sample_response(user_id, assignment_id, sample, embedding)

    async with asyncio.TaskGroup() as tg:
        for sample in samples:
            tg.create_task(handle_sample(sample))
