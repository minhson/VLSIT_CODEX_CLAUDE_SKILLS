# Content file format

`content.json` is the reviewable intermediate between the source specification and the DOCX. The
assistant authors it; `scripts/vlsit_content_check.py` validates it and `scripts/vlsit_docx_fill.py`
applies it. A worked fragment is in [vlsit_content_example.json](vlsit_content_example.json).

## Top level

```json
{
  "schema_version": 1,
  "meta": {
    "ip_name": "m_apb_tlul_bridge",
    "title": "APB4 to TL-UL Bridge",
    "revision": "0.1",
    "date": "2026-11-07",
    "source_spec": "common_rtl/007_APB2TLUL_Bridge/APB2TLUL_Bridge_Design_Specification.md",
    "source_updated": "common_rtl/007_APB2TLUL_Bridge/APB2TLUL_Bridge_Design_Specification_updated.md",
    "template": "reference/vlsit_spec_template.docx"
  },
  "sections": { },
  "functions": [ ],
  "interfaces": [ ],
  "tables": { },
  "figures": [ ]
}
```

| Key | Required | Meaning |
|---|---|---|
| `meta` | yes | identity of the run; all six fields are strings |
| `sections` | yes | content of the fixed part of the template, keyed by heading slug |
| `functions` | no | one entry per function; the `[FN-001]` subsection is cloned for each extra entry |
| `interfaces` | no | one entry per interface group; the `[IF-001]` subsection is cloned likewise |
| `tables` | no | rows for the captioned tables |
| `figures` | no | images to insert |

## Section keys

A key is the heading text lowercased, with every run of non-alphanumeric characters replaced by
one underscore, trimmed. Run `scripts/vlsit_template_probe.py` and use the slugs it prints.

Examples: `Overview` → `overview`; `IP Description` → `ip_description`;
`User-Configurable Parameters, Dependencies, and Legal Combinations` →
`user_configurable_parameters_dependencies_and_legal_combinations`.

## Section entry

```json
"ip_description": {
  "status": "filled",
  "blocks": [
    {"type": "paragraph", "text": "The bridge ..."},
    {"type": "bullets", "items": ["...", "..."]},
    {"type": "numbered", "items": ["...", "..."]},
    {"type": "note", "text": "Constraint: ..."},
    {"type": "code", "text": "assign ..."},
    {"type": "figure", "figure_id": "fig-1"},
    {"type": "table", "caption": "Table 4"}
  ]
}
```

| `status` | Requirement |
|---|---|
| `filled` | `blocks` is a non-empty list |
| `na` | `reason` (string) and `confirmed_by_user` (`true`) are required; `blocks` is empty |

Block types: `paragraph`, `bullets`, `numbered`, `note`, `code`, `figure`, `table`. Unknown types
are an error. Every `text` and every list item is one paragraph; empty strings are an error.

## Functions

```json
"functions": [
  {
    "id": "FN-001",
    "name": "APB request launch",
    "figure_id": "fig-2",
    "waveform_id": "fig-3",
    "blocks": {
      "overview_purpose_use_case_and_scope": [ {"type": "paragraph", "text": "..."} ],
      "function_description": [ {"type": "paragraph", "text": "..."} ]
    }
  }
]
```

`blocks` is keyed by the slug of the four fixed part headings. `function_diagram` and `waveform`
hold the figure references; `waveform_id` may be omitted when the function has no timing.

The filler clones the whole `[FN-001]` subsection once per extra entry and rewrites the identifier
in its headings and captions (`FN-001` becomes `FN-002`, and so on). Two consequences:

1. A figure used by a function must carry the template caption of that slot, for example
   `Figure 3. FN-001 function diagram`. The filler matches a caption by its first two words
   (`Figure 3.`), so the same entry works in every clone.
2. Tables inside the cloned subsection keep their captions and renumber through their `SEQ` fields.
   Their rows are not filled by this version; fill them through `tables` after the document is
   generated, or extend the filler deliberately.

## Tables

```json
"tables": {
  "Table 2": {"rows": [["PARA_ADDR_W", "Address width", "32", "1 to 64", "None", "Port width"]], "replace": true}
}
```

The key is the caption number or the exact caption text. `rows` is a list of rows, each a list of
cell strings; the number of cells must equal the table's column count. `replace` defaults to
`false`, which appends the rows after the existing data rows; `true` deletes the existing data
rows first. The header row and the caption are never changed.

## Figures

```json
"figures": [
  {"id": "fig-1", "path": "figures_out/block_diagram_diagram.png", "caption": "Figure 1. IP internal architecture", "width_in": 6.2, "section": "ip_block_diagram"}
]
```

`path` is relative to the folder of `content.json` (or absolute). `caption` must match the caption
paragraph that already exists in the template; the filler inserts the image before that paragraph.
`width_in` is optional and defaults to 6.2 in, the text width of the template.

## Validation rules enforced by the script

1. `schema_version` is `1`, `meta` has all six fields and none is empty.
2. Every key in `sections` matches a heading slug reported by the template probe.
3. Every `filled` section has at least one block; every `na` section has a reason and
   `confirmed_by_user: true`.
4. No block text contains a template placeholder (`[INSERT`, `[...]`, `<...>`), and no text is
   `TBD` without the word `confirmed` beside it.
5. Every table row width equals the table column count reported by the probe.
6. Every figure path exists and its caption exists in the template.
