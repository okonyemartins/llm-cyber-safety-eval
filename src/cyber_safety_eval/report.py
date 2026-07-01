from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean

from .schema import EvalRun, EvaluationRecord


def flatten_record(record: EvaluationRecord) -> dict[str, object]:
    return {
        "case_id": record.case.case_id,
        "category": record.case.category.value,
        "expected_behavior": record.case.expected_behavior.value,
        "authorized_context": record.case.authorized_context,
        "provider": record.model_response.provider,
        "model": record.model_response.model,
        "overall_score": record.score.overall_score,
        "risk_level": record.score.risk_level,
        "refusal_quality": record.score.refusal_quality,
        "safe_helpfulness": record.score.safe_helpfulness,
        "false_positive": record.score.false_positive,
        "unsafe_detail": record.score.unsafe_detail,
        "boundary_clarity": record.score.boundary_clarity,
        "findings": " | ".join(record.score.findings),
        "recommendations": " | ".join(record.score.recommendations),
        "prompt": record.case.prompt,
        "response_text": record.model_response.response_text,
    }


def write_csv(run: EvalRun, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [flatten_record(record) for record in run.records]
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(run: EvalRun, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    risk_counts = _risk_counts(run)
    avg_score = mean([record.score.overall_score for record in run.records]) if run.records else 0.0
    lines = [
        "# LLM Cyber Safety Evaluation Report",
        "",
        f"**Run ID:** `{run.run_id}`  ",
        f"**Created:** {run.created_at}  ",
        f"**Provider:** {run.provider}  ",
        f"**Model:** {run.model}  ",
        f"**Cases evaluated:** {len(run.records)}  ",
        f"**Average overall score:** {avg_score:.2f}/100  ",
        "",
        "## Risk Summary",
        "",
        "| Risk level | Count |",
        "|---|---:|",
    ]
    for level in ["critical", "high", "medium", "low", "none"]:
        lines.append(f"| {level} | {risk_counts.get(level, 0)} |")
    lines.extend([
        "",
        "## Case Results",
        "",
        "| Case | Category | Expected | Score | Risk | Key finding |",
        "|---|---|---|---:|---|---|",
    ])
    for record in run.records:
        finding = record.score.findings[0].replace("|", "\\|") if record.score.findings else ""
        lines.append(
            "| {case} | {category} | {expected} | {score:.2f} | {risk} | {finding} |".format(
                case=record.case.case_id,
                category=record.case.category.value,
                expected=record.case.expected_behavior.value,
                score=record.score.overall_score,
                risk=record.score.risk_level,
                finding=finding,
            )
        )
    lines.extend([
        "",
        "## Recommended Next Steps",
        "",
        "1. Review every medium, high, and critical risk case manually.",
        "2. Add human labels for refusal quality, safe helpfulness, and unsafe detail.",
        "3. Expand the prompt suite with more realistic but non-operational defensive SOC scenarios.",
        "4. Compare multiple models or model versions using the same prompt suite.",
        "5. Calibrate the heuristic scorer against human annotations before making strong claims.",
        "",
        "## Method Note",
        "",
        "This report uses a transparent heuristic rubric. It is designed for portfolio demonstration and early research iteration, not as a final safety benchmark.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _risk_counts(run: EvalRun) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in run.records:
        counts[record.score.risk_level] = counts.get(record.score.risk_level, 0) + 1
    return counts
