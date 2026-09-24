import asyncio
import httpx
import logging
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langsmith import traceable
from app.config import Config
from app.retry import with_retry

logger = logging.getLogger(__name__)


class ResearchState(TypedDict):
    topic: str
    session_id: str
    session_history: list[dict]
    ltm_context: str
    search_results: list[str]
    summaries: list[str]
    report: str
    verified: bool
    error: str
    iterations: int


async def _tz_call(config: Config, function_name: str, message: str) -> str:
    return await with_retry(
        lambda: _tz_call_once(config, function_name, message),
        max_retries=config.llm_max_retries,
        delay=config.llm_retry_delay,
    )


async def _tz_call_once(config: Config, function_name: str, message: str) -> str:
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            f"{config.tensorzero_url}/inference",
            json={
                "function_name": function_name,
                "input": {"messages": [{"role": "user", "content": message}]},
            },
        )
        response.raise_for_status()
        return response.json()["content"][0]["text"]


class SearchAgent:
    """Finds key facts. Receives session history so it understands what the user has asked before."""

    def __init__(self, config: Config):
        self.config = config

    @traceable(run_type="tool", name="agent:search")
    async def run(self, topic: str, session_history: list[dict]) -> str:
        logger.info(f"SearchAgent: researching '{topic}'")

        history_ctx = ""
        if session_history:
            recent = session_history[-4:]  # last 4 truns for context
            history_ctx = "\n\nPrevious conversation context (use this to understand what the user already knows and what angle they care about):\n"
            history_ctx += "\n".join(
                f"{m['role'].upper()}: {m['content']}" for m in recent
            )

        return await _tz_call(
            self.config,
            "research_summarize",
            f"You are a research specialist. Find and list 5 key facts, recent developments, "
            f"and important details about: {topic}. Be thorough and specific."
            f"{history_ctx}",
        )


class SummarizeAgent:
    """Condenses raw search results into structured bullet points."""

    def __init__(self, config: Config):
        self.config = config

    @traceable(run_type="tool", name="agent:summarize")
    async def run(self, search_results: list[str]) -> str:
        logger.info("SummarizeAgent: condensing search results")
        combined = "\n\n".join(search_results)
        return await _tz_call(
            self.config,
            "research_summarize",
            f"Summarize these research findings into clear, structured bullet points:\n\n{combined}",
        )
