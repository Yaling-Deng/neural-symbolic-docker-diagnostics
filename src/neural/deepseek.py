import json
import os

from openai import OpenAI

from src.models.semantic import SemanticFacts


SYSTEM_PROMPT = """
You are a semantic parser for Docker troubleshooting.

Your task is to extract factual information from a user's
natural-language description of a Docker or containerized
application problem.

Do NOT diagnose the problem.
Do NOT infer causes that are not explicitly stated.

Return the extracted information as JSON.

The JSON must have exactly these top-level fields:

{
  "applications": [],
  "services": [],
  "connections": [],
  "listeners": []
}

Applications represent applications or application processes
that initiate connections.

Services represent backend services such as postgres, redis,
mysql, nginx, etc.

Do NOT classify an application as a service unless the text
explicitly identifies it as a service.

Each application must have:
{
  "name": "application name"
}

Each service must have:
{
  "name": "service name"
}

Each connection must have:
{
  "source": "source application",
  "target": "target service",
  "requested_port": 1234
}

Use null for requested_port if it is not stated.

Each listener must have:
{
  "service": "service name",
  "port": 1234
}

Only extract facts that are supported by the user's description.
"""


def parse_with_deepseek(text: str) -> SemanticFacts:
    api_key = os.environ.get("DEEPSEEK_API_KEY")

    if not api_key:
        raise RuntimeError(
            "DEEPSEEK_API_KEY environment variable is not set."
        )

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )

    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": text,
            },
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError("DeepSeek returned an empty response.")

    data = json.loads(content)

    return SemanticFacts.model_validate(data)