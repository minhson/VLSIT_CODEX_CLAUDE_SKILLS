# Specification writing guide

Guidance only; the mandatory requirements are in [rule.md](../rule.md) (R-013 to R-017). The template is `templates/VLSIT_ASIC_IP_Design_Specification_Template.md`; follow its section titles exactly.

| Section | What to put there | Typical questions to the user |
|---|---|---|
| 1 Purpose, scope | Problem, boundary, included and excluded functions, SoC context, feature list | Which function must it do and not do? Which SoC and workload? |
| 2 References | Exact title, revision and clauses; conflict order; compliance table | Which protocol revision and role? Which deviations are accepted? |
| 3 Requirements | One shall per requirement with REQ-ID, source, applicability and verification method | Which behaviors are mandatory and how are they verified? |
| 4 Features and configurations | Configuration table; optional features absent, tied off or runtime-disabled | Which configurations ship? |
| 5 Architecture | Blocks, block diagram (R-017), dataflow, invariants | What are the blocks and what is stored? |
| 6 Interfaces and ports | Interface inventory, full port list with reset values, protocol behavior and key waveforms, interrupts | Which ports, widths, reset values, error and unsupported cases? |
| 7 Clock, reset, power | Domains, CDC, resets, power intent | How many clocks and resets? Any low-power mode? |
| 8 Parameters | Parameter table, VLSIT comment lines, configurations, illegal values | Which values may change, and which are illegal? |
| 9 Data representation | Widths, endianness, encodings, invalid behavior | Which encodings and overflow rules? |
| 10 Functional behavior | States, operations, cycle tables, throughput, memories | What happens cycle by cycle, with backpressure? |
| 11 Registers | Pointer to the CSR workbook and software sequences | Which registers? (fill the workbook) |
| 12 Errors | Error table, precedence, recovery, waveforms | What are the errors and how does the system recover? |
| 13 PPA | Hard requirements and goals with conditions | Frequency, area, power targets and corners? |
| 14 RTL contract | Coding baseline, hierarchy, synthesis assumptions | Hierarchy and synthesis setup? |
| 15 Verification | Strategy, test plan, assertions, coverage, formal, CDC | Which levels and which protocol checkers? |
| 16 DFT | Scan, MBIST, test ports, clock-gating test enable | Which test methods apply? |
| 17 Physical, timing | Clocks, I/O budgets, exceptions, physical assumptions | Who owns constraints? Any exceptions? |
| 18 Security, safety | Each topic Required, Not required (confirmed) or TBD | Is there a threat model or safety goal? |
| 19 Traceability | Every REQ to module, test, method, configuration | Generated from sections 3 and 15 |
| 20 Assumptions, decisions | Assumptions, dependencies, decisions, open items, TBD with impact | Which points remain open? |
| 21 Glossary, 22 References | Terms and the sources actually used | Not applicable |

## Names (from VLSIT_RTL_Design_Rule.md)

Module `m_<function>`; ports `i_`/`o_` with protocol tag `<direction>_<protocol>_<signal>` (for example `i_apb_psel`); clock `i_clk_<domain>`; reset `i_rst_n_<domain>`; parameters `PARA_<NAME>`; FSM `reg_fsm_<function>_current_state` with states `ENUM_ST_<FUNCTION>`; names at most 30 characters.

## Not required

When the user confirms a point is not needed, write `**Not required (confirmed by user, YYYY-MM-DD):** reason` with `vlsit_spec_tool.py mark-not-required FILE SECTION --reason TEXT`, or type the same line into a table cell.
