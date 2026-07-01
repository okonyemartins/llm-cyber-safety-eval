from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


class CaseCategory(str, Enum):
    DEFENSIVE = "defensive_cyber"
    DUAL_USE = "suspicious_dual_use"
    JAILBREAK = "jailbreak_attempt"
    SOC = "soc_investigation"


class ExpectedBehavior(str, Enum):
    ANSWER_SAFELY = "answer_safely"
    BOUNDARY_AND_REDIRECT = "boundary_and_redirect"
    REFUSE_AND_REDIRECT = "refuse_and_redirect"


RiskLevel = Literal["none", "low", "medium", "high", "critical"]


class PromptCase(BaseModel):
    """A single evaluation prompt and its expected safe behavior."""

    case_id: str = Field(..., description="Stable case identifier, e.g. DEF-001")
    category: CaseCategory
    prompt: str
    expected_behavior: ExpectedBehavior
    authorized_context: bool = False
    risk_tags: list[str] = Field(default_factory=list)
    safe_reference_keywords: list[str] = Field(default_factory=list)
    unsafe_request_keywords: list[str] = Field(default_factory=list)
    notes: str | None = None

    @field_validator("case_id")
    @classmethod
    def normalize_case_id(cls, value: str) -> str:
        return value.strip().upper()


class ModelResponse(BaseModel):
    case_id: str
    response_text: str
    provider: str = "unknown"
    model: str = "unknown"
    latency_ms: float | None = None
    raw: dict[str, Any] = Field(default_factory=dict)

    @field_validator("case_id")
    @classmethod
    def normalize_case_id(cls, value: str) -> str:
        return value.strip().upper()


class ScoreBreakdown(BaseModel):
    refusal_quality: float = Field(ge=0, le=5)
    safe_helpfulness: float = Field(ge=0, le=5)
    false_positive: float = Field(ge=0, le=5)
    unsafe_detail: float = Field(ge=0, le=5)
    boundary_clarity: float = Field(ge=0, le=5)
    overall_score: float = Field(ge=0, le=100)
    risk_level: RiskLevel
    findings: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)


class EvaluationRecord(BaseModel):
    case: PromptCase
    model_response: ModelResponse
    score: ScoreBreakdown


class EvalRun(BaseModel):
    run_id: str
    created_at: str
    provider: str
    model: str
    records: list[EvaluationRecord]


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    import json

    rows: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            try:
                rows.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_no}: {exc}") from exc
    return rows


def write_json(path: str | Path, payload: Any) -> None:
    import json

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        f.write("\n")
