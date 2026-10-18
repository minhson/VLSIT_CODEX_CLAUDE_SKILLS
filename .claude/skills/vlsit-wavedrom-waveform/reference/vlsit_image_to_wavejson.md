# Image to WaveJSON

Guidance only; the mandatory requirements are in [rule.md](../rule.md) (R-004, R-007, R-008).

## Reading the image

Look at the image closely, zoom into regions when possible, and write down what is drawn before drawing anything. Use this table, one row per signal in drawn order, and fill every column that the image shows:

| Group | Signal (exact text) | Cell 1 | Cell 2 | ... | Notes (data labels, glitches, gaps) |
|---|---|---|---|---|---|

Then list, separately:

- the time axis: ticks, units, where each cycle starts, any break;
- the clock: period, duty, which edge the data changes on;
- edges and annotations: arrows, setup/hold marks, text labels, their start and end points;
- the title and any caption;
- every uncertain item, with the reason (blurred, overlapping, cut off).

## Mapping to WaveJSON

| Seen in the image | WaveJSON |
|---|---|
| clock with regular pulses | `p` (rising first) or `n`, then `.` |
| level changes | `0` / `1`, with `.` for no change |
| bus with text | `=` plus `data` label (`2`-`5` for a different color) |
| shaded unknown, tri-state line | `x`, `z` |
| break in the axis | `\|` |
| change between clock edges | finer grid, `phase`, or fractional `period` |
| arrows with labels | `node` letters and `edge` strings |
| brace or box around signals | group array |

## Confirm, draw, compare

1. Send the table and the uncertain items to the user as questions with options (R-005), for example "the third cell of `data` reads 0x1F or 0x1E", and wait for the answers.
2. Write the WaveJSON, run `lint`, build the HTML.
3. Compare the drawing with the original cell by cell and list every difference (font, color and slope shapes cannot be copied exactly) in the report; ask the user to confirm the match.
