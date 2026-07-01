# LLM Cyber Safety Evaluation Framework

## Project Overview

This project evaluates whether AI assistants can remain useful for legitimate cybersecurity defense while refusing, redirecting, or setting safe boundaries around suspicious dual-use, jailbreak-style, and harmful cyber requests.

It is designed as an empirical AI-security evaluation framework for testing model behavior across:

- Defensive cybersecurity prompts
- Suspicious dual-use prompts
- Jailbreak attempts
- SOC investigation scenarios

The framework produces structured JSON, CSV, and Markdown reports that score model behavior across refusal quality, safe helpfulness, unsafe detail, boundary clarity, false positives, overall score, and risk level.

This project is intentionally defensive and does not include operational exploit instructions.

## Current Evaluation Results

Latest static sample run:

- Cases evaluated: 18
- Average overall score: 84.20/100
- Critical risk cases: 0
- High risk cases: 0
- Medium risk cases: 0
- Low risk cases: 18

These results are based on a transparent heuristic rubric and static sample responses. The framework is intended for portfolio demonstration and early empirical AI-security research iteration, not as a final safety benchmark.

## Why This Project Exists

AI assistants can be valuable to defenders. They can summarize incidents, help structure SOC investigations, improve documentation, and support governance workflows. However, similar capabilities can be misused for cyber abuse, social engineering, credential theft, evasion, malware development, or unauthorized access.

This project tests whether a model can remain helpful for legitimate cyber-defense requests while refusing or safely redirecting harmful or suspicious requests.

## Project Structure

```text
llm_cyber_safety_eval/
├── data/
│   └── prompt_suite.jsonl
├── docs/
│   ├── anthropic_fellows_project_pitch.md
│   ├── research_writeup.md
│   └── scoring_rubric.md
├── examples/
│   ├── mock_model.py
│   └── static_responses.jsonl
├── runs/
│   └── static-demo/
│       ├── report.md
│       ├── results.csv
│       └── results.json
├── src/cyber_safety_eval/
│   ├── cli.py
│   ├── prompts.py
│   ├── providers.py
│   ├── report.py
│   ├── runner.py
│   ├── schema.py
│   └── scorers.py
└── tests/
    └── test_scorers.py
    ```
    ## Install

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"