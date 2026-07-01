# Project Pitch: LLM Cyber Safety Evaluation Framework

## Working title
LLM Cyber Safety Evaluation Framework for Defensive Use, Dual-Use Boundaries, Jailbreak Resistance, and SOC Investigation Quality

## Research motivation
Advanced AI systems increasingly interact with cybersecurity workflows. The same model capabilities that help a SOC analyst triage alerts, summarize logs, or document incidents can also be misused for unauthorized access, social engineering, evasion, or harmful automation. This creates a practical safety challenge: models should remain helpful for legitimate defensive users while refusing or safely redirecting harmful requests.

## Research question
Can we build an empirical evaluation framework that measures whether AI systems appropriately distinguish between:

1. legitimate defensive cybersecurity requests;
2. suspicious dual-use requests that require boundaries and safe redirection;
3. explicit jailbreak or harmful cyber requests; and
4. SOC investigation scenarios where safe, practical help is valuable?

## Proposed method
The project creates a structured prompt suite, a response collection pipeline, and a transparent scoring rubric. Each prompt is labeled with expected behavior: answer safely, set boundaries and redirect, or refuse and redirect. Model responses are scored across refusal quality, safe helpfulness, false positives, unsafe detail, boundary clarity, overall score, and risk level.

## Safety design
The prompt suite intentionally avoids operational exploit instructions. It uses high-level adversarial and dual-use examples to evaluate model boundaries without teaching harmful procedures. Reports emphasize manual review, safe alternatives, and defensive remediation.

## Expected output
A public GitHub-ready research artifact containing:

- a Python evaluation framework;
- a safe seed prompt suite;
- an initial heuristic rubric;
- reproducible sample reports;
- a roadmap for human annotation and model comparison;
- a short paper-style writeup of findings.

## Why this aligns with AI Security Fellows
The project sits at the intersection of AI security, cyber misuse prevention, adversarial robustness, and practical model evaluation. It is designed to test whether models can help legitimate defenders without enabling harmful cyber activity.

## Candidate fit statement
My background in cybersecurity operations, endpoint security, incident response, GRC, Splunk, Microsoft Defender, Intune, Active Directory, ServiceNow, AI security experimentation, and Python gives me a practical foundation for evaluating AI behavior in realistic SOC and security-governance scenarios.
