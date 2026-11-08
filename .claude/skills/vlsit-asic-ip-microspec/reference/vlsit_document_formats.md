# Specification source and export formats

## Authoritative source

Keep the design specification in the bundled Markdown template. Edit the `.md` file; treat DOCX and PDF as generated review or sharing copies. Keep figures in the adjacent `figures/` directory and link them with relative paths:

```markdown
![Block diagram](figures/block_diagram.svg)
```

Write equations with Pandoc-supported TeX math. Use `$...$` inline and `$$...$$` on separate lines for display equations:

```markdown
The output rate is $f_{out}=f_{clk}/N$.

$$
T_{frame}=\frac{N_{cycles}}{f_{clk}}
$$
```

Pandoc converts TeX math in DOCX to native Word OMML equations. Keep dollar delimiters adjacent to the equation text; avoid using dollar-delimited currency expressions as math.

## DOCX export

Use the export script so the Markdown extensions, relative figures and output paths are handled consistently:

```powershell
<python> "<skill folder>\scripts\vlsit_spec_export.py" export "VLSIT_AES_HDS.md" --format docx
```

An optional Word reference document can supply paragraph, character and table styles:

```powershell
<python> "<skill folder>\scripts\vlsit_spec_export.py" export "VLSIT_AES_HDS.md" --format docx --reference-doc "<Word style template.docx>"
```

Do not claim that a DOCX matches a company's Word template unless that reference document was actually used. Without one, Pandoc's default DOCX styles apply.

## PDF export

Pandoc needs a PDF engine to make a PDF. The default for this skill is Typst; select an installed alternative with `--pdf-engine` if required:

```powershell
<python> "<skill folder>\scripts\vlsit_spec_export.py" export "VLSIT_AES_HDS.md" --format pdf
<python> "<skill folder>\scripts\vlsit_spec_export.py" export "VLSIT_AES_HDS.md" --format pdf --pdf-engine xelatex
```

The first command needs both `pandoc` and `typst` on `PATH`. Pandoc alone is sufficient for DOCX, but not PDF. The script reports a missing executable and does not install software.

## Both exports

Request both formats together, keeping the Markdown source beside the generated copies:

```powershell
<python> "<skill folder>\scripts\vlsit_spec_export.py" export "VLSIT_AES_HDS.md" --format all
```

By default the outputs use the same basename as the Markdown file and are written beside it. Use `--output-dir` for another destination. The script refuses to replace existing exports unless `--force` is supplied; obtain the user's approval before using `--force` on files not created in the current run.

References: [Pandoc User's Guide: Math](https://pandoc.org/MANUAL.html#math), [Pandoc User's Guide: DOCX](https://pandoc.org/MANUAL.html#option--reference-doc), [Pandoc User's Guide: PDF](https://pandoc.org/MANUAL.html#option--pdf-engine), [Pandoc installation](https://pandoc.org/installing.html).
