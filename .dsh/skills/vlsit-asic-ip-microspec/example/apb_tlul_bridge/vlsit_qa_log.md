# Simulated Q&A (example)

This log shows the style the skill uses: each question has options with explanations, an example, and an open choice. The answers are **simulated** so that the example is complete; no real user gave them.

## Round 1 (scope)

**Q1. Which direction does the bridge convert?**
- A. APB manager to TL-UL (APB subordinate, TL-UL host). Example: a peripheral subsystem that reads and writes the SoC bus. Advantage: the usual need. Disadvantage: one outstanding request only.
- B. TL-UL to APB (the opposite). Example: a CPU reaching APB peripherals.
- C. Other: write your own idea.
Answer: A.

**Q2. How many requests may be in flight?**
- A. One (recommended). Example: APB itself cannot pipeline. Advantage: no buffers, small area. Disadvantage: throughput limited by response latency.
- B. Several with a FIFO. Advantage: hides latency. Disadvantage: APB cannot use it, so extra area gives no gain.
- C. Other.
Answer: A.

## Round 2 (details)

**Q3. Which write strobes must be supported?** (Partial strobes such as 4'b0110 have no clean TL-UL form.)
- A. Only contiguous power-of-two masks, error otherwise (recommended). Advantage: always legal TL-UL. Disadvantage: a rare manager pattern gets PSLVERR.
- B. Split into several requests. Advantage: all patterns work. Disadvantage: needs a loop and several outstanding requests.
- C. Other.
Answer: A (decision DEC-001).

**Q4. What if the TL-UL device never answers?**
- A. Optional timeout with a drain state (recommended). Example: PARA_TIMEOUT_CNT = 16.
- B. Wait forever. Advantage: simplest. Disadvantage: the system hangs.
- C. Other.
Answer: A (decision DEC-004).

**Q5. Which sections are not needed?** The user confirms: interrupts, CDC, power intent, memories, register map, security topics, timing exceptions.
Answer recorded as "Not required (confirmed by user, date)" in the specification.
