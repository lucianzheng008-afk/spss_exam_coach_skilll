# Result Interpretation Principles

Use this reference when an SPSS exam answer needs principles, automatic result description, or inference from output values. Keep the final answer in Chinese and exam-oriented.

## "为什么" Explanation Requirement

Whenever a题目 asks 为什么/请说明理由/请解释/为什么是这个结果 (including embedded inside a sub-question like "哪个自变量解释度最高？为什么？"), the answer must give a **full causal chain**, not a one-clause label. A bare restatement of the number (e.g. "因为Beta最大") is insufficient on its own — always state which statistic is the deciding criterion, why that statistic (and not a related-looking one) is the correct criterion, and what about the textbook/course principle makes it the correct criterion. Structure every "为什么" answer in three layers:

1. **结论**：直接给出答案本身（哪个变量/哪组/显著或不显著）。
2. **判断依据**：点名用来做判断的具体统计量（如标准化Beta、Sig.、Levene、Adjusted R²、Cramer's V），并给出它的数值。
3. **原理性理由**：解释为什么该统计量、而不是另一个看起来相关的统计量，是正确依据 — 引用该方法的核心逻辑（例如："比较自变量相对影响力要用标准化Beta而不是未标准化B，因为不同自变量的原始单位不同，B的大小受量纲影响，Beta去除了量纲，才能跨变量比较"；"判断模型是否显著要看ANOVA的F和Sig.，而不是R²，因为R²只描述拟合优度，不直接提供显著性检验的p值"）。When `textbook-ocr-notes.md` or `textbook-integration.md` has a paraphrased principle that matches, align the wording with that paraphrase instead of inventing a different justification.

Apply this same three-layer depth to comparative/superlative questions even without the literal word "为什么" — e.g. "哪个自变量解释度最高/最低"，"哪两组差异显著/不显著"，"是否满足方差齐性" all implicitly require stating the deciding statistic and the principle behind using it, not just the answer.

Do not pad with repeated generic statistics caveats (avoid restating "相关不等于因果" in every single sub-answer if it was already stated once for the same block) — depth means a complete, specific causal chain for *this* question, not boilerplate repetition.

## Universal Reading Logic

Read SPSS output in this order:

1. `N/Valid/Missing`: confirm how many cases entered the analysis.
2. Descriptive layer: frequencies, percentages, means, SD, group means, or scatter direction.
3. Assumption layer when relevant: expected counts, Levene, normality/linearity, collinearity.
4. Significance layer: `Sig.` / `p`.
5. Effect layer: Phi/Cramer's V, eta squared, `r/ρ`, `R²/Adjusted R²`, `B`, `Beta`.
6. Conclusion layer: state sample pattern, statistical inference, substantive meaning, and limitation.

Default inference wording:

- `p < .05`: `拒绝零假设，认为该关系/差异/模型/系数具有统计显著性。`
- `p >= .05`: `不能拒绝零假设，现有样本不足以说明该关系/差异/模型/系数显著。`
- Do not write `接受零假设` unless a teacher explicitly requires that wording.

## Significant Does Not Mean Strong

`Sig. < .05` and effect size are independent dimensions — always report both, and never let a small `Sig.` imply a large or substantively important effect. This applies to every method with both a significance test and an effect-size statistic: chi-square (`Sig.` vs Phi/Cramer's V), ANOVA (`Sig.` vs eta squared), correlation (`Sig.` vs `r`/`ρ`), regression (model `Sig.` vs `R²`/`Adjusted R²`; coefficient `Sig.` vs `Beta`).

- Large N makes it easy for a trivially small effect to reach `Sig. < .05` (this happens often in survey data with N in the hundreds or thousands, which is common in this course's datasets). A significant model/coefficient with weak effect size is a real, reportable pattern, not a contradiction to resolve.
- When effect size falls in the weak band for that method (`Adjusted R²` roughly `< .10`, `|r|`/`|Beta|` roughly `< .30`, Cramer's V/Phi `< .30`, eta squared `< .06`) while `Sig. < .05`, add an explicit one-sentence qualifier to the conclusion: `结果统计显著，但效应量很小（如XX=...），说明该关系/模型在统计上成立，但实质解释力或预测力有限，不应过度强调其重要性。`
- When effect size is in the strong band (`Adjusted R²` roughly `> .50`, `|r|`/`|Beta|` roughly `> .50`, Cramer's V/Phi `> .50`, eta squared `> .14`) and also significant, it is fine to state both facts together without the weak-effect qualifier — do not pad a genuinely strong result with unnecessary hedging.
- Never substitute "significant" for "important" or "large" in Chinese wording — avoid writing `显著的影响` when meaning size alone is being described; say `统计显著但效应较小的影响` if that is what the numbers show.

## Description vs Inference vs Meaning

Every conclusion should separate three ideas:

- Description: `样本中，A 组的均值/比例高于 B 组。`
- Inference: `Sig.=...，因此该差异达到/未达到 .05 显著性水平。`
- Meaning: `这说明变量 A 与 B 之间存在/暂未发现统计显著关联；但不能仅凭该检验证明因果关系。`

If output values are supplied, write concrete sentences. If values are absent, give blanks.

## Method Principles

### Descriptive Statistics

Principle: 描述统计不检验假设，主要概括样本分布。分类变量看频数和百分比；连续变量看中心趋势和离散程度。

Automatic wording:

- Categorical: `频率表显示，变量 X 中占比最高的类别是...，占...%，说明样本主要集中在该类别。`
- Continuous: `变量 X 的均值为...，标准差为...；均值表示总体水平，标准差越大说明个体差异越大。`
- Skew/outlier: `若均值和中位数差距较大或箱图有极端点，应补充中位数并谨慎解释均值。`

### Recode And Compute

Principle: 重编码改变变量取值含义；计算变量把多个题项或已有变量按规则合成为新指标。考试重点是保留原变量、说明转换规则、验证新变量。

Automatic wording:

`本题先将 X 重新编码为 X_new，使数值越大表示...。随后用...公式计算 Y。完成后通过频率/描述统计检查新变量取值范围是否正确。`

### Missing Values And Outliers

Principle: 缺失值影响有效样本量，偏离值会拉动均值、相关、回归和方差分析。处理前先识别，处理后再复查。

Automatic wording:

`频率/箱图显示 X 存在...个缺失/偏离值。若题目要求处理，可将非实质编码设为用户缺失，或按题目指定方法替换缺失值。处理后需重新运行描述统计确认结果。`

### Chi-Square

Principle: 卡方检验比较观察频数和独立性假设下期望频数的差距。零假设是两个类别变量相互独立。

Automatic wording:

- Significant: `Pearson Chi-Square 的 Sig.=... < .05，拒绝独立性零假设，说明 A 与 B 存在统计显著关联。Cramer's V/Phi=...，关联强度为...。从交叉表看，...组在...类别上的比例更高。`
- Not significant: `Sig.=... >= .05，不能拒绝独立性零假设，现有样本不足以说明 A 与 B 有统计显著关联。`

Strength guide: `< .30` weak, `.30-.70` moderate, `> .70` strong. Use Phi for `2 x 2`; use Cramer's V for larger tables.

Assumption wording:

`若超过 20% 单元格期望频数小于 5，卡方结果不稳，应考虑合并类别、增加样本，或在适合的 2 x 2 表中看 Fisher/Yates。`

### One-Way ANOVA

Principle: ANOVA 比较组间差异相对于组内差异是否足够大。零假设是各组总体均值相等。`F` 越大通常表示组间差异相对组内误差越大。

Automatic wording:

- Homogeneity: `Levene Sig.=... > .05，方差齐性假定基本满足；若 < .05，优先看 Welch/Brown-Forsythe，并选择不等方差事后检验。`
- Significant: `ANOVA 表显示 F(df1, df2)=...，Sig.=... < .05，说明不同 A 组在 B 的均值上存在显著差异。描述统计中...组均值最高，...组均值最低。事后检验显示...组与...组差异显著。`
- Not significant: `Sig.=... >= .05，不能认为不同 A 组在 B 上存在显著均值差异；即使样本均值有高低，也不足以推论总体差异显著。`

Effect wording: `eta squared=...，表示 A 可解释 B 总变异的约...%。`

### Correlation And Partial Correlation

Principle: 相关分析衡量两个变量同向或反向共同变化的程度。零假设是总体相关系数为 0。偏相关是在控制变量后看两个核心变量的净相关。

Automatic wording:

- Positive: `r/ρ=... > 0，说明 A 越高，B 越高。`
- Negative: `r/ρ=... < 0，说明 A 越高，B 越低。`
- Significant: `Sig.=... < .05，该相关达到统计显著。`
- Not significant: `Sig.=... >= .05，不能认为二者存在稳定相关；不要只根据 r 的正负下结论。`
- Partial: `控制 C 后，A 与 B 的偏相关为...，p=...，说明二者关系在排除 C 的线性影响后仍然显著/不再显著。`

Strength guide for `|r|`: `< .30` weak, `.30-.50` low/moderate, `.50-.80` strong, `>= .80` very high. Correlation does not prove causality.

### Multiple Linear Regression

Principle: 多元线性回归估计多个自变量在彼此控制后的独立预测作用。模型显著性看整体是否有解释力，系数显著性看某个自变量是否有独立作用。

Reading order:

1. Model Summary: `R Square`, `Adjusted R Square`.
2. ANOVA: model `F` and `Sig.`.
3. Coefficients: constant, `B`, `Beta`, `t`, `Sig.`, `Tolerance`, `VIF`.

Automatic wording:

- Model: `模型整体显著，F=...，p=...；调整后 R²=...，说明模型可解释因变量约...% 的变异。`
- Coefficient: `在控制其他变量后，X 对 Y 有显著正/负向影响，B=...，p=...。这表示 X 每增加 1 个单位，Y 平均增加/减少...个单位。`
- Relative importance: `标准化 Beta 的绝对值越大，说明相对影响越强；不同单位变量不要直接比较未标准化 B。`
- Non-significant predictor: `X 的 Sig.=... >= .05，说明在控制其他变量后，X 的独立预测作用不显著。`
- Equation: `根据未标准化系数，回归方程为 Y = 常量 + B1X1 + B2X2 + ...。`
- Collinearity: `VIF < 5 通常问题较小；VIF > 10 或 Tolerance < .10 表明严重共线性，需要谨慎。`

Avoid causal language unless the design justifies it. Prefer `预测/解释/相关影响`.
