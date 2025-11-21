import os
from langsmith import Client
from app.config import settings

_client = None

def get_langsmith_client():
    global _client
    if _client is None:
        if not settings.langsmith_api_key:
            return None
        _client = Client(api_key=settings.langsmith_api_key)
    return _client

def log_run(name: str, inputs: dict, outputs: dict, metrics: dict = None):
    client = get_langsmith_client()
    if not client:
        return
    client.log_run(name=name, inputs=inputs, outputs=outputs, metrics=metrics or {})
