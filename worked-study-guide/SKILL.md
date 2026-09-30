---
name: worked-study-guide
description: Create worked study guides from homework, lesson questions, screenshots, and local textbooks, especially for engineering courses. Use when the user wants a study guide explaining the setup, governing equations, assumptions, calculations, and diagrams. Defaults to self-contained HTML; not a general textbook summarizer or flashcard generator.
---

# Worked Study Guide

Create a study companion that teaches how to start and solve every assigned problem. The user's established preference is a self-contained HTML file, with source images where available and explicit derivations before substitution. Follow newer user instructions when they change this format.

## Find the assignment and sources

1. Inspect the specified folder and applicable local instructions. Inventory all questions and subparts, including required plots, sketches, proofs, and alternate solution methods. Inspect a previous guide when referenced; use it for style, not as authority for a new answer.
2. Locate the supplied textbook, tables, diagrams, and instructor modifications. Prefer the user's actual textbook edition and tables over properties copied from an earlier guide. Booklet PDFs may have two book pages per PDF page in imposed order: inspect the correct half and distinguish printed page numbers from PDF positions.
3. Put the finished guide beside the assignment or in the requested destination. Keep generators, calculations, crops, and validation artifacts in `guide_source`. Preserve original inputs. Do not create a PDF unless requested.
4. If essential data is obscured or missing, ask one focused question early and continue independent work. Keep dependent results symbolic until resolved. An input control can evaluate a symbolic solution; do not silently default to an invented value. Conventional modeling assumptions may be used when justified, but state them and their effect on the answer.

## Required organization for each problem

Use this order unless the user asks otherwise:

1. **Problem.** Include a readable crop of the original question and its referenced diagram or table. Preserve relevant text, dimensions, arrows, and labels. Cite the source filename and textbook page. For text-only assignments, reproduce the supplied prompt in a labeled text block; do not manufacture an image and call it an original screenshot. Shared images may be reused for linked questions.
2. **Knowns and unknowns.** List values, units, geometry, states, coordinates, sign conventions, and what must be found. Distinguish given facts, looked-up properties, and assumptions.
3. **Equations to reference.** Show governing equations in their general form before specialized formulas, plus relevant property definitions and constitutive relations. A common reference sheet may introduce notation, but each problem must make its own starting law clear.
4. **Assumptions and consequences.** Explain which term each assumption removes, which parameter becomes constant, or which model becomes valid. Do not attach a generic list of inapplicable assumptions.
5. **Worked solution.** Define the system, control volume, or free body; reduce governing equations; solve symbolically where helpful; then substitute numbers with units. Show intermediate steps, every requested subpart, a boxed result, and a short physical or dimensional check.

Connect explanations to algebra. The starting point matters more than listing a final shortcut. Show accumulation terms before setting them to zero, and justify canceling a density, pressure, area, or other shared factor. Distinguish sign from magnitude and force/work on a body from that exerted by it.

Read the relevant subject notes in [references/engineering-guidance.md](references/engineering-guidance.md) when useful. These are reasoning checks, not assumptions to impose on every assignment.

## Work the content accurately

- Classify the state or physical regime before selecting a property table or model. State approximations such as compressed-liquid properties evaluated at the same temperature.
- Identify properties by table, state inputs, units, and source location. Retain intermediate precision; explain differences caused by independently rounded table columns rather than forcing exact agreement.
- Derive answers from the supplied information. Never infer covered dimensions from drawing proportions or present a sample calculation as the assigned answer.
- Cover every requested diagram and alternate method. Include a compact answer check at the end. Add conceptual checks when they clarify recurring mistakes; do not expand into unrelated lessons.

## HTML, source images, and diagrams

Use [assets/guide_template.html](assets/guide_template.html) and [scripts/build_html.py](scripts/build_html.py) when they fit. The builder supplies visual styling, navigation, image zoom, and embedded images. Read [references/html-builder.md](references/html-builder.md) for its input format. Direct HTML authoring is also fine.

- Default to a navy/teal layout with clear headings, pale equation blocks, boxed answers, responsive tables, and mobile-friendly spacing. Keep explanations and formulas readable without interactive controls.
- Deliver one offline HTML file with images embedded as data URLs, inline CSS, and any necessary inline JavaScript. Citations may be links, but reading the guide must not require a CDN or account. Use **KaTeX** for textbook-style math by default: author formulas in LaTeX, pre-render them as HTML with accompanying MathML, and embed the KaTeX CSS and fonts. Apply this to inline notation as well as display equations. See the math-typesetting workflow in [references/html-builder.md](references/html-builder.md). Do not use plain Unicode or hand-built subscript/superscript formulas as the primary equation renderer.
- Extract screenshots directly from supplied PDFs or images. Inspect crops for cut-off text and labels. Mark omitted rows when showing a table header and a separate row crop.
- Use native SVG/HTML for explanatory diagrams. Label coordinate directions, states, units, process arrows, and signs. Distinguish schematic geometry from quantitatively scaled plots. For scientific figures intended for export, use appropriate plotting tools and provide the standalone artifact.
- Add interaction when it helps explain a dependency, such as changing an unknown length or comparing heat and work. Keep the assigned case distinct from what-if values. Provide a reset, units, input validation, and textual results alongside diagrams.
- Never substitute generated imagery for an original textbook problem, measured chart, or property table.

## Check and finish

Verify calculations using an independent relation where practical: conservation residuals, dimensional consistency, numerical integration, alternate energy balances, or stress-tensor eigenvalues. Check special cases that could expose a sign or frame error. Do not merely compare two copies of the same formula.

Inspect the HTML in a browser when available. Check equations, diagram labels, screenshots, navigation, and mobile overflow. Verify KaTeX fonts and equations load with the network disabled, and resolve all math parse errors. Long equations may scroll within their own blocks but must not widen the page. Test controls' assigned defaults, updates, reset, and invalid inputs. Use a separate browser-test profile and remove only temporary files created for the task.

Confirm all requested subparts are present, images are embedded, and no draft tokens remain. Finish with a link to the guide and any material unresolved assumption or missing input. Report only checks actually performed.
