# Simulation testbench guide

Guidance only; the mandatory requirements are in [rule.md](../rule.md) (R-010, R-022 to R-026). Read this before you write or change a simulation testbench. A testbench is written only when the user asks for one (R-022).

## 1. What the testbench is derived from (R-023)

The order of authority is:

1. The specification of the design: requirements (REQ-IDs), the cycle-level behavior, the port list, the parameters, the test plan and the assertion list of its verification section.
2. The standard of every protocol on the ports (APB, AXI, TL-UL, ...): the clause that defines a signal rule, a transfer, a response or an error. Take the text from the converted standard of the project (for example the `md_doc` folder of the specification skill), not from memory.
3. The RTL, **only** for the names, widths and parameters of the ports it must connect to. The behavior of the RTL is never a source for a stimulus, an expected value or a check.

Why: a test copied from the RTL agrees with the RTL even when the RTL is wrong. Write each check from the specification first, then run it on the RTL.

Every check, expected value and assertion carries the requirement ID or the protocol clause it comes from (in its name or in a comment). When the specification is silent or ambiguous about a behavior, ask the designer (R-005) instead of reading the answer from the RTL.

## 2. Parts of the testbench

| Part | Content |
|---|---|
| Stimulus models | One model per interface, written from the protocol: a requester for a completer port, a device or memory for a host port. They can inject the cases of the test plan: wait states, back pressure, error responses, orphan or wrong responses, back-to-back traffic, reset in the middle of a transfer. |
| Reference model / scoreboard | Expected completion, response and data computed from the specification, not from the RTL. |
| Monitors and protocol assertions | See section 3. |
| Directed tests | One group per requirement or test-plan entry of the specification. |
| Constrained-random test | Random traffic with a seed (`+SEED`) and a length (`+N`), checked by the same scoreboard and assertions. |
| Result | A table of the assertions, a one-line PASS or FAIL, and a non-zero exit status on failure (`$fatal`). |

## 2a. Layout

Keep the testbench and the assertions in their own folder beside the design files, for example `verification/` next to `rtl/`, never in the design file set or in `filelist.f` (R-010, R-022). The rule check of the skill (`vlsit_rtl_check.py`) and the lint run on the design folder only, because the design rules do not apply to verification code. A Makefile that runs the rule check, the lint and the simulation, and a folder for their logs and reports (for example `sanity/`), make the run repeatable.

## 3. Protocol assertions (R-024, R-025)

Write at least 20 assertions on the rules of each standard protocol the design has on a port, plus the assertions that relate two interfaces when the design converts between them (completion reflects response, illegal request gives no downstream request, a legal request becomes the matching downstream request). Typical groups:

- **Phases and handshakes:** a signal that is only legal with another one, a phase that lasts one cycle, a request that holds until it is accepted, a completion that lasts one cycle.
- **Stability:** address, control and data unchanged while a transfer is stalled.
- **Validity:** signals not X when the protocol says they must be valid, at the moment the protocol says so.
- **Encoding:** legal opcodes, sizes, masks, alignment, parameter fields, response codes.
- **Responses:** a response needs a request, has the opcode, size and identifier that the request calls for, and the error and data rules of the standard.
- **Reset:** the outputs the specification fixes while the reset is asserted.
- **Bounded progress:** a transfer ends within a limit that the testbench models guarantee (no hang).

Rules for the assertions:

- Name each one with the standard and the clause (for example `APB-04 ... (IHI0024D 3.1, 4.1)`) or with the requirement ID.
- Count how many times the antecedent was true (hits) and how many times the consequent failed (fails), and print the table at the end.
- The run fails when an assertion fails and also when an assertion has no hit: a check that never fired proves nothing. Make the stimulus reach it or remove it.
- A rule that binds the other side (the requester or the device) checks that the testbench stimulus is legal. When a test breaks such a rule on purpose (for example an orphan response, or a read driven with a non-zero strobe), mask exactly that assertion for exactly that cycle with an input of the assertion module, and say so in its header.
- Sample at the active clock edge before the flip-flops update, like a concurrent assertion. If the simulator has no concurrent assertions, write them as clocked checks:

```systemverilog
task chk;
  input integer id;
  input ante;     // antecedent: the assertion is active
  input cons;     // consequent: what must hold
  begin
    if (ante === 1'b1) begin
      hit[id] = hit[id] + 1;
      if (cons !== 1'b1) begin
        bad[id] = bad[id] + 1;
        $display("ASSERT FAIL @%0t: %0s", $time, nm[id]);
      end
    end
  end
endtask
```

## 4. How strong is the testbench

Show that the testbench can fail. Copy the RTL, inject a bug that matches a requirement (a rule not applied, a signal stuck, a phase one cycle late), run the testbench and record which check or assertion fired. A bug that nothing catches means a missing check or a missing stimulus. State in the report how many injected bugs were caught and which ones were equivalent to the original design. Do this on a copy, never on the delivered RTL.

## 5. When a simulation check or assertion fails (R-026)

Do not change the RTL or the test just to make the failure disappear. First decide where the fault is:

1. Read the clause of the specification or standard that the failing check comes from.
2. Read the RTL that drives the signals involved.
3. Read the test: the stimulus, the expected value, the assertion and its masks.
4. Trace the cycles around the failure.

When the cause is clear from this (for example the RTL breaks a named requirement, or the test breaks a named clause), fix it, say what you changed and why, and repeat the run. When the cause is **not** clear, stop and give the user the analysis below, then wait for the decision (R-026):

| Item | Content |
|---|---|
| Failure | Test and check or assertion name, simulation time, seed, the signal values and the cycle trace around it. |
| Specification says | The requirement ID or protocol clause, quoted, with the file and section. |
| RTL does | The file and lines that produce the observed behavior, and what they do in these cycles. |
| Test does | The stimulus, the expected value and the assertion, with the file and lines, and how the expected value was derived. |
| Candidates | A. the RTL is wrong, B. the test is wrong, C. the specification is silent or contradictory: the evidence for and against each one. |
| Impact | What each candidate means for the design and for the other tests. |
| Options | What the designer can decide (fix the RTL, fix the test, clarify the specification), with the change each one needs. A recommendation may be given and is marked as such. |

The designer decides; then make exactly that change.

## 6. Report

State which standards and which requirements the testbench was derived from, the number of assertions and the table of their hits, the stimulus cases, the seeds, the number of injected bugs caught, every failure with its decision, and what was not verified (formal proof, coverage, a protocol feature that the stimulus models do not drive).
