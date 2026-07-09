# Context Transfer Worked Example

Status: candidate example. This file illustrates one complete context transfer between two agents and does not create canon.

## Scenario

Agent A has finished first-pass triage on a small documentation bug. Agent B is asked to resume the work, verify the proposed fix, and prepare a draft PR. The handoff packet makes the boundary explicit so Agent B does not need to infer authority or redo the whole investigation.

## Agent A Output

```text
Finding: README installation section references setup.py, but the repo uses pyproject.toml.
Evidence: README.md section "Install"; pyproject.toml exists at repo root.
Recommended action: replace setup.py wording with pip install -e . wording.
Out of scope: dependency upgrades, packaging metadata changes, release publication.
```

## Handoff Packet

```json
{
  "schemaVersion": "agent-handoffs/v0.1",
  "packetStatus": "issued",
  "handoffManifest": {
    "id": "handoff-docs-install-0001",
    "title": "Resume README installation wording fix",
    "version": "1",
    "scope": "single documentation correction"
  },
  "authority": {
    "issuer": "agent-a",
    "issuerType": "agent",
    "basis": "operator-approved documentation triage lane"
  },
  "handoffContract": {
    "fromAgent": {
      "id": "agent-a",
      "type": "agent",
      "name": "Triage Agent"
    },
    "toAgent": {
      "id": "agent-b",
      "type": "agent",
      "name": "Implementation Agent"
    },
    "contextEnvelope": {
      "objective": "Verify and correct README installation wording.",
      "inScope": [
        "Read README.md installation section",
        "Confirm pyproject.toml is present",
        "Prepare a minimal documentation patch"
      ],
      "outOfScope": [
        "Changing package metadata",
        "Changing dependencies",
        "Publishing a release"
      ],
      "constraints": [
        "Preserve non-canon repository posture",
        "Do not make private or internal claims"
      ],
      "priorContext": [
        {
          "ref": "README.md#install",
          "kind": "repo-file"
        },
        {
          "ref": "pyproject.toml",
          "kind": "repo-file"
        }
      ]
    },
    "delegationScope": {
      "grantedAuthority": [
        "read repository files",
        "prepare documentation patch",
        "open draft PR"
      ],
      "limits": [
        "no merge authority",
        "no package publication",
        "no repo setting changes"
      ]
    },
    "expiry": "2026-12-31T23:59:59Z",
    "receiptChain": [
      {
        "hop": 0,
        "actor": "agent-a",
        "action": "issued handoff packet",
        "at": "2026-07-06T00:00:00Z",
        "ref": "docs/context-transfer-worked-example.md"
      }
    ]
  },
  "receiptRequirements": {
    "acknowledgeBy": "2026-07-06T01:00:00Z",
    "produce": [
      "acknowledgement receipt",
      "minimal diff summary",
      "validation result",
      "draft PR link"
    ]
  }
}
```

## Agent B Resume Step

Agent B reads the packet and starts from the stated evidence instead of reconstructing the full task. If the evidence is stale or false, Agent B records that in the receipt and stops or narrows the patch.

```text
Acknowledgement: accepted handoff-docs-install-0001.
Verified: README.md still references setup.py; pyproject.toml is present.
Action: prepare README-only wording patch.
Validation: markdown-only change; no package behavior changed.
```

## Receipt

- Added a worked context-transfer example with Agent A output, Agent B resume behavior, and a JSON handoff packet.
- Kept the example candidate/non-canon.
- Did not modify operator-authority surfaces.
- Did not introduce new HUMMBL/BaseN terminology.
- Draft PR: https://github.com/example-org/example-repo/pull/42
