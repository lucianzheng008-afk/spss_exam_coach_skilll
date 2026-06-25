# spss-exam-coach

A Claude Code skill that turns an SPSS 操作考试题目, pasted SPSS output table, or raw dataset into a direct, exam-ready answer: method choice, core principle, exact SPSS menu steps, output-table reading order, automatic result wording, statistical inference, and common pitfalls.

It is built around China's 国际关系量化研究方法 (Pang Qin) course structure — chi-square, ANOVA, correlation/partial correlation, and multiple linear regression — but the operational SPSS guidance generalizes to any course covering the same methods.

## What it does

- Picks the right method from variable types and the question's wording (描述统计 / 重新编码 / 卡方检验 / 单因素ANOVA / 相关与偏相关 / 多元线性回归).
- Gives exact SPSS menu paths, which variable goes in which box, and which buttons to click.
- Tells you which output table and which exact statistic to read, in the right order.
- Translates `Sig.`, `r`/`ρ`, `F`, `B`/`Beta`, `VIF` into a natural-language conclusion, separating significance from strength and description from inference.
- Provides fill-in-the-blank exam answer templates (significant and non-significant versions).
- Lists high-value mistakes to avoid for each method.
- If given a raw `.sav`/`.csv`/`.xlsx` dataset, audits recoding direction and missing values, runs the actual analysis (via installed IBM SPSS Statistics syntax when available, or `scripts/spss_exam_analyzer.py` as a Python fallback), and reports real numbers instead of placeholders.

## Installation

Copy this folder into your Claude Code skills directory:

```bash
cp -r spss-exam-coach ~/.claude/skills/
```

Claude Code will pick it up automatically; invoke it with `/spss-exam-coach` or by describing an SPSS exam question.

## Structure

```
SKILL.md                                  # entry point: response contract + workflow
references/
  spss-operation-map.md                   # generic SPSS menu paths, output tables, rules, templates
  result-interpretation-principles.md     # method principles, hypothesis logic, result wording
  data-execution-mode.md                  # how to run real data when a .sav/.csv/.xlsx is provided
  textbook-integration.md                 # how to align answers with your own textbook (see below)
  textbook-ocr-notes.md                   # paraphrased, exam-relevant textbook notes (see below)
  classroom-review-v2.md                  # open-book review / quick-reference structures
  last-year-real-exam.md                  # abstracted patterns from a past real exam (no literal exam text)
scripts/
  spss_exam_analyzer.py                   # Python fallback for computing/auditing stats when SPSS isn't available
agents/
  openai.yaml                             # optional agent config
```

## Using your own textbook

`textbook-integration.md` and `textbook-ocr-notes.md` are written for one specific textbook (庞琴《国际关系量化研究方法》) with paths to that user's local PDF/OCR files. If you adapt this skill for your own course:

1. Replace the placeholder paths (`<path-to-your-textbook-...>`) in `textbook-integration.md` and `textbook-ocr-notes.md` with paths to your own textbook PDF/OCR export, or delete those two files if you don't need textbook alignment.
2. Re-summarize your textbook's chapter content in your own words in `textbook-ocr-notes.md` — do not paste long verbatim passages; keep it to exam-relevant operational points (method, conditions, SPSS reading order, thresholds), as the existing entries do.
3. `spss-operation-map.md` and `result-interpretation-principles.md` are textbook-agnostic and should work for any course covering chi-square, ANOVA, correlation, and multiple linear regression.

## Notes on copyright

This skill deliberately avoids storing or reproducing long verbatim excerpts from any textbook. Textbook-derived reference files contain paraphrased summaries (principles, formulas, thresholds, worked-example logic) rather than copied prose, tables, or exercises. If you contribute textbook notes for a different book, please keep the same paraphrase-only convention.

## License

MIT — see `LICENSE`.
