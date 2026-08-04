import asyncio
import json
import os

import httpx

from app.config import GOOGLE_API_KEY
from .prompt import (
    CLAUSE_EXTRACTION_PROMPT,
    CONTRACT_SUMMARY_PROMPT,
    RISK_ANALYSIS_PROMPT,
)

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"


def _clean_response(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else ""
        cleaned = cleaned.rsplit("```", 1)[0]
    return cleaned


async def _call_gemini(prompt: str) -> dict:
    payload = {
        "model": GEMINI_MODEL,
        "input": prompt,
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GOOGLE_API_KEY,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(GEMINI_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Gemini API error {response.status_code}: {response.text}")

    response_json = response.json()

    try:
        text = next(
            step["content"][0]["text"]
            for step in response_json["steps"]
            if step["type"] == "model_output"
        )
    except (KeyError, IndexError, StopIteration):
        raise Exception(f"Unexpected Gemini response: {response_json}")

    return json.loads(_clean_response(text))


async def extract_clauses(text_content: str) -> dict:
    prompt = CLAUSE_EXTRACTION_PROMPT.replace("{contract_text}", text_content)
    return await _call_gemini(prompt)


async def analyze_risks(text_content: str) -> dict:
    prompt = RISK_ANALYSIS_PROMPT.replace("{contract_text}", text_content)
    return await _call_gemini(prompt)


async def summarize(text_content: str) -> dict:
    prompt = CONTRACT_SUMMARY_PROMPT.replace("{contract_text}", text_content)
    return await _call_gemini(prompt)


async def analyze_contract(contract_id: str, text_content: str) -> dict:
    clauses, risks, summary = await asyncio.gather(
        extract_clauses(text_content),
        analyze_risks(text_content),
        summarize(text_content),
    )

    return {
        "contract_id": contract_id,
        "clause_analysis": clauses,
        "risk_analysis": risks,
        "summary": summary,
    }
