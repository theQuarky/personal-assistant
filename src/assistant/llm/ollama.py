from __future__ import annotations

import os
from datetime import datetime
from typing import Any

import httpx


class OllamaClient:
    def __init__(self, base_url: str | None = None, model: str | None = None):
        self.base_url = (base_url or os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")).rstrip("/")
        self.model = model or os.getenv("ASSISTANT_MODEL", "qwen3:8b")

    async def chat(self, messages: list[dict[str, str]], tools: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"model": self.model, "messages": messages, "stream": False}
        if tools:
            payload["tools"] = tools
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(f"{self.base_url}/api/chat", json=payload)
            response.raise_for_status()
            return response.json()

    async def embed(self, text: str, model: str = "nomic-embed-text") -> list[float]:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                f"{self.base_url}/api/embed",
                json={"model": model, "input": text},
            )
            response.raise_for_status()
            return response.json()["embeddings"][0]
