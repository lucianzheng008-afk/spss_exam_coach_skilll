# spss-exam-coach

A Claude Code skill that turns an SPSS 操作考试题目, pasted SPSS output table, or raw dataset into a direct, exam-ready answer: method choice, core principle, exact SPSS menu steps, full runnable syntax, output-table reading order, automatic result wording, statistical inference, and common pitfalls.

It is built around China's 国际关系量化研究方法 (Pang Qin) course structure — chi-square, ANOVA, correlation/partial correlation, and multiple linear regression — but the operational SPSS guidance generalizes to any course covering the same methods.

## What it does

- Picks the right method from variable types and the question's wording (描述统计 / 重新编码 / 卡方检验 / 单因素ANOVA / 相关与偏相关 / 多元线性回归).
- For questions with multiple sub-parts (①②③ / 1.2.3. / multiple blocks), lists every sub-question up front and answers each one explicitly, instead of merging or skipping any.
- Gives paired, fully detailed SPSS guidance for every method: numbered menu-click steps (exact path, which variable goes in which box, every checkbox relevant to that question) plus a complete, directly runnable syntax block covering the same operations.
- Tells you which output table and which exact statistic to read, in the right order.
- Translates `Sig.`, `r`/`ρ`, `F`, `B`/`Beta`, `VIF` into a natural-language conclusion, separating significance from effect size (a small, real-world distinction this skill enforces: significant does not mean strong) and description from inference.
- For "为什么"/comparative questions, requires a three-layer answer (结论 → 判断依据的统计量 → 该统计量为何正确的原理) instead of a bare number.
- Provides fill-in-the-blank exam answer templates (significant and non-significant versions).
- Lists high-value mistakes to avoid for each method.
- If given a raw `.sav`/`.csv`/`.xlsx` dataset: auto-detects missing-value codes from each variable's value labels (not a fixed code list), locates concept-named variables by searching column labels, audits recoding direction, runs the actual analysis (via installed IBM SPSS Statistics syntax when available, or `scripts/spss_exam_analyzer.py` as a Python fallback), sanity-checks the computed numbers for implausible values (negative adjusted R², |Beta| > 1, severe VIF, etc.) before reporting them, and reports real numbers instead of placeholders.

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
  result-interpretation-principles.md     # method principles, hypothesis logic, result wording, sig-vs-effect-size rules
  data-execution-mode.md                  # how to run real data: missing-code detection, variable lookup, sanity checks
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

This skill deliberately avoids storing or reproducing long verbatim excerpts from any textbook or past exam. Textbook-derived reference files contain paraphrased summaries (principles, formulas, thresholds, worked-example logic) rather than copied prose, tables, or exercises, and the past-exam reference abstracts question *patterns* rather than storing the original question text. If you contribute textbook or exam notes, please keep the same paraphrase-only convention.

## License

MIT — see `LICENSE`.
