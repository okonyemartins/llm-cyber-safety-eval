from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from .providers import ModelProvider
from .schema import EvalRun, EvaluationRecord, PromptCase
from .scorers import CyberSafetyScorer


def run_evaluation(
    cases: list[PromptCase],
    provider: ModelProvider,
    scorer: CyberSafetyScorer | None = None,
) -> EvalRun:
    scorer = scorer or CyberSafetyScorer()
    records: list[EvaluationRecord] = []
    for case in cases:
        response = provider.complete(case)
        score = scorer.score(case, response)
        records.append(EvaluationRecord(case=case, model_response=response, score=score))
    return EvalRun(
        run_id=str(uuid4()),
        created_at=datetime.now(timezone.utc).isoformat(),
        provider=provider.name,
        model=provider.model,
        records=records,
    )
