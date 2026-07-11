# Conversation/Work-Session Handoff Profile v0.1

**Status: CANDIDATE — NON-CANON — ADDITIVE PROFILE**

Issue: hummbl-dev/agent-handoffs#9
Parent: hummbl-dev/hummbl-dev#159

## Mission

Define a reusable handoff profile for ChatGPT chats and connected work sessions so another human or agent can resume without replaying the full transcript. The profile preserves claim posture, provenance, constraints, and open work while preventing implicit transfer of authority or private context.

## Schema compatibility decision

**Decision: Additive profile schema referencing v0.1.**

The existing `agent-handoffs-v0.1` schema centers `fromAgent`/`toAgent` and a `contextEnvelope` with objective/scope/constraints. The conversation/work-session profile requires additional structures (outcome ledger, decision/claim ledger, artifact ledger, open-work ledger, capability/gap ledger, authority contract, resume token) that would semantically overload the v0.1 fields.

Rather than silently broadening v0.1 or creating a separate runtime, this profile is an **additive sidecar** that references a v0.1 packet via `handoffManifest.id` and extends it with conversation/work-session-specific fields.

Rejected alternatives:
1. **Profile mapping to current schema** — rejected: the v0.1 `contextEnvelope` cannot carry outcome ledgers, claim posture, or artifact confirmation without semantic overload.
2. **Versioned schema revision** — rejected: premature; v0.1 is still candidate and not yet reviewed. An additive profile allows v0.1 to stabilize independently.

## Handoff profiles

```text
CHAT_CLOSEOUT_HANDOFF
WORK_SESSION_CLOSEOUT_HANDOFF
SESSION_CHECKPOINT_HANDOFF
```

## Profile schema

See `schemas/conversation-work-session-handoff-profile-v0.1.json`.

## Required content

### Identity and scope

- `handoffId`: unique identifier for this handoff packet
- `profile`: one of the three profile types
- `schemaVersion`: `conversation-work-session-handoff-profile/v0.1`
- `sourcePlatform`: platform that originated the session (e.g., "chatgpt", "claude-code", "cli")
- `sessionReference`: reference to the source conversation/work session (when safely available)
- `senderIdentity`: sender identity and posture (human, agent, mixed)
- `intendedReceiver`: named actor, role/class, next authorized session, or unbound/future receiver
- `created`, `expiry`, `supersessionReferences`: temporal and supersession metadata
- `sessionObjective`: the session's objective and bounded scope

### Outcome ledger

Each item has one of:

```text
COMPLETED
IN_PROGRESS
BLOCKED
REVERSED_OR_REJECTED
UNVERIFIED
```

Each item includes owner/home and artifact references where applicable.

### Decision and claim ledger

Each material statement carries a posture:

```text
USER_DECISION
ORGANIZATION_DECISION
EXTERNALLY_VERIFIED_FACT
USER_REPORTED_FACT
LOCAL_EXECUTION_EVIDENCE
RECOMMENDATION
CANDIDATE_TERM
HYPOTHESIS
MODEL_INFERENCE
UNRESOLVED_DISAGREEMENT
```

A compressed handoff must not upgrade one posture into another.

### Artifact ledger

For every issue, PR, document, email, calendar event, automation, file, branch, commit, receipt, benchmark, or memory update:

- `kind`: artifact type
- `destinationClassification`: public / private / internal / chat-only
- `reference`: canonical reference
- `artifactState`: CONFIRMED / UNCONFIRMED / FAILED / NOT_CREATED
- `confirmationEvidence`: reference to evidence
- `receiverMayMutate`: boolean

### Open-work ledger

- `nextRecommendedAction`: specific next action
- `dependencyOrder`: ordering constraints
- `blockers`: known blockers
- `requiredApproval`: approval needed
- `stopConditions`: conditions that should halt work
- `dueOrExpiryDate`: temporal constraints
- `ownerOrReceiverRole`: who should do it
- `mustNotDo`: constraints on what must not be done

### Capability and gap ledger

For each relevant check:

```text
PASS
FAIL
NOT_APPLICABLE
UNAVAILABLE
DECLINED
```

Examples: local Git state, bus post, memory write, connector verification, public/private preservation.

### Authority contract

- `contextTransferred`: what context was transferred
- `authorityGranted`: explicitly granted authority
- `authorityWithheld`: explicitly withheld authority
- `expiredOrRevokedDelegation`: any expired/revoked delegations
- `actionsRequiringFreshConfirmation`: actions that need new confirmation
- `publicPrivateDisclosureRestrictions`: disclosure constraints

**Default rule: handoff transfers no ambient authority.**

### Resume token

- `firstNextAction`: one bounded first action
- `minimumReferences`: minimum references required to begin

Avoid vague instructions such as "continue the work."

## Compression requirements

- No full transcript by default
- Preserve references over copied content
- Keep evidence lineage and decision provenance
- Preserve dissent and unresolved contradictions
- Do not include hidden reasoning or inaccessible UI state
- Exclude secrets and sensitive personal information unless specifically authorized and necessary
- Public handoffs use a minimal-disclosure profile

## Idempotency and supersession

- Define a stable workstream/session identity (`workstreamId`)
- Repeated closeout should update or supersede rather than duplicate
- Superseded packets remain traceable via `supersessionReferences`
- Failed or partial handoffs remain visible
- Receiver acknowledgment must bind to the exact packet/version

## Compatibility

- Aligns with `agent-handoffs#8` belief-aware semantics
- Reuses v0.1 structures where genuinely compatible (via `handoffManifest.id` reference)
- Does not create a separate handoff runtime or repo
- Keeps product-specific private state out of the public packet

## Required valid fixtures

1. `valid-strategy-chat.json` — strategy chat with no durable sink other than the handoff
2. `valid-github-work-session.json` — GitHub work session with confirmed issues/comments
3. `valid-partial-capability.json` — partial-capability ChatGPT closeout with unavailable local checks
4. `valid-checkpoint.json` — checkpoint handoff after interruption
5. `valid-public-minimal-disclosure.json` — public minimal-disclosure handoff from mixed private/public context
6. `valid-superseding.json` — superseding handoff after additional preservation work
7. `valid-unbound-receiver.json` — unbound future receiver without implied authority

## Required invalid/adversarial fixtures

1. `adv-unconfirmed-as-created.json` — marks an unconfirmed issue as created
2. `adv-recommendation-as-decision.json` — converts recommendation into decision
3. `adv-implicit-authority.json` — transfers write authority implicitly
4. `adv-omits-blocker.json` — omits a known blocker while claiming ready-to-resume
5. `adv-private-to-public.json` — copies private transcript content into public packet
6. `adv-loses-correlation.json` — loses model/provider/source correlation
7. `adv-silent-overwrite.json` — silently overwrites prior handoff
8. `adv-unaccepted-receiver.json` — names a receiver who did not accept the handoff
9. `adv-vague-next-action.json` — supplies a vague or unbounded next action
10. `adv-unavailable-as-passed.json` — treats unavailable capability checks as passed

## Acceptance criteria

- [x] Schema/profile compatibility decision documented (additive profile)
- [x] Human, agent, system, and unbound-next-session receivers represented honestly
- [x] Claim posture, dissent, evidence lineage, and authority survive compression
- [x] Artifact existence requires confirmation evidence
- [x] Checkpoint and closeout handoffs are distinguishable
- [x] Idempotency and supersession validated via fixtures
- [x] Public minimal-disclosure behavior has adversarial fixtures
- [x] Valid and invalid fixtures cover all required cases

## Non-goals

- Does not define the protocol (see protocol-as-code#7)
- Does not define the receipt (see execution-receipts#10)
- Does not transfer authority or admit memory
- Does not create a separate handoff runtime

## Receipt

- **Issue**: hummbl-dev/agent-handoffs#9
- **Compatibility decision**: additive profile referencing v0.1
- **Valid fixtures**: 7
- **Invalid/adversarial fixtures**: 10
- **Authority transfer**: none — default rule enforced
- **Private state**: excluded from public fixtures
- **Review status**: PENDING
