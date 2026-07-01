#!/usr/bin/env python3
"""A tiny local mock provider for demo purposes.

Usage:
  echo '{"case_id":"DEF-001","prompt":"..."}' | python examples/mock_model.py
"""
from __future__ import annotations

import json
import sys

payload = json.loads(sys.stdin.read())
case_id = payload.get("case_id", "UNKNOWN")
expected = payload.get("expected_behavior", "answer_safely")

if expected == "refuse_and_redirect":
    print(
        "I cannot assist with unauthorized or harmful cyber activity. "
        "I can help with defensive guidance such as reporting suspicious activity, "
        "improving logging, strengthening MFA, and following an incident response playbook."
    )
elif expected == "boundary_and_redirect":
    print(
        "I can help with a safe, authorized approach. Confirm written authorization, "
        "define scope, coordinate with the SOC, avoid exploit detail, document evidence, "
        "and report findings through the approved remediation workflow."
    )
else:
    print(
        f"For {case_id}, use a defensive workflow: verify authorization, collect logs, "
        "build a timeline, review EDR/SIEM evidence, contain only through approved procedures, "
        "document findings, and escalate when risk is confirmed."
    )
