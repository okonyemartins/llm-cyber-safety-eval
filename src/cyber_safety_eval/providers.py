from __future__ import annotations

import json
import subprocess
import time
from abc import ABC, abstractmethod
from pathlib import Path

from .schema import ModelResponse, PromptCase, load_jsonl


class ModelProvider(ABC):
    """Minimal provider interface.

    This project intentionally keeps providers simple and safe. You can evaluate:
    1. A static JSONL file of model responses.
    2. A local command wrapper that you control.

    For API integrations, add a provider subclass in your own environment and keep
    secrets in environment variables, never in source code.
    """

    name: str = "base"
    model: str = "unknown"

    @abstractmethod
    def complete(self, case: PromptCase) -> ModelResponse:
        raise NotImplementedError


class StaticResponseProvider(ModelProvider):
    """Loads already-generated responses from JSONL for offline scoring."""

    name = "static_jsonl"

    def __init__(self, response_path: str | Path, model: str = "sample-model") -> None:
        self.model = model
        rows = load_jsonl(response_path)
        self.responses = {row["case_id"].strip().upper(): row for row in rows}

    def complete(self, case: PromptCase) -> ModelResponse:
        row = self.responses.get(case.case_id)
        if row is None:
            response_text = ""
        else:
            response_text = str(row.get("response_text", ""))
        return ModelResponse(
            case_id=case.case_id,
            response_text=response_text,
            provider=self.name,
            model=self.model,
            raw=row or {},
        )


class CommandProvider(ModelProvider):
    """Runs a local command that returns a response on stdout.

    The prompt is passed on stdin as JSON:
    {"case_id": "DEF-001", "prompt": "...", "category": "..."}

    Example command:
      python examples/mock_model.py

    This lets you connect the framework to any model CLI without committing API
    keys or provider-specific logic.
    """

    name = "command"

    def __init__(self, command: list[str], model: str = "command-model", timeout_seconds: int = 90) -> None:
        if not command:
            raise ValueError("CommandProvider requires a non-empty command list")
        self.command = command
        self.model = model
        self.timeout_seconds = timeout_seconds

    def complete(self, case: PromptCase) -> ModelResponse:
        payload = json.dumps(
            {
                "case_id": case.case_id,
                "prompt": case.prompt,
                "category": case.category.value,
                "expected_behavior": case.expected_behavior.value,
            }
        )
        started = time.perf_counter()
        proc = subprocess.run(
            self.command,
            input=payload,
            text=True,
            capture_output=True,
            timeout=self.timeout_seconds,
            check=False,
        )
        latency_ms = (time.perf_counter() - started) * 1000
        response_text = proc.stdout.strip()
        raw = {"returncode": proc.returncode, "stderr": proc.stderr.strip()}
        return ModelResponse(
            case_id=case.case_id,
            response_text=response_text,
            provider=self.name,
            model=self.model,
            latency_ms=latency_ms,
            raw=raw,
        )
