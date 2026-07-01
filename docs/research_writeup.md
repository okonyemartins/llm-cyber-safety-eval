# LLM Cyber Safety Evaluation Framework: Research Write-Up

## 1. Project Purpose

This project evaluates whether AI assistants can remain useful for legitimate cybersecurity defense while safely refusing, redirecting, or setting boundaries around suspicious dual-use, jailbreak-style, and harmful cyber requests.

The goal is to create a transparent Python-based evaluation framework that tests model behavior across realistic but non-operational cybersecurity scenarios, including SOC investigations, defensive cyber guidance, suspicious dual-use prompts, and jailbreak attempts.

This project is intended as an early empirical AI-security research artifact. It focuses on measuring safety behavior, refusal quality, safe helpfulness, false positives, unsafe detail, boundary clarity, and overall risk level.

## 2. Research Motivation

Advanced AI systems are increasingly useful for cybersecurity operations, including alert triage, incident response, vulnerability management, identity review, and security awareness. However, the same systems may also be misused for cyber abuse, social engineering, credential theft, evasion, malware development, or unauthorized access.

A useful AI-security evaluation should test both sides of this problem:

1. Can the model provide helpful defensive guidance when the user has a legitimate security context?
2. Can the model refuse or redirect harmful requests without over-refusing safe cybersecurity work?

This project explores that balance through structured prompt cases and a transparent scoring rubric.

## 3. Prompt Categories

The prompt suite currently includes 50 cases across four categories:

### Defensive Cyber

These prompts ask for safe, authorized cybersecurity help, such as vulnerability remediation, MFA awareness, and endpoint security workflows.

Expected behavior: answer safely.

### SOC Investigation

These prompts simulate authorized security operations scenarios, including DLP alerts, privileged account review, OAuth consent investigation, and lost-device response.

Expected behavior: answer safely with practical defensive steps.

### Suspicious Dual-Use

These prompts involve requests that could be legitimate or harmful depending on context, such as password security review or AI-assisted external asset review.

Expected behavior: establish authorization, define scope, avoid harmful operational detail, and redirect to safe governance or defensive guidance.

### Jailbreak Attempts

These prompts attempt to override safety boundaries or request harmful cyber behavior, such as token theft or ransomware evasion.

Expected behavior: refuse and redirect to safe defensive information.

## 4. Scoring Method

The framework uses a transparent heuristic scoring rubric. Each response is evaluated across several dimensions:

- Refusal quality
- Safe helpfulness
- False positive risk
- Unsafe detail
- Boundary clarity
- Overall score
- Risk level

The framework generates JSON, CSV, and Markdown reports. The Markdown report provides a readable summary of case results and risk distribution.

## 5. Current Results

The current evaluation includes 50 test cases.

Summary from the latest static sample run:

- Cases evaluated: 50
- Average overall score: 75.24/100
- Critical risk cases: 0
- High risk cases: 0
- Medium risk cases: 2
- Low risk cases: 48
- No-risk cases: 0

These results suggest that the sample responses generally follow safe defensive behavior, provide useful guidance where appropriate, and avoid direct harmful cyber instructions. Two medium-risk cases were flagged by the heuristic scorer and should be reviewed manually as part of future calibration.

## 6. Key Findings

The strongest results appeared in defensive cyber and SOC investigation scenarios, where the sample responses provided clear, authorized, practical guidance.

Dual-use cases performed well when the response established authorization, scope, governance controls, and safe boundaries before offering guidance.

Jailbreak cases scored lower than the defensive cases, which is expected. These cases are intentionally more difficult because the model must refuse harmful requests while still providing a safe redirection.

## 7. Limitations

This project is an early-stage evaluation framework and should not be treated as a final safety benchmark.

Current limitations include:

- The prompt suite is small and should be expanded.
- The scoring system is heuristic rather than human-calibrated.
- The sample responses are static and do not yet compare multiple live models.
- The evaluation does not yet include inter-rater human labels.
- The risk scoring should be calibrated against expert cybersecurity and AI-safety reviewers.

## 8. Future Work

Planned improvements include:

1. Expand the prompt suite from 50 cases to 100+ cases.
2. Add human labels for refusal quality, safe helpfulness, unsafe detail, and boundary clarity.
3. Compare multiple model providers or model versions.
4. Add charts showing score distribution by category and risk level.
5. Add more realistic SOC scenarios involving SIEM triage, endpoint detection, phishing, identity risk, cloud security, and GRC controls.
6. Calibrate heuristic scoring against human annotations.
7. Add a research notebook for deeper analysis of false positives and false negatives.

## 9. Relevance to AI Security Research

This project sits at the intersection of cybersecurity operations and empirical AI safety. It focuses on evaluating whether AI systems can support legitimate defenders while resisting cyber misuse.

The framework is especially relevant to AI-security research areas such as:

- LLM cyber misuse evaluation
- Safe helpfulness in cybersecurity contexts
- Jailbreak resilience
- Dual-use boundary handling
- SOC investigation assistance
- AI-assisted cyber defense governance
- Model behavior evaluation under adversarial prompts

## 10. Conclusion

This project demonstrates a practical approach to evaluating cyber safety behavior in AI assistants. It provides a working Python framework, structured prompt suite, transparent scoring rubric, automated tests, and generated reports.

The next major step is to expand the dataset, add human labels, compare multiple models, and improve scoring calibration.