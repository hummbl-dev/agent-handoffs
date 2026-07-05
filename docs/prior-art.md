# Prior Art and Adjacent Ecosystem

This document collects public prior art and adjacent ecosystem references relevant to
agent handoffs. It is non-exhaustive and intentionally non-canon: it exists to place
the candidate v0.1 baseline inside the existing field rather than to claim novelty
over it.

## Non-canon note

Nothing in this document is asserted as authoritative. Links point to public
documentation and repositories. Names, terms, and concepts are shared vocabulary
across the ecosystem; no ownership is claimed by this repository over any term,
pattern, or protocol listed below. Where a concept appears in multiple projects, the
earliest public source is not adjudicated here.

## Vocabulary

The following terms recur across the prior art and adjacent ecosystem and are used
throughout this repository:

- **Handoff** — transfer of responsibility for a task or session from one agent (or
  human) to another.
- **Delegation** — transfer of authority to act on behalf of another agent, with
  defined scope and limits.
- **Context transfer** — movement of the minimal state required for a receiving
  agent to continue work.
- **Agent-to-agent** — communication or handoff between two agents.
- **Session continuity** — preservation of conversational or task state across a
  handoff so the receiving agent can continue without restart.
- **State handoff** — explicit transfer of execution or task state between agents.

## Key concepts

- **Context envelope** — the bundled minimal state (objective, scope, constraints,
  pointers to prior context) carried by a handoff packet.
- **Delegation token** — a scoped, expiring grant of authority from one agent to
  another.
- **State transfer** — the act of moving execution or task state from a source to a
  recipient.
- **Session continuity** — the property that a session remains usable across a
  handoff.
- **Receipt chain** — an ordered, append-only provenance record across handoff hops.
- **Authority propagation** — the flow of delegated authority along a chain of
  handoffs, bounded by scope and expiry.

## Public prior art

### OpenAI Assistants API — handoff patterns

- **What it does:** Provides a hosted assistant abstraction with persistent threads,
  tool bindings, and run lifecycle. Handoff-like patterns arise by routing a thread
  between assistants or by delegating tool calls.
- **Relevance:** Demonstrates session continuity and context transfer via persistent
  threads, and informs how a context envelope can be modeled independently of any
  single vendor's runtime.
- **Public docs:** https://platform.openai.com/docs/assistants/overview

### LangGraph — state handoffs

- **What it does:** A graph-based orchestration framework where nodes exchange state
  through a shared, typed state object and conditional edges route execution between
  agents.
- **Relevance:** Directly models state handoff between agents as typed state transfer
  along graph edges; informs the context envelope and state transfer concepts.
- **Public docs:** https://langchain-ai.github.io/langgraph/

### CrewAI — task delegation

- **What it does:** A framework for orchestrating role-defined agents that delegate
  tasks to each other under a crew-level plan.
- **Relevance:** Models delegation and role-based authority transfer between agents;
  informs delegation scope and authority propagation.
- **Public docs:** https://docs.crewai.com/introduction

### AutoGen — conversation patterns

- **What it does:** A multi-agent conversation framework where agents exchange
  messages in conversational patterns (two-agent, group chat, sequential) and can
  delegate work to each other.
- **Relevance:** Models agent-to-agent handoff as conversational turn-taking and
  delegation; informs session continuity and agent-to-agent vocabulary.
- **Public docs:** https://microsoft.github.io/autogen/

### A2A — Agent-to-Agent protocol

- **What it does:** An open protocol for agent-to-agent communication and task
  delegation, including agent cards, task lifecycle, and streaming updates.
- **Relevance:** Directly addresses agent-to-agent handoff and delegation as an
  interoperable protocol; informs delegation token, agent identity, and receipt
  concepts.
- **Public docs:** https://a2a-protocol.org/latest/

### ACP — Agent Communication Protocol

- **What it does:** An open protocol for agent communication standardizing how agents
  exchange messages, describe capabilities, and negotiate interactions.
- **Relevance:** Standardizes agent-to-agent messaging and capability description;
  informs the contract shape of a handoff packet.
- **Public docs:** https://agentcommunicationprotocol.com/

### OpenClaw ACP

- **What it does:** A public implementation/reference exploring the Agent
  Communication Protocol surface in an open, extensible form.
- **Relevance:** Provides a concrete, open reference point for ACP-style agent
  communication and handoff; informs how a candidate baseline can stay
  implementation-agnostic.
- **Public docs:** https://github.com/openclaw

## Adjacent ecosystem

### MCP — Model Context Protocol

- **What it does:** An open protocol for connecting models/agents to external tools,
  data sources, and resources through a standardized context layer.
- **Relevance:** Standardizes how context is exposed to agents; adjacent to (not the
  same as) handoff, but informs how a context envelope can reference external
  resources rather than embedding them.
- **Public docs:** https://modelcontextprotocol.io/

### A2A-Protocol

- **What it does:** The reference organization for the A2A agent-to-agent protocol,
  including specs, SDKs, and examples.
- **Relevance:** Primary public home for agent-to-agent protocol work; informs
  delegation, task lifecycle, and receipt concepts.
- **Public docs:** https://github.com/a2aproject

### Google A2A

- **What it does:** Google's public A2A protocol work for agent-to-agent
  interoperability, including agent cards and task delegation semantics.
- **Relevance:** A major public reference for agent-to-agent handoff and delegation;
  informs agent identity and delegation scope.
- **Public docs:** https://github.com/google-a2a/A2A

### Semantic Kernel — orchestration

- **What it does:** An orchestration SDK that chains prompts, tools, and agents into
  plans and pipelines with planner-based delegation.
- **Relevance:** Models orchestration and planner-driven delegation; informs how a
  handoff packet can sit alongside, rather than replace, an orchestration runtime.
- **Public docs:** https://learn.microsoft.com/en-us/semantic-kernel/overview/

### Temporal — workflows

- **What it does:** A durable execution engine for workflows, with state, retries,
  timers, and event-sourced history that preserves execution state across process
  boundaries.
- **Relevance:** Models durable state transfer and provenance across hops; informs
  the receipt chain and state transfer concepts for long-running handoffs.
- **Public docs:** https://docs.temporal.io/
