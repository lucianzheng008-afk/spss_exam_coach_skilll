# Data Execution Mode

Use this reference when the user sends an SPSS/CSV/Excel dataset together with a题目 and wants Codex to compute the answer directly.

## Goal

Do not guess from the题目 alone when raw data is available. Load the data, audit variables and value labels, decide missing values and recoding direction first, run the matching statistical procedure, then write the Chinese exam answer from computed values.

## Actual SPSS First

When `.sav` data is provided or the user asks to call SPSS:

1. Look for IBM SPSS Statistics before using Python-only computation.
   - macOS common path: `/Applications/IBM SPSS Statistics*/SPSS Statistics.app/Contents/MacOS/stats`
   - Check with `find /Applications -path '*SPSS Statistics.app/Contents/MacOS/stats' -print`.
2. Use a pure ASCII temporary working directory for SPSS production jobs when the project path or data path contains Chinese or other non-ASCII characters. Copy or symlink the `.sav` to an ASCII path such as `/tmp/spss_exam_job/data.sav`.
3. Generate a `.sps` syntax file and a `.spj` production job file. On macOS, passing a `.sps` directly to `stats` often opens the GUI instead of executing the syntax; `.spj -production silent` is the reliable batch route.
4. The syntax must include, in this order:
   - `GET FILE=...`
   - `MISSING VALUES` or recode of non-substantive answers to `SYSMIS`; for more than three adjacent missing codes, use ranges such as `MISSING VALUES q1 (-1, 7 THRU 9).`
   - recoded variables when direction is not intuitive
   - an exclusion analysis and, when feasible, an imputed sensitivity analysis
   - the requested `FREQUENCIES`, `CROSSTABS`, `ONEWAY`, `CORRELATIONS`, `REGRESSION`, etc.
5. Run SPSS with the production job:
   ```bash
   '/Applications/IBM SPSS Statistics 27/SPSS Statistics.app/Contents/MacOS/stats' /tmp/spss_exam_job/job.spj -production silent -nologo
   ```
6. Prefer `outputFormat="text-utf8"` in the `.spj` so the agent can read SPSS tables from a text output file. If SPSS opens a GUI session or does not return machine-readable tables, leave the syntax file for reproducibility and use the Python script to extract exact values from the same data and same recoding rules. Say this clearly in `数据核验`.

Minimal production job:
```xml
<?xml version="1.0" encoding="utf-8"?>
<job xmlns="http://www.ibm.com/software/analytics/spss/xml/production"
     syntaxFormat="batch"
     syntaxErrorHandling="stop"
     print="false"
     unicode="true">
  <locale language="en" country="US" charset="UTF-8"/>
  <output outputPath="/tmp/spss_exam_job/output.txt"
          outputFormat="text-utf8"
          tableColumnSeparator="tab"/>
  <syntax syntaxPath="/tmp/spss_exam_job/job.sps"/>
</job>
```

## Supported Data

- `.sav`: SPSS data, read with `pyreadstat`.
- `.csv`: read with `pandas.read_csv`.
- `.xlsx` / `.xls`: read with `pandas.read_excel`.

Preferred runtime:

`<path-to-python3-if-system-python-lacks-pyreadstat>`

Required packages for full mode: `pandas`, `numpy`, `pyreadstat`, `scipy`, `statsmodels`, `openpyxl`.

Reusable script:

`scripts/spss_exam_analyzer.py`

## High-Accuracy Workflow

1. Save or locate the user's data file.
2. Run an audit first:
   ```bash
   python scripts/spss_exam_analyzer.py --file DATA --analysis audit
   ```
3. Match题目 variables to data columns:
   - Prefer exact column names from the file.
   - Use SPSS variable labels/value labels when `.sav` metadata is available.
   - If two candidate variables are plausible, state the ambiguity and ask only that question.
4. Auto-detect missing-value codes from value labels before manually guessing per variable:
   - For every variable that will enter an analysis, read its SPSS value labels (or codebook text if no `.sav` metadata) and scan label text for keywords meaning non-substantive response: 缺失、不知道、不理解、无法选择、拒答、其他、don't know、cannot choose、decline (to answer)、refused、not applicable、no answer.
   - Treat every value whose label matches one of those keywords as missing for that variable, regardless of its numeric code — codes are not consistent across variables or datasets (e.g. one variable may use `8/9` for "can't choose/decline", another may use `97/98/99`, another may use `-1`). Do not assume a fixed code list applies dataset-wide; check labels per variable.
   - State the detected missing codes per variable in `数据核验` (e.g. `se12: 97/98/99为"不理解/无法选择/拒答"，设为缺失`) so the user can verify the auto-detection was correct.
   - If a variable has no value labels at all (numeric-only data, no metadata), fall back to asking the user or to the题目's stated missing codes.
   - Distinguish **structural missing** from **item-level missing** before doing anything else with a missing variable:
     - Structural missing: the entire column is empty for every case in this file (common in cross-national survey files where a variable is country-specific, e.g. a weight variable that only applies to one other country). This is not "missing data" to exclude or impute — it means the variable does not apply to this file/group at all. Drop it from consideration and say so once; do not run exclusion/imputation logic on it, and do not count its rows against any other variable's missing rate.
     - Item-level missing: some but not all cases lack a valid answer (skipped, declined, don't know, or genuinely blank). This is the kind step 7 below applies to.
   - Report each analysis variable's **missing rate** (missing N / total N) in `数据核验`, not just the missing count. If any analysis variable's item-level missing rate exceeds roughly 20-30%, flag it explicitly (e.g. `se13家庭收入缺失率28%，结果解读时需注明样本代表性可能受限`) before reporting results computed from it — a high missing rate weakens both the exclusion result (smaller effective N) and the imputation result (more values are guessed, not observed).

5. Locate variables by keyword search when the题目 uses concept names but the data uses opaque column names (e.g. `q12`, `se13`):
   - Search every column's variable label (not just the column name) for keywords from the题目's concept (Chinese concept words may need an English equivalent search too, since many cross-national survey codebooks are labeled in English — e.g. "信任行政机构" → search labels for "civil service"/"administration"/"bureaucracy"/"trust").
   - When more than one column label plausibly matches, list all candidates with their full label text and ask the user to confirm, rather than silently picking one.
   - Once confirmed, record the mapping explicitly in `数据核验` (e.g. `"信任行政机构" -> q12 "Civil service"`) so later steps and the final answer use a traceable variable name, not just the concept name.
   - For a recurring course/survey (e.g. the same cross-national questionnaire reused across multiple country files), keep the confirmed concept-to-column mapping consistent across all files in the same task instead of re-deriving it per file.

6. For every analysis variable, decide whether it needs recoding before any calculation:
   - Mandatory default: low end = smaller/weaker/less/negative/pejorative; high end = larger/stronger/more/positive/commendatory.
   - If labels say the opposite, create a new variable and analyze the new variable.
   - Examples: `1=影响非常大 ... 4=没有影响` must reverse to larger = greater influence; `1=非常积极 ... 6=非常消极` must reverse to larger = more positive.
   - Mark non-substantive codes as missing first: 缺失、不知道、不理解、无法选择、拒答、其他、don't know、refused、no answer. (This duplicates step 4's keyword scan — step 4 is now the authoritative source for which codes are missing; this step is about recoding direction, not about re-deriving missing codes.)
7. Decide missing-value treatments:
   - **Default when the题目/user doesn't specify which treatment to use: present both the exclusion (listwise/pairwise deletion) result and the imputed result as two equally complete, equally labeled answers — not one primary + one footnote.** The user often does not know which one their instructor expects, so the default output should be a side-by-side pair (e.g. two small tables or two consecutive equation/coefficient blocks, each clearly headed `剔除缺失值版本` and `插补缺失值版本`), each carried all the way through to its own full conclusion sentence, so either one can be copied as the final answer depending on what's expected.
   - Only collapse to a single result when the题目 explicitly states a treatment (e.g. "请筛除缺失值后处理" or "请用均值替补缺失值") — in that case follow the题目's instruction and skip the other variant, since the题目 already settled the question.
   - When both are given, also state plainly whether they lead to the same substantive conclusion or differ (reuse the divergence-flagging rule below) so the user immediately knows whether the choice of treatment matters for their answer.
   - Default single ordered survey item imputation: median after recoding.
   - Roughly continuous variables: median if skewed/outliers, mean if approximately symmetric.
   - Nominal categorical variables: mode imputation only as a sensitivity check; do not treat it as the primary answer unless the question asks for it.
   - **Do not impute the dependent variable / outcome being tested by default.** Imputing the DV with its own mean/median artificially shrinks its variance and can inflate or deflate significance tests in either direction depending on the method — this biases the very thing being tested. Default imputation sensitivity should only fill in missing **predictors/covariates/independent variables**; if the题目 specifically asks for DV imputation, do it but label the result as following that explicit instruction, not as the skill's own default.
   - Deletion method depends on the method, not a single dataset-wide default:
     - Regression (`REGRESSION`/`UNIANOVA` with multiple predictors), one-way ANOVA, chi-square: use **listwise** deletion — every case must have valid values on all variables entering that specific model, so the N is identical across every coefficient/cell in that one output.
     - A bivariate correlation **matrix** with several variable pairs computed in one `CORRELATIONS` call: **pairwise** deletion is acceptable and is SPSS's default — each pair's N can differ, and that is expected, not an error. State the per-pair N if it varies noticeably across pairs in the same matrix.
     - Never mix listwise results from one run with pairwise results from another inside the same comparison table without flagging that the Ns differ for that reason.
   - Report valid/excluded N and imputed N separately for every variant reported.
   - After computing both the exclusion result and the imputed sensitivity result, compare them: if a coefficient's sign flips, a `Sig.` crosses the .05 threshold in either direction, or an effect-size band changes (e.g. weak vs strong) between the two, flag this divergence explicitly and clearly. When the题目 has explicitly settled on one treatment (step 7's first bullet), follow that one. When neither was specified and both are shown side by side, do not silently rank one above the other — state the divergence and let the user decide which one matches their instructor's expectation; only default to favoring the exclusion result if the user asks which one to trust more without further context.
8. Check variable measurement levels:
   - few unique numeric/text categories -> categorical
   - ordered Likert-style numeric variable -> ordinal, often acceptable for Spearman or scale computation
   - many numeric values -> continuous
9. Run SPSS syntax first when SPSS is installed; otherwise run the needed calculation with the script.
10. Sanity-check every computed statistic before writing it into the answer (see "Result Sanity Checks" below) — catch and flag implausible values instead of reporting them at face value.
11. Write the answer using the standard Response Contract:
   - method choice
   - principle
   - SPSS menu path
   - exact computed output values
   - result interpretation and inference
   - exam-ready conclusion

## Script Commands

Audit:
```bash
python scripts/spss_exam_analyzer.py --file DATA --analysis audit
```

Descriptive statistics:
```bash
python scripts/spss_exam_analyzer.py --file DATA --analysis desc --vars var1 var2
```

Recoded descriptive statistics:
```bash
python scripts/spss_exam_analyzer.py --file DATA --analysis recode-desc --vars var1 --missing-values -1 7 8 9 --direction high-to-low
```

Use `--direction high-to-low` when the original high values have smaller/weaker/more negative meanings and must be reversed. Use `--direction low-to-high` when the original direction is already correct.

Recoded descriptive statistics with median imputation sensitivity:
```bash
python scripts/spss_exam_analyzer.py --file DATA --analysis recode-desc --vars var1 --missing-values -1 7 8 9 --direction high-to-low --impute median
```

Chi-square:
```bash
python scripts/spss_exam_analyzer.py --file DATA --analysis chi2 --iv group_var --dv outcome_var
```

One-way ANOVA:
```bash
python scripts/spss_exam_analyzer.py --file DATA --analysis anova --iv group_var --dv continuous_var
```

Correlation:
```bash
python scripts/spss_exam_analyzer.py --file DATA --analysis corr --x var1 --y var2 --corr-method pearson
python scripts/spss_exam_analyzer.py --file DATA --analysis corr --x var1 --y var2 --corr-method spearman
```

Partial correlation:
```bash
python scripts/spss_exam_analyzer.py --file DATA --analysis partial-corr --x var1 --y var2 --controls control1 control2
```

Linear regression:
```bash
python scripts/spss_exam_analyzer.py --file DATA --analysis regression --dv y --predictors x1 x2 x3
```

## Result Sanity Checks

Before writing any computed statistic into the answer, check it against these implausibility signals. If a value trips one of these, say so explicitly in `数据核验` or right next to the number (e.g. `调整后R²为负值，提示该模型几乎没有解释力，结果如实保留`) — do not silently report an implausible number as if it were unremarkable, and do not "fix" it by re-running with different specifications unless the题目 asks for a different model.

- `Adjusted R²` negative, or `Adjusted R²` noticeably larger than `R²`: with few predictors and reasonable N this should not happen; flag and double-check predictor count/N/listwise deletion.
- Any standardized `Beta` with `|Beta| > 1`: almost always signals severe multicollinearity or a near-deterministic relationship (e.g. a predictor that is a rescaled version of another predictor or of the DV).
- `VIF > 20` or `Tolerance < .05`: collinearity severe enough that individual coefficients are likely unstable; say this even if the题目 only asked for the coefficient, not the diagnostic.
- `Durbin-Watson` far from 2 (roughly `< 1` or `> 3`) on cross-sectional (non-time-series) data: unexpected — re-check whether cases are sorted/grouped in a way that creates artificial ordering; on genuine time-series data this is expected and should be reported as a LINE/independence violation, not an error.
- Group `N` in ANOVA/post-hoc under ~5: flag the group as too small for a stable mean/post-hoc comparison even if SPSS still produces a p-value for it.
- A model `Sig. >= .05` (not significant) but the题目's answer template assumes significance: report the null result as-is using the 不显著 template; do not force a significant-sounding interpretation onto a non-significant model (this was a real case: an exercise's regression model was not significant, and the correct answer was "no predictor can be interpreted," not a forced explanation).
- A correlation/coefficient `|r|` or `|Beta|` that is implausibly close to 1 (e.g. > .95) outside of known near-deterministic relationships: double check for a coding/duplication error (e.g. accidentally regressing a variable on a rescaled copy of itself) before reporting it as a strong substantive finding.

## Accuracy Rules

- Always audit before analyzing a new dataset.
- Always judge recoding before analyzing any dataset. Do not wait for the题目 to say "重新编码".
- Always consider both missing-value exclusion and imputation when raw data are available; label which one is primary; flag any meaningful divergence between the two instead of silently picking the more favorable one.
- Always report valid `N` and each analysis variable's missing rate; use listwise deletion for any single multi-variable model (regression, ANOVA, chi-square) and pairwise deletion only for a standalone bivariate correlation matrix.
- Do not impute the dependent variable by default; imputation sensitivity targets predictors/covariates unless the题目 explicitly asks to impute the DV.
- Do not treat a column that is structurally empty for the entire file (e.g. a country-specific variable in a cross-national dataset) as item-level missing data — name it once as not applicable to this file and exclude it from missing-rate/imputation logic entirely.
- Do not silently choose among ambiguous variables.
- Do not treat coded missing values such as `8`, `9`, `99`, `999` as real answers if labels or codebook say they mean missing/refused/unknown.
- Do not interpret means or coefficients from reversed labels. Recode so that low values are small/negative/pejorative and high values are large/positive/commendatory.
- For categorical predictors in regression, the script dummy-codes with one reference category dropped; mention the reference group if visible from variable coding.
- For ANOVA, report Levene's p before choosing ordinary ANOVA/post-hoc wording.
- For chi-square, report expected-count warnings when more than 20% of cells have expected counts below 5.
- If the script result and SPSS screenshot disagree, first check missing-value definitions, filters, weights, value labels, and listwise/pairwise deletion.
