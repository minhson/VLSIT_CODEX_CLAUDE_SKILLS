# VCD to WaveJSON

Guidance only; the mandatory requirements are in [rule.md](../rule.md) (R-006 for the user's choice of scope).

## Steps

1. `vcd-info FILE` prints the timescale, the last time and every signal with its width and number of changes. Add `--active` to hide constants, `--pattern 'top.dut.*'` to narrow the list, `--max N` to show more lines.
2. Show the user the summary (signal groups, time range, noisy or constant signals) and ask for the scope as options: whole file, time window, signal or group list, or their own idea.
3. `vcd-to-wavejson FILE --signals "a,b*" --start 100ns --end 500ns --period 10ns --out w.json`.
4. Run `lint`, then `html`, and show the user the HTML file.

## How the converter works

- Signals are matched by full name (`top.dut.data`) or by leaf name, with glob patterns; no `--signals` means all.
- Times accept units (`ns`, `us`, ...) and are converted with the file's timescale; a plain number means VCD time units.
- The sampling step is `--period`, or by default the greatest common divisor of the change times in the window, so every change lands on a cycle boundary. A drawing of more than 400 cycles is refused; narrow the window or pass a larger `--period`.
- A 1-bit signal becomes `0`, `1`, `x`, `z` with `.` for repeated cycles. A bus becomes `=` with a hex `data` label, `x` or `z` when all bits are unknown or high-impedance, and a binary label when only some bits are unknown.
- Signals are grouped by VCD scope when they come from more than one scope (`--group` forces grouping).
- Real-valued (analog) signals are refused (R-008): ask the user which digital form to draw instead.

## Typical questions to ask

- Which part: whole file, one time window, or specific signals?
- Is the default step (finest fit) acceptable, or should one cycle be one clock period (give the period)?
- Should buses show hexadecimal or binary labels? (The converter writes hex; edit the labels if the user wants binary.)
