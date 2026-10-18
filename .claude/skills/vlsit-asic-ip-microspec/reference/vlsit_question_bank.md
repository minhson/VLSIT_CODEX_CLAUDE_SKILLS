# Question bank

Guidance only; the mandatory requirements are in [rule.md](../rule.md) (R-003, R-004). Each question has at least two options with explanations and an example, and ends with an open choice. At most four questions per message. Adapt the wording to the IP.

## Format

```
Q. <the question>
Why it matters: <one sentence>
A. <option> (recommended: <reason>)
   Meaning / example: <concrete example>
   Advantage: <...>   Disadvantage: <...>
B. <option>
   ...
C. Other: write your own idea.
```

## Scope and function

1. What is the main function, and what must it not do? (Example: "convert an APB write into a TL-UL write; must not decode addresses".)
2. Which interfaces and roles? (Example: APB subordinate and TL-UL host; options: add an interrupt, a debug port, a test port.)
3. How many transactions in flight? (A: one, simple and small; B: several with a FIFO, hides latency but costs area; C: other.)

## Protocol

4. Which revision and optional signals? (Example for APB: APB3 without PSTRB or PPROT; APB4 with PSTRB, PPROT and PSLVERR; APB5 with extra user signals.)
5. What happens on an unsupported or illegal request? (A: error response; B: ignore; C: split into legal requests.)
6. What is the timeout policy for a peer that does not answer? (A: no timeout, simplest; B: counter with an error and a drain state; C: other.)

## Clock, reset, power

7. One clock domain or several? (A: one, no CDC; B: two with a handshake or FIFO crossing; state which structure.)
8. Reset style? (A: asynchronous assertion with synchronized release; B: synchronous reset; follow the project policy.)

## Verification, DFT, physical

9. Which protocol checkers and coverage? (A: vendor checker plus formal proofs; B: simulation only.)
10. Which DFT methods apply? (Scan always; MBIST and LBIST only with memories or logic BIST.)
11. Who owns timing constraints? (A: IP delivers an SDC; B: integrator writes all constraints.)

## Closing each section

12. "Is this section needed?" Options: A: yes, fill it; B: not required, record the reason (the skill writes the dated line); C: decide later, record a TBD with its impact.
