# Last-Year Real Exam Patterns

Use this reference when the user mentions 去年真题、真题、往年题、模拟题、仿题、照着出题, or provides screenshots asking for blanks around government/administrative-institution trust, regression interpretation, ANOVA, or post-hoc pairwise comparisons.

## Captured Real Exam Shape

The supplied screenshots contain two connected question blocks.

### Block A: Multiple Linear Regression

Substantive topic:

- 韩国民众对行政机构的信任.
- Dependent variable: `信任行政机构` / `对行政机构的信任`.
- Predictors shown in the prompt: 性别、教育、主观的社会地位、家庭收入.

Expected questions:

1. Which predictors are significant, and why?
2. For significant predictors, state whether each relationship is positive or negative.
3. Which predictor has the highest explanatory power, and why?
4. Which significant predictor has the lowest explanatory power, and why?
5. Write the regression equation for dependent variable `信任行政机构`.

Reading order:

1. `Model Summary`: read `R Square` and `Adjusted R Square` only if asked about overall explanation.
2. `ANOVA`: read `F` and `Sig.` to judge whether the whole regression model is significant.
3. `Coefficients`: read each predictor's `Sig.`, unstandardized `B`, standardized `Beta`, and optionally `VIF`.

Answer rules:

- Significant variables are those with coefficient-table `Sig. < 0.05`.
- Direction comes from the sign of `B` or `Beta`: positive means 正相关, negative means 负相关.
- Highest explanatory power means the largest absolute standardized coefficient `|Beta|`, not the largest `B`.
- Lowest explanatory power among significant predictors means the smallest absolute `|Beta|` after excluding nonsignificant variables.
- Do not include nonsignificant variables when answering “解释度最低（不显著的自变量除外）”.
- Regression equation uses unstandardized coefficients:
  `信任行政机构 = 常数项 + B1*性别 + B2*教育 + B3*主观社会地位 + B4*家庭收入`.
- If a predictor is categorical and dummy-coded, name the reference category when visible. If not visible, avoid over-interpreting group meaning.

Copyable wording:

`根据系数表，变量 X 的 Sig.=...，小于 0.05，因此 X 对“信任行政机构”的影响显著。其 B/Beta 为正/负，说明 X 与行政机构信任呈正/负相关。`

`在显著变量中，X 的标准化系数 Beta 绝对值最大，因此解释度最高；Y 的 Beta 绝对值最小，因此解释度最低。`

`回归方程为：信任行政机构 = a + b1*性别 + b2*教育 + b3*主观社会地位 + b4*家庭收入。`

### Block B: One-Way ANOVA And Post-Hoc Pairwise Comparison

Substantive topic:

- Compare group differences in government trust.
- Prompt asks “哪个组对政府的信任度最高”, “哪两组之间差异显著”, and “哪两组之间差异不显著”.

Expected questions:

4. Which group has the highest trust in government?
5. Which two group pairs differ significantly?
6. Which two group pair does not differ significantly, and why?

Reading order:

1. `Descriptives` or means table: read group `Mean`.
2. `Test of Homogeneity of Variances`: read Levene `Sig.` to choose post-hoc logic.
3. `ANOVA`: read `F` and `Sig.` to decide whether at least one group mean differs.
4. `Multiple Comparisons`: read pairwise `Sig.` values.

Answer rules:

- Highest government trust group is the group with the largest mean in descriptive statistics.
- Significant pairwise differences are pairs with post-hoc `Sig. < 0.05`.
- Nonsignificant pairwise differences are pairs with post-hoc `Sig. >= 0.05`.
- Reason for nonsignificance: `Sig.` is greater than or equal to 0.05, so fail to reject equal-means null hypothesis; do not say “证明没有差异”.
- If ANOVA is not significant, do not hunt for significant pairwise pairs as the main conclusion; state no overall significant difference.

Copyable wording:

`根据描述性统计结果，均值最高的是 X 组，因此该组对政府的信任度最高。`

`根据事后两两比较结果，X 组与 Y 组的 Sig.=...，小于 0.05，因此二者差异显著。`

`X 组与 Y 组的 Sig.=...，大于/等于 0.05，因此二者差异不显著，只能说样本中均值有差别，但统计上没有足够证据认为总体均值不同。`

## Exam-Filling Priority

When the user supplies screenshots or tables for this real-exam pattern, answer blanks directly:

1. Extract exact values from the visible SPSS output.
2. Fill blanks first.
3. Then give one-sentence reasons using `Sig.`, `Mean`, `B`, and `Beta`.
4. Keep wording short and exam-like.

Never invent group names or coefficient values not visible in the provided output. If only the blank-question screenshot is supplied without SPSS tables, give the method and fill-in template instead of pretending to know the values.

## Simulation-Question Generation

When the user asks to 模仿去年真题出模拟题, generate practice questions that preserve the same cognitive operations, not the same surface wording only.

Default structure:

1. Regression interpretation block with 5 blanks/questions:
   - Identify which predictors significantly affect the dependent variable.
   - State whether significant effects are positive or negative.
   - Identify the predictor with the highest explanatory power using `|Beta|`.
   - Identify the significant predictor with the lowest explanatory power, excluding nonsignificant predictors.
   - Write the regression equation with unstandardized `B`.
2. ANOVA/post-hoc block with 3 blanks/questions:
   - Identify the group with the highest mean.
   - Identify significant pairwise differences using post-hoc `Sig. < 0.05`.
   - Identify nonsignificant pairwise differences using post-hoc `Sig. >= 0.05` and give the reason.

Default simulated topic options:

- Political trust: 信任政府、信任行政机构、信任议会、信任法院.
- International perception: 对某国地区影响力评价、对某国好感度、对某国威胁认知.
- Social attitude: 民主满意度、国家认同、政策支持度.

For each simulation set, include:

- A compact SPSS-like output table with enough values to answer.
- The student question sheet with blanks.
- A separate answer key unless the user asks for questions only.

SPSS-like output must be internally consistent:

- Regression coefficient table needs `B`, `Beta`, `t`, and `Sig.` for each predictor.
- Model table may include `R Square`, `Adjusted R Square`, `F`, and model `Sig.`.
- ANOVA practice needs a descriptives/means table and a multiple-comparisons table.
- Make at least one predictor nonsignificant so the student must exclude it.
- Make at least two significant pairwise comparisons and at least one nonsignificant pairwise comparison when there are four groups, matching the last-year blank format.

Difficulty controls:

- Easy: 3 predictors, 3 groups, obvious `Sig.` values.
- Standard: 4 predictors, 4 groups, mixed significant/nonsignificant results. Use this by default.
- Hard: include dummy variables, close `Sig.` values such as `.047` and `.052`, and ask for reference-category interpretation.

Copyable generation prompt:

`请根据以下 SPSS 输出回答问题。显著性标准为 0.05。注意：解释度比较看标准化系数 Beta 的绝对值；回归方程使用未标准化系数 B；事后比较看 Sig.。`

Do not make simulation questions require calculations that are not supported by the shown output. The goal is exam-style table reading, not hidden arithmetic.
