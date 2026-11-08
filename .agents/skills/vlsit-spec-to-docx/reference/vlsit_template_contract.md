# Template contract

What the VLSIT IP Microarchitecture Specification template contains and what a filled document
must show in each part. Read it at step 4 and step 8. The template file is
[vlsit_spec_template.docx](vlsit_spec_template.docx).

## Shape of the document

- A4, two sections (cover page, body), 11 pt body text, 1.15 line spacing.
- Fourteen numbered sections, each starting on a new page, followed by Revision History,
  Acronyms and Definitions, and References.
- 44 captioned tables (`Table 1` … `Table 44`) plus one uncaptioned document-control table on the
  cover.
- Six caption fields: `Figure 1` … `Figure 6` in the body, one `[INSERT FIGURE]` placeholder per
  figure.
- Live fields: contents, list of tables, list of figures, page numbers (`PAGE`/`NUMPAGES`). They
  refresh when the document is opened with field update enabled; never type over them.
- Guidance paragraphs are italic grey 10 pt; they are instructions, not content, and must be
  removed or replaced in a filled document.

## Sections and what a filled document must show

| # | Section | Required content | Tables / figures |
|---|---|---|---|
| 1 | Overview | prose description of the IP, its role, boundary, operating context; feature list; limitations; standards compliance | T1 |
| 2 | Parameters | parameter model and ownership, legal combinations, validation, validated examples | T2, T3 |
| 3 | Block Diagram | internal block diagram, block responsibilities, interconnect and data/control paths | Fig 1, Fig 2 (optional SoC context), T4, T5 |
| 4 | Functions | one subsection per function, each with the four fixed parts: overview/purpose/use case/scope, function diagram, function description with modes and cycle behaviour, waveform | Fig 3, Fig 4, Fig 5; T6–T9 |
| 5 | Interfaces | one subsection per interface group, with the complete signal table | T10 |
| 6 | Control and Status Registers | CSR summary, register map, register detail, behaviour rules, interrupt and error lifecycle | T11–T15 |
| 7 | Software Programming | programming model, then the init, configure/start, normal transfer, interrupt service, DMA, error recovery and shutdown flows, then worked examples | T16–T22 |
| 8 | Integration Guideline | bus and access integration, clock/reset/power/CDC integration, interrupt/DMA/memory/pin integration, hazards and bring-up, performance and liveness requirements | T23–T25 |
| 9 | SDC | clock definitions and relationships, input/output delays, timing exceptions with rationale, synthesis and STA sign-off criteria | T26–T28 |
| 10 | DFT | test modes and access, scan and memory test, DFT verification and manufacturing | T29–T31 |
| 11 | Physical Design | implementation views, floorplan/pins/macros/power, routing and reliability, PPA results | T32–T35 |
| 12 | Verification and Validation | scope and traceability, testbench architecture, scenarios/assertions/coverage, regression sign-off | T36 |
| 13 | Power Management and Power Intent | domain and state model, transition/isolation/retention, power-intent artefacts and verification | T37–T39 |
| 14 | Security and Robustness | security boundary and access control, integrity/RAS/error containment, verification | T40–T42 |
| — | Revision History / Acronyms / References | revision rows, acronym definitions, numbered reference list | T43, T44 |

## Rules for the writer

1. Every guidance paragraph under a heading is replaced by real content or removed; a filled
   document contains no `[...]` prompt.
2. A table keeps its caption and header row; only data rows are added or replaced, so the column
   count never changes.
3. A figure placeholder is replaced by the image; the caption and its field stay untouched.
4. Section 4 is repeated for each function: duplicate the whole subsection, keep the four part
   headings, renumber only the function ID (`[FN-001]`, `[FN-002]`, …).
5. Section 5 is repeated for each interface group (`[IF-001]`, `[IF-002]`, …).
6. A section that does not apply keeps its heading and states `N/A` with a one-paragraph reason,
   confirmed by the user (R-005).
7. Identifier conventions used by the template: `FEAT-`, `LIM-`, `PAR-`, `CFG-`, `BLK-`, `FN-`,
   `IF-`, `REQ-FN001-`, `SDC-EX-`, `DFT-`, `PD-`, `PPA-`, `PERF-`, `INT-`, `TC-`. Keep them; the
   verification traceability table (T36) refers to them.

## Filling anchors

`scripts/vlsit_template_probe.py` reports, for the template: the heading text of each section, the
index and text of every guidance paragraph, the caption text of every table, and the text of every
figure placeholder. The content keys used in `content.json` are the slug of the heading text, so
they stay stable when the document is re-flowed. Run the probe on a user template before filling it.
