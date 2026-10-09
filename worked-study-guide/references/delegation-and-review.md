# Delegation and review

Use bounded support tasks to reduce cost while keeping the lead responsible for engineering reasoning and the finished guide. These instructions authorize delegation within guide creation when the environment permits it. They do not require delegation for short or dependent steps.

## Model assignments

| Task | Preferred model and effort | Boundary |
|---|---|---|
| Assignment inventory, page/figure locating, checklist creation, completeness check | GPT-6 Luna, Low | Extract and organize; do not solve problems. |
| Screenshot crop inspection and prompt/label transcription | GPT-6 Luna, Low; Medium for ambiguous handwriting, image quality, or labels | Return candidate text/crops with source locations and uncertainty flags. Never guess illegible values. |
| Textbook/source navigation | GPT-6 Luna, Low | Locate candidate pages and table entries; the lead verifies relevance and property selection. |
| Straightforward arithmetic, unit conversion, numeric spot-check | GPT-6 Luna, Medium | Recompute from the lead's stated equations and givens; do not decide whether the physical model is valid. |
| Learner clarity audit of a complete guide | GPT-6 Luna, Medium | Flag confusing transitions, undefined notation, and unexplained cancellations; suggest targeted edits. |
| Adversarial technical audit of a complete guide | GPT-6.1 Sol, High | Independently inspect governing equations, assumptions, signs, units, states/properties, calculations, and prompt coverage. |
| Escalation on an unresolved technical disagreement or unusually difficult modeling/source ambiguity | GPT-6 Astra, High | Address only the specific issue under the escalation limit below. |

For technically involved guides, use GPT-6.1 Sol at High effort or stronger as the lead where configurable. The lead verifies agent findings against the assignment, textbook, and calculations. A stronger reviewer is not automatically correct.

When supported, the corresponding tool model identifiers are `gpt-6-luna`, `gpt-6.1-sol`, and `gpt-6-astra`, with `low`, `medium`, or `high` effort. Check the active tool's advertised availability. For model overrides requiring a fresh context, use `fork_turns="none"` and supply the bounded task, relevant raw sources, guide paths, and constraints explicitly.

If a preferred model is unavailable, use the closest available lower-cost model for extraction/support and the strongest available general reasoning model for technical review. Do not silently lower the reviewer tier for a difficult audit. Record substitutions and material limitations. If delegation is unavailable, perform the checks with the lead and disclose that independent agent review was unavailable; do not claim it occurred or stall otherwise authorized work. Skill instructions cannot themselves change the active lead model or effort.

## Support task contracts

Give each agent one clearly scoped task with concise, structured output. Delegate only independent work that can proceed without another task's result. Include the relevant source files/pages, expected output, uncertainty handling, and an explicit prohibition on further delegation. Agents may prepare candidate crops or other assigned support artifacts in separate task directories under `guide_source`; avoid concurrent edits to shared files.

| Task | Required result and lead verification |
|---|---|
| Assignment inventory | Checklist of every problem, subpart, requested plot/sketch/proof, alternate method, and referenced figure/table. The lead confirms it against the source. |
| Screenshot support | Relevant PDF positions and candidate crops of statements, figures, and tables; flag illegible or cut-off content. The lead visually inspects crops before inclusion. |
| Prompt transcription | Problem text, numerical givens, units, and diagram labels with uncertain readings marked. The lead checks the original. |
| Source navigation | Candidate textbook pages, tables, and instructor modifications with filenames, printed pages, and PDF positions. The lead decides applicability. |
| Calculation spot-check | Equations used, inputs with units, independently recomputed values, and discrepancies. The lead validates the physical model and assumptions. |
| Completeness check | Comparison of the near-final guide with the confirmed checklist; flag missing subparts, figures, units, citations, intermediate steps, or answers. Fold into an existing support task or technical audit when practical. |

Keep governing-equation selection, physical modeling, assumptions, property-state classification, and final synthesis with the lead unless it requests a narrowly bounded independent opinion. Treat agent output as a lead for verification, never as authoritative source material.

## Review sequence

Once the draft covers the full assignment, run these passes once each, in order:

1. **Technical audit — GPT-6.1 Sol, High.** Give the reviewer the complete guide and relevant assignment/textbook sources. Ask it to independently trace setup and solution, looking for unsupported equations or assumptions, omitted terms, sign/frame mistakes, dimensional inconsistency, arithmetic errors, table/state mismatches, and missing prompt requirements. Supply enough raw evidence to check the solution without relying on the lead's conclusions.
2. **Learner clarity audit — GPT-6 Luna, Medium.** Read the complete guide as a student encountering the method for the first time. Flag unexplained equation choices, algebraic jumps, cancellations, undefined symbols, unclear units/sign conventions, and assumptions whose consequences are not explained. Suggest concise fixes without changing technical content.
3. **Resolution — lead, at the same or higher effort than drafting where configurable.** Mark every finding valid, invalid, or unresolved and record the supporting evidence. Correct valid issues and check the corrections against the assignment, supplied sources, and calculations. Verify reviewer claims before accepting them.

Ask both reviewers for actionable findings with:

- Location: problem/subpart and guide section or equation.
- Finding and why it matters.
- Evidence or independent check.
- Suggested correction, if known.
- Confidence: high, medium, or low.

Have reviewers explicitly identify checked categories with no issues. A clean review is not proof of correctness. Keep a compact review log in `guide_source` containing model/effort used, findings, lead dispositions, evidence, and any unresolved impact. Reviewers report findings only; the lead makes edits.

## Hard limits and escalation

- At most **two delegated agents active at once** for one guide.
- Each delegated task returns **one result**. No subagent may create or delegate to another agent.
- Permit **one retry per task**, only when the initial result is missing, malformed, or explicitly incomplete. Narrow or clarify the retry request; never repeat an unchanged prompt. A retry completes the original task, not a new audit of a revised guide. If it still fails, the lead handles the remaining work and records any review limitation.
- Allow **three regular review passes total**: one technical audit, one clarity audit, and one lead resolution. Do not rerun a pass to seek agreement.
- Allow **one additional GPT-6 Astra/High escalation** on a specific disputed point if technical disagreement remains after resolution, or on a specifically identified issue with unusually difficult modeling or source ambiguity. This is the sole exception to the three-pass limit; an earlier escalation consumes the same allowance. Do not escalate the whole guide by default.
- After escalation, the lead verifies the response and applies any supported correction without another reviewer round. Record any remaining uncertainty and its impact rather than presenting it as resolved.
- Stop when the assignment checklist is complete and findings are resolved or explicitly recorded as unresolved. Do not continue asking agents whether the guide is correct.
