# Reference-IP research log (example run)

Run with `scripts/vlsit_ip_search.py` and `scripts/vlsit_protocol_docs.py` on 2026-10-18. Rule R-007: only IP with silicon or FPGA evidence, a testbench and a licence is used as a design reference.

## Queries

| Query | Source | Result |
|---|---|---|
| `tilelink apb` | GitHub | 3 candidates, 0 qualified (table below) |
| `apb2tlul`, `tlul apb bridge` | GitHub | 0 candidates |
| `opentitan tlul` | Gitee | 0 candidates (no Chinese-site reference IP found for this function) |

## Candidates

| Candidate | Direction | Evidence found | Licence | Decision |
|---|---|---|---|---|
| vyges/tlul-apb-adapter | TL-UL device to APB manager (the reverse of this IP) | README states "Maturity: Prototype"; simulation testbenches (SystemVerilog and cocotb); no tapeout or FPGA board evidence | README badge says Apache-2.0, but the GitHub licence field is NOASSERTION | EXCLUDED by R-007 (no silicon or FPGA proof, licence unclear). Read for ideas only; nothing copied |
| vyges-ip/tlul-apb-adapter | Same project, mirror | Same | NOASSERTION | EXCLUDED |
| merledu/common_peripheral_ips | Peripheral collection | No evidence | Apache-2.0 | EXCLUDED |

## Accepted reference

| Reference | Evidence of silicon | Used for |
|---|---|---|
| lowRISC OpenTitan (Apache-2.0), TL-UL documents `hw/ip/tlul/README.md` and `hw/ip/tlul/doc/TlulProtocolChecker.md` | OpenTitan Earl Grey: first silicon tapeout reported in 2023 and commercial availability announced on 2024-02-13 by lowRISC and partners (Business Wire release dated 2024-02-12, Cambridge Network) | Interface signals, opcodes, error cases and protocol checks (`reference/md_doc/tilelink_ul_*.md`) |

## Findings that shaped the specification

- OpenTitan has no APB-to-TL-UL bridge under `hw/ip/tlul`; the TL-UL adapters there are `tlul_adapter_host`, `tlul_adapter_reg` and `tlul_adapter_sram`. The bridge of this example is a new design, so the TL-UL side follows the OpenTitan TL-UL profile and checker only.
- The reverse bridge (TL-UL to APB) exists as an unproven prototype; the single-outstanding design choice (REQ-FUNC-005) is the same idea, and its timeout handling is not copied.
- The mask rule conflict between the TL-UL README and the protocol checker is recorded as OI-001.

## Not done

- No RTL of any candidate was downloaded.
- Chinese sources (Gitee, CSDN) returned no relevant candidate; the Gitee search API may need a token (not tested with one).
