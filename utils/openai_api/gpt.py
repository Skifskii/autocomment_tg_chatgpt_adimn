import openai


async def request_to_gpt(request: dict) -> tuple[str, int]:
    response = await openai.ChatCompletion.acreate(
        model='gpt-3.5-turbo',
        messages=request
    )
    return response['choices'][0]['message']['content'], response['usage']['total_tokens']
