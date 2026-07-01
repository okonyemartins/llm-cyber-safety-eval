from __future__ import annotations

from pathlib import Path

from .schema import PromptCase, load_jsonl


def load_prompt_cases(path: str | Path) -> list[PromptCase]:
    return [PromptCase.model_validate(row) for row in load_jsonl(path)]


def prompt_case_by_id(cases: list[PromptCase]) -> dict[str, PromptCase]:
    return {case.case_id: case for case in cases}
