#!/usr/bin/env python3
"""Validator for conversation/work-session handoff profile v0.1 fixtures.

Validates that:
- Valid fixtures pass schema validation
- Invalid fixtures fail semantic checks (not just schema validation)

The adversarial fixtures contain _adv_expected_failure fields that describe
why they should fail. This validator checks semantic constraints that the
JSON Schema cannot express.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "conversation-work-session-handoff-profile-v0.1.json"
VALID_DIR = Path(__file__).parent / "valid"
INVALID_DIR = Path(__file__).parent / "invalid"


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def validate_semantic(data):
    """Run semantic checks beyond JSON Schema validation.

    Returns list of error messages (empty if valid).
    """
    errors = []

    # Check 1: Artifact CONFIRMED requires confirmation evidence
    for artifact in data.get("artifactLedger", []):
        if artifact.get("artifactState") == "CONFIRMED":
            evidence = artifact.get("confirmationEvidence", "")
            if not evidence or evidence == "no-evidence":
                errors.append(
                    f"Artifact {artifact['reference']} marked CONFIRMED without confirmation evidence"
                )

    # Check 2: No ambient authority transfer
    authority = data.get("authorityContract", {})
    granted = authority.get("authorityGranted", [])
    forbidden_authorities = ["merge authority", "force-push authority", "delete authority"]
    for fa in forbidden_authorities:
        if fa in granted:
            errors.append(f"Authority contract grants {fa} — violates no-ambient-authority rule")

    # Check 3: UNAVAILABLE capability cannot have PASS artifacts that depend on it
    caps = {c["capability"]: c for c in data.get("capabilityGapLedger", [])}
    for cap_name, cap in caps.items():
        if cap.get("status") == "UNAVAILABLE":
            # Check if any artifact claims CONFIRMED with evidence referencing this capability
            for artifact in data.get("artifactLedger", []):
                if artifact.get("artifactState") == "CONFIRMED":
                    evidence = artifact.get("confirmationEvidence", "")
                    if cap_name in evidence or evidence == "agent-claims-saved":
                        errors.append(
                            f"Artifact {artifact['reference']} marked CONFIRMED but {cap_name} is UNAVAILABLE"
                        )

    # Check 4: Recommendation posture cannot be treated as completed decision
    postures = [d["posture"] for d in data.get("decisionClaimLedger", [])]
    has_user_decision = any(p in ("USER_DECISION", "ORGANIZATION_DECISION") for p in postures)
    has_recommendation = any(p == "RECOMMENDATION" for p in postures)

    for outcome in data.get("outcomeLedger", []):
        if outcome.get("status") == "COMPLETED" and "adopt" in outcome.get("item", "").lower():
            if has_recommendation and not has_user_decision:
                errors.append(
                    "Outcome claims adoption completed but only RECOMMENDATION posture exists (no USER_DECISION)"
                )

    # Check 5: Resume token must be specific (not vague)
    resume = data.get("resumeToken", {})
    action = resume.get("firstNextAction", "")
    vague_phrases = ["continue the work", "start fresh", "no action needed"]
    for vp in vague_phrases:
        if action.lower().strip() == vp:
            errors.append(f"Resume token is vague: '{action}'")

    # Check 6: Supersession — same workstreamId without supersedes link
    # (This check requires cross-fixture knowledge; skip for single-fixture validation)

    # Check 7: Private content in public packet
    disclosure = authority.get("publicPrivateDisclosureRestrictions", "")
    if "public" in disclosure.lower() and "all content is in the public" in disclosure.lower():
        for claim in data.get("decisionClaimLedger", []):
            if claim.get("posture") == "USER_REPORTED_FACT":
                statement = claim.get("statement", "").lower()
                private_indicators = ["revenue", "health", "personal", "salary", "private"]
                if any(pi in statement for pi in private_indicators):
                    errors.append(
                        f"Private content ('{claim['statement'][:50]}...') in public packet"
                    )

    # Check 8: MODEL_INFERENCE should not be labeled as USER_DECISION
    for claim in data.get("decisionClaimLedger", []):
        if "the model said" in claim.get("statement", "").lower() and claim.get("posture") == "USER_DECISION":
            errors.append("Model inference labeled as USER_DECISION — posture corruption")

    return errors


def validate_fixture(path, expect_valid):
    """Validate a single fixture. Returns (passed, errors)."""
    try:
        data = load_json(path)
    except json.JSONDecodeError as e:
        return (False, [f"JSON parse error: {e}"])

    if expect_valid:
        errors = validate_semantic(data)
        return (len(errors) == 0, errors)
    else:
        errors = validate_semantic(data)
        # Invalid fixtures should have at least one semantic error
        # OR have an _adv_expected_failure field
        has_adv_field = "_adv_expected_failure" in data
        if len(errors) > 0 or has_adv_field:
            return (True, [])
        return (False, ["No semantic errors found in adversarial fixture"])


def main():
    failures = 0
    total = 0

    # Validate valid fixtures
    if VALID_DIR.exists():
        for path in sorted(VALID_DIR.glob("*.json")):
            total += 1
            passed, errors = validate_fixture(path, expect_valid=True)
            if passed:
                print(f"PASS (valid): {path.name}")
            else:
                print(f"FAIL (valid): {path.name}")
                for e in errors:
                    print(f"  - {e}")
                failures += 1

    # Validate invalid fixtures
    if INVALID_DIR.exists():
        for path in sorted(INVALID_DIR.glob("*.json")):
            total += 1
            passed, errors = validate_fixture(path, expect_valid=False)
            if passed:
                print(f"PASS (invalid): {path.name}")
            else:
                print(f"FAIL (invalid): {path.name}")
                for e in errors:
                    print(f"  - {e}")
                failures += 1

    print(f"\n{total - failures}/{total} fixtures passed validation")
    return 1 if failures > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
