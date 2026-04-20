# Constraint Analysis Reference

Supporting reference for the workflow-auditor skill. Use this during Steps 2, 3, and 4.

---

## Five Types of Time

For each step in a workflow, classify the time spent into one of these five categories. Most people only see processing time. The waste is almost always in the other four.

**Processing time** — actual work being done. Writing, calculating, building, deciding. This is the only type that adds value. Everything else is waste to be minimised.

**Waiting time** — work is done but sitting in a queue. Awaiting approval, sitting in an inbox, pending a meeting that happens weekly. Often invisible because nothing looks broken — the work is finished, it's just not moving.

**Handoff time** — moving work between people or systems. Emailing files, copy-pasting data between tools, re-entering information into a new format. Every handoff is a failure point and a delay.

**Rework time** — fixing errors, redoing work, clarifying misunderstandings. Rework is expensive because the work happens twice. More importantly, rework usually signals a broken upstream step — fixing the rework without fixing the upstream step is pointless.

**Setup time** — getting ready to do the work. Finding files, logging in, reading context, waiting for a system to load, asking someone for the background. High setup time often means information is not accessible to the person who needs it.

Most people underestimate waiting, handoff, and setup time. Ask directly: "How long does this step actually take from when the previous step finishes to when you start working on it?"

---

## Five C's Framework

Before recommending a fix, check these five factors. If any are weak, fixing the technical constraint alone will not help. Address the human factor first.

**Context** — does the team understand what is happening in their workflow? Can they see the whole picture, or only their part? People who cannot see the whole system cannot improve it. They optimise their step at the expense of the whole.

**Control** — can the people doing the work direct and shape the outputs, or are they just following a rigid process? Workers with no control cannot adapt when something goes wrong. They escalate instead of solving.

**Confidence** — do they trust the tools and data they are working with? Are they double-checking everything? Low confidence creates hidden rework. People verify outputs they should be able to trust, or they avoid tools that have let them down before.

**Coordination** — how does work move between people? Are handoffs explicit or assumed? Clear handoffs with defined ownership are fast. Unclear handoffs with assumed ownership create gaps where work sits unclaimed.

**Capacity** — is there actually enough time and attention for this work, or is it being squeezed between other priorities? A workflow that looks broken might just be under-resourced. No process improvement will help if the people doing the work are already at 110%.

---

## Common Constraint Patterns

These are the most frequent constraint types found in SMB workflows:

- Single approval bottleneck: one person must sign off at a critical step, and they are not always available
- Data in one system needed in another: information exists but requires manual transfer between tools
- Manual step not yet automated: a repetitive task that nobody has found time to address
- Quality checks catching upstream errors: a review step that exists because an earlier step is unreliable
- Information available but not accessible: data exists in the organisation but the person who needs it cannot reach it without asking someone else

---

## After the Fix

Once the first constraint is addressed, the bottleneck moves. Note where you think it will move next so the user is prepared. The second constraint is usually visible in the workflow map — it is the step that was previously fast but only because it was waiting for the first constraint.
