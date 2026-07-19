# Belief-Aware Agent Handoffs v0.1

**Status: CANDIDATE SPEC — NON-CANONICAL**

Issue: hummbl-dev/agent-handoffs#8
Parents:
- hummbl-dev/hummbl-dev#151 — Multi-Actor World Models v0.1
- hummbl-dev/hummbl-dev#149 — User-Driven World Model Generation v0.1

## Purpose

Define handoff semantics for transferring work among humans and agents without flattening local beliefs, uncertainty, dissent, authority, or provenance into one opaque context bundle.

A handoff must distinguish:

- accepted shared operational state
- sender-local belief or hypothesis
- user- or organization-ratified model state
- unresolved disagreement
- sources and evidence lineage
- delegated authority
- required next decision or observation
- what must not be durably admitted or executed

## Candidate packet sections

```text
handoff_id
sender_actor
sender_agent_version
receiver_actor
represented_principal
active_delegation
mission_and_scope
shared_operational_state
ratified_model_state
sender_local_beliefs
candidate_inferences
known_dissent
open_questions
source_and_independence_lineage
uncertainty_and_staleness
rejected_or_superseded_state
allowed_next_actions
forbidden_actions
required_approval
receipt_requirements
expiry_and_revalidation
```

## Required invariants

- A sender-local inference must not become receiver-accepted fact merely because it appears in a handoff.
- User or organizational ratification must remain attributable.
- Authority does not automatically transfer with context.
- A receiver must not inherit expired or revoked delegation.
- Dissent and unresolved contradiction must survive transfer.
- Source/model/provider correlation must survive transfer.
- Handoff compression must not erase claim posture or model version.

## Required events

Crosswalk with `hummbl-tuples` for:

- `HANDOFF_INITIATED`
- `STATE_ACCEPTED`
- `STATE_REJECTED`
- `BELIEF_FLAGGED`
- `DISSENT_PRESERVED`
- `AUTHORITY_TRANSFERRED`
- `AUTHORITY_EXPIRED`
- `REVALIDATION_REQUIRED`
- `HANDOFF_CLOSED`

## Required fixtures

### Valid fixtures

- valid simple handoff with shared state only
- valid handoff with sender-local belief explicitly flagged
- valid handoff preserving dissent between two agents
- valid handoff with expired delegation marked as expired
- valid handoff with authority transfer and receipt
- valid handoff with source lineage and uncertainty markers

### Invalid fixtures

- invalid handoff where sender inference appears as ratified fact
- invalid handoff where dissent is silently dropped
- invalid handoff where expired delegation is presented as active
- invalid handoff where authority transfers without explicit delegation
- invalid handoff where source lineage is erased by compression
- invalid handoff where claim posture is missing on load-bearing assertions

## Cross-repo dependencies

- `hummbl-tuples` — tuple event schema for handoff events
- `hummbl-dev/hummbl-dev#151` — multi-actor world models (parent)
- `hummbl-dev/hummbl-dev#149` — user-driven world model generation (parent)
- `agent-handoffs#9` — conversation/work-session handoff profile (sibling)

## Acceptance criteria

- [x] Handoff packet schema documented
- [x] 7 required invariants documented
- [x] 9 required events defined
- [x] 12 fixtures defined (6 valid, 6 invalid)
- [x] Cross-repo dependencies mapped
- [ ] JSON schema for packet sections
- [ ] Validator with deterministic checks
- [ ] Fixtures pass/fail as expected
- [ ] hummbl-tuples crosswalk validated
- [ ] Independent review completed

## Non-goals

- Replacing the conversation/work-session handoff profile (#9)
- Defining world model structure (parent issues own that)
- Creating a new tuple family (hummbl-tuples owns that)
- Flattening belief diversity into consensus
- Silencing dissent for transfer efficiency

## Fact posture

This is a coordination spec derived from issue #8. No claims about existing implementation. All packet sections are candidate until validated against fixtures and independent review.

## Receipt

- **Issue**: hummbl-dev/agent-handoffs#8
- **Packet sections**: 21
- **Required invariants**: 7
- **Required events**: 9
- **Fixtures**: 12 (6 valid, 6 invalid)
- **Cross-repo deps**: 4
- **Review status**: PENDING
