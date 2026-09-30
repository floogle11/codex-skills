# Building the offline HTML guide

The optional builder uses Python's standard library. It renders authored JSON into the included layout and embeds images. It does not solve problems, fetch properties, crop PDFs, typeset LaTeX, sanitize untrusted HTML, or generate a PDF. Complete the KaTeX rendering step below before delivering the guide.

```text
python scripts/build_html.py path/to/guide_source/content.json path/to/Worked-Study-Guide.html
```

Resolve the script relative to this skill. Image paths in authored HTML are relative to the JSON file. Data-image URLs are preserved. Missing files, remote image URLs, image `srcset`, linked scripts/styles, and duplicate section IDs are rejected.

## Authored content format

Required: `title` and a nonempty `sections` array. Every section needs a unique `id`, a `title`, and `body_html`. Other fields are optional.

```json
{
  "title": "Thermodynamics - Worked Study Guide",
  "subtitle": "Boundary work and closed-system energy balances",
  "intro_html": "<p>Write the energy balance before substituting numbers.</p>",
  "sections": [
    {
      "id": "problem-1",
      "title": "1 - Isothermal compression",
      "body_html": "<h3>1 · Problem</h3><div class=\"prompt\">A fixed mass of ideal gas is compressed at constant temperature.</div><h3>2 · Knowns</h3><p>Mass, temperature, and endpoint volumes come from the assignment.</p><h3>3 · Equations</h3><div class=\"eq\">\\[W_b=\\int P\\,dV,\\qquad PV=mRT\\]</div><h3>4 · Assumptions</h3><p>Fixed mass, ideal gas, isothermal, quasi-equilibrium.</p><h3>5 · Solution</h3><div class=\"eq\">\\[W_b=mRT\\ln(V_2/V_1)\\]</div><div class=\"answer\">Compression gives negative work under a work-by-system convention.</div>"
    }
  ],
  "source_notes_html": "<p>Identify the assignment, textbook edition, and table pages.</p>",
  "extra_css": "",
  "extra_js": ""
}
```

This illustrates the schema, not a completed numerical solution. Populate all assigned facts, derivations, results, and sources for the real task. HTML strings are trusted authored content, not arbitrary executable material copied from source documents.

## Textbook-style math with KaTeX

Use KaTeX as the default math renderer. Author inline math with `\(...\)` and display math with `\[...\]`; in JSON, escape each backslash as `\\`. Use proper fractions, integrals, aligned derivations, subscripts, and upright units instead of assembling formulas from Unicode characters and HTML subscript tags.

The Python builder does not render these delimiters. Either insert pre-rendered math into `body_html`, or process the generated HTML afterward with a local Node.js rendering step. Direct HTML authoring uses the same approach:

```js
katex.renderToString(latex, {
  displayMode: isDisplay,
  output: 'htmlAndMathml',
  throwOnError: true,
  trust: false
});
```

- Use a local KaTeX package; record its version and retain its license. Keep package files and rendering scripts in the assignment's `guide_source` folder. An already available package is suitable; an upgrade is not required for each guide.
- Embed `katex.min.css` and replace its font URLs with data URLs containing the corresponding WOFF2 fonts. Remove unused external font-source alternatives. Pre-rendered static equations do not need the KaTeX JavaScript library at runtime. If interaction requires re-typesetting, embed the required JavaScript too.
- Preserve the accompanying MathML for accessibility. Render only designated math content, not scripts, styles, code examples, or already-rendered equations. Do not deliver raw delimiters or silently ignore parse errors.
- Give equation blocks horizontal scrolling when needed, with enough vertical padding for tall fractions and integrals. Position math wrappers and scrollable tables relatively so KaTeX's absolutely positioned accessibility content stays contained. Check long inline expressions too. Prefer shorter aligned steps when they improve readability.
- Inspect desktop and narrow mobile layouts with the network disabled. Confirm embedded fonts actually load, no external asset requests occur, and the document width stays within the configured viewport (not just a browser-expanded `innerWidth`).

Official references: [KaTeX pre-rendering](https://katex.org/docs/node), [rendering API](https://katex.org/docs/api), and [font handling](https://katex.org/docs/font).

## Layout classes

- `prompt`: question text; `img.source-image`: original screenshot with zoom.
- `eq` and child `line` spans: equation blocks with one or more lines.
- `answer`: result with sign, units, and interpretation.
- `note`: material assumption, approximation, or missing input.
- `check`: physical or dimensional check.
- `grid` / `card`: responsive parallel panels.
- `table-wrap`: scrollable wrapper for wide tables.
- `figbox` / `figure`: explanatory SVG or diagrams.
- `caption` / `source`: attribution and diagram conventions.
- `screen-only`: controls omitted when printing.

Navigation is generated from section IDs. Source images enlarge by click or keyboard. Inline SVG may appear in `body_html`. Put chart logic in `extra_js`; use unique element IDs and include textual results. The template supplies only image zoom, not numerical chart logic.

The builder checks packaging and structure. Still inspect layout and verify equations, diagrams, and calculations. Do not add runtime network requests through authored JavaScript or CSS.
