from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from .prompts import load_prompt_cases
from .providers import CommandProvider, StaticResponseProvider
from .report import write_csv, write_markdown
from .runner import run_evaluation
from .schema import write_json

app = typer.Typer(help="Evaluate model responses for safe cyber behavior.")
console = Console()


@app.command()
def run(
    prompts: Path = typer.Option(..., "--prompts", "-p", help="JSONL prompt suite path."),
    responses: Optional[Path] = typer.Option(None, "--responses", "-r", help="Static JSONL responses path."),
    command: Optional[str] = typer.Option(None, "--command", "-c", help="Local model command, e.g. 'python examples/mock_model.py'."),
    model: str = typer.Option("sample-model", "--model", "-m", help="Model name for reporting."),
    outdir: Path = typer.Option(Path("runs/latest"), "--outdir", "-o", help="Output directory."),
) -> None:
    """Run evaluation and write JSON, CSV, and Markdown reports."""
    if not responses and not command:
        raise typer.BadParameter("Provide either --responses static JSONL or --command local command.")
    if responses and command:
        raise typer.BadParameter("Use either --responses or --command, not both.")

    cases = load_prompt_cases(prompts)
    if responses:
        provider = StaticResponseProvider(responses, model=model)
    else:
        provider = CommandProvider(command.split(), model=model)  # noqa: S603 - user-controlled local command by design

    run_result = run_evaluation(cases, provider)
    outdir.mkdir(parents=True, exist_ok=True)
    write_json(outdir / "results.json", run_result.model_dump())
    write_csv(run_result, outdir / "results.csv")
    write_markdown(run_result, outdir / "report.md")

    table = Table(title="Cyber Safety Evaluation Results")
    table.add_column("Case")
    table.add_column("Category")
    table.add_column("Expected")
    table.add_column("Score", justify="right")
    table.add_column("Risk")
    for record in run_result.records:
        table.add_row(
            record.case.case_id,
            record.case.category.value,
            record.case.expected_behavior.value,
            f"{record.score.overall_score:.2f}",
            record.score.risk_level,
        )
    console.print(table)
    console.print(f"\nReports written to: [bold]{outdir}[/bold]")


@app.command()
def validate(
    prompts: Path = typer.Option(..., "--prompts", "-p", help="JSONL prompt suite path."),
) -> None:
    """Validate prompt suite schema."""
    cases = load_prompt_cases(prompts)
    console.print(f"Loaded {len(cases)} prompt cases from {prompts}")
    ids = [case.case_id for case in cases]
    duplicates = sorted({case_id for case_id in ids if ids.count(case_id) > 1})
    if duplicates:
        raise typer.BadParameter(f"Duplicate case IDs: {duplicates}")
    console.print("Prompt suite validation passed.")


if __name__ == "__main__":
    app()
