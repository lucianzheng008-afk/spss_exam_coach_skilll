# Textbook OCR Notes

Source: `<path-to-your-textbook-ocr-markdown>`

Use this reference only to align SPSS exam answers with 庞琴《国际关系量化研究方法》. Keep answers operational; do not quote long textbook passages.

## OCR Status

- Full OCR Markdown exists and is readable.
- Relevant chapters found: Chapter 6 SPSS basics, Chapter 7 chi-square, Chapter 8 ANOVA, Chapter 9 correlation.
- Chapter 10 linear regression: a separate clean OCR export was supplied on 2026-06-25 (`<path-to-your-chapter10-ocr-markdown>`, plus an `images/` folder of the same screenshots referenced inside it). This export is readable and complete; its content is summarized in the "Chapter 10: Linear Regression" section below. The original combined-textbook OCR mentioned in the line above is still incomplete for this chapter — prefer the dedicated Chapter 10 export when exact wording or example numbers are needed.
- Images are stored in `<path-to-your-textbook-ocr-images>` (other chapters) and in the Chapter 10 export's own `images/` subfolder (Chapter 10 figures).

## Descriptive Statistics And Data Cleaning

- Before formal hypothesis testing, describe each main variable's distribution to decide later analysis strategy.
- Continuous variables: report mean, median, mode if useful, quartiles, SD, variance, range, min, max; use histogram for distribution and possible outliers.
- Categorical variables: report frequency and percentage; use bar chart.
- Median is less sensitive than mean to extreme values; if a distribution has outliers or skew, mention median as a more robust center.
- SPSS route for central tendency: `分析 -> 描述统计 -> 频率 -> 统计`, then choose mean, median, mode, quartiles/percentiles as needed.
- SPSS route for dispersion: `分析 -> 描述统计 -> 频率 -> 统计`, then choose standard deviation, variance, range, min, max.
- Histogram route: `图形 -> 旧对话框 -> 直方图`; choose the continuous variable and add title if needed.
- Boxplot route: `图形 -> 旧对话框 -> 箱图 -> 单独变量的摘要`; put the target continuous variable into the boxplot field.
- Missing values can be system missing or user-defined missing. In variable view, define impossible codes such as `8`, `9`, `99`, `999` as missing when they are not substantive answers.
- Missing handling: deletion can be listwise or pairwise; imputation can be used when missingness is limited. The textbook highlights multiple imputation as a principled approach, but exam operations may use the method specified by the question.
- Outliers affect regression and ANOVA; identify them with frequency/histogram or boxplot before final analysis.

## Compute And Recode

- Compute variables: `转换 -> 计算变量`; enter a target variable and a numeric expression. Use it for sums, means, transformations, and derived indicators.
- Recode: `转换 -> 重新编码`. Prefer `重新编码为不同变量` so the original variable remains intact.
- For categorical recoding, map old values into new categories. Example: alliance levels `5,4 -> 2`; `3,2,1 -> 1`.
- For continuous recoding, use ranges. Example age groups: `0-14 -> 1`, `15-64 -> 2`, `65+ -> 3`.
- After recoding, run frequency on the new variable and check value labels.

## Chi-Square

- Use chi-square when both variables are categorical/nominal. The textbook distinguishes goodness-of-fit for one categorical variable and independence chi-square for two categorical variables; the exam focus is usually independence chi-square.
- A contingency/crosstab table shows frequency and percentage combinations of two categorical variables.
- Usually put the independent variable in rows and the dependent variable in columns. Interpret percentages along the independent variable direction.
- SPSS route: `分析 -> 描述统计 -> 交叉表`.
- In `统计`, choose `卡方`; choose `Phi 和 Cramer V` for association strength.
- In `单元格`, select observed count, expected count, row percentage, column percentage, and total percentage as required.
- Output reading order:
  1. Case Processing Summary: valid and missing cases.
  2. Crosstabulation: counts, expected counts, and percentages.
  3. Chi-Square Tests: Pearson Chi-Square, df, and Sig.
  4. Symmetric Measures: Phi for `2 x 2`; Cramer's V when any variable has more than two categories.
- Assumption check: ideally sample size `>= 40`; expected counts should generally be at least 5 in at least 80% of cells. If more than 20% expected counts are below 5, consider merging categories, increasing sample size, Yates correction for eligible `2 x 2`, or Fisher exact test when appropriate.
- Interpretation: `p < 0.05` rejects the null that variables are independent. Then use Phi/Cramer's V for strength. Significance is not strength.
- Strength guide used by the textbook: absolute association coefficient `< .30` weak, `.30-.70` moderate, `> .70` strong.
- Exam wording: "变量 A 与变量 B 存在/不存在统计显著关联；Phi/Cramer's V=...，关联强度为..."

## ANOVA

- Use one-way ANOVA when the independent variable is categorical and the dependent variable is continuous.
- ANOVA compares between-group variation with within-group/error variation. `F = MSB / MSW`.
- The null hypothesis is that group means are not significantly different.
- SPSS route: `分析 -> 比较平均值 -> 单因素 ANOVA 检验`.
- Put the continuous dependent variable into `因变量列表`; put the categorical independent variable into `因子`.
- In `选项`, select `描述`, `方差齐性检验`, Brown-Forsythe, Welch, and mean plot when needed.
- If more than two groups, use `事后检验`. If variance homogeneity holds, textbook examples include LSD and Scheffe; if group sizes differ, Scheffe is safer. If variance homogeneity is violated, use Dunnett T3, Games-Howell, Tamhane T2, or Dunnett C where available.
- Output reading order:
  1. Descriptives: N, mean, SD, SE, min, max for each group.
  2. Test of Homogeneity of Variances: Levene Sig.
  3. ANOVA table: sum of squares, df, mean square, F, Sig.
  4. Robust tests such as Welch/Brown-Forsythe if homogeneity is violated.
  5. Multiple Comparisons: which group pairs differ.
- Interpretation: if ANOVA `p < .05`, at least one group mean differs; use post-hoc tests to say which groups differ.
- Effect size: eta squared can express how much of total variation is explained by the independent variable. Textbook guide: `.01-.059` weak, `.059-.138` moderate, `>= .138` strong.

## Correlation And Partial Correlation

- Use correlation to test whether two variables are associated and to estimate direction and strength. Correlation does not prove causality.
- Before Pearson correlation, check approximate normality and linearity.
- Normality route: `分析 -> 描述统计 -> 探索`; put variables into dependent list; choose plots and tick normality plots with tests.
- Normality judgment: if K-S and Shapiro-Wilk Sig. are both `> .05`, treat as approximately normal. If they conflict, use K-S more for large samples and Shapiro-Wilk more for small samples; also inspect histogram, P-P plot, and Q-Q plot.
- Linearity route: `图形 -> 旧对话框 -> 散点图/点图 -> 简单散点图`; put the two variables into X and Y axes.
- Bivariate route: `分析 -> 相关 -> 双变量`; put variables into `变量`; choose Pearson or Spearman.
- Pearson: use for continuous variables that are approximately normal and linearly related.
- Spearman: use for ordinal variables, rank variables, non-normal data, unknown distribution, or monotonic but not clearly linear relations.
- Point-biserial correlation: use for one binary categorical variable and one continuous variable; it is equivalent to Pearson after coding the binary variable as `0/1`, but interpret direction relative to the reference coding.
- Partial correlation, also called net correlation in the textbook, controls one or more variables and then examines the relationship between two target variables.
- Partial route: `分析 -> 相关 -> 偏相关`; put the two target variables into `变量`; put controls into `控制变量`.
- Output: read correlation coefficient `r` or `ρ`, Sig. (2-tailed), and N.
- Result rule: if `p >= .05`, do not interpret the coefficient as reliable even if its absolute value looks large.
- Textbook strength guide for Pearson: `|r| < .30` weak, `.30-.50` low, `.50-.80` significant/strong, `.80-1` high.

## Multiple Linear Regression

- Because Chapter 10 OCR is incomplete/noisy, use `spss-operation-map.md` for the operation core.
- Keep textbook-aligned theory: linear regression remains association/conditional expectation unless a causal design justifies causal language.
- Use multiple linear regression when the dependent variable is continuous and several predictors explain or predict it.
- Main output reading order: Model Summary (`R Square`, `Adjusted R Square`), ANOVA (`F`, `Sig.`), Coefficients (`B`, `Beta`, `t`, `Sig.`, `Tolerance`, `VIF`).
- Enter/simultaneous regression: all predictors entered at once; use when theory specifies the variables.
- Stepwise regression: exploratory variable selection; use only when the task asks for strongest predictors or stepwise method.
- Hierarchical/block regression: enter predictors by blocks with `Next`; use when comparing controls first, then core explanatory variables.
- Multi-category categorical predictors need dummy variables: use `n-1` dummies and leave one category as reference.

## Chapter 10: Linear Regression (dedicated export, summarized)

Source: `<path-to-your-chapter10-ocr-markdown>`. Summary only — do not quote long passages from this source; this section paraphrases the textbook's own structure and worked examples.

- Opening case: a study on shared international-organization membership uses simultaneous (Enter) multiple regression with predictors including militarized disputes, democracy level, trade interdependence, alliance ties, geographic distance, and per-capita GDP; large N, adjusted R² around .63, all predictors significant at .05. The textbook uses this to show regression goes beyond simple correlation by estimating each predictor's net/partial contribution while holding the others constant.
- Simple (one-IV) regression: equation form is DV = intercept + slope×IV + error. Slope sign tells direction of effect; intercept is the predicted DV when IV = 0. The term "regression" originates from Galton's regression-to-the-mean observation in height inheritance.
- Multiple regression: extends correlation/partial correlation logic — partial correlation controls a third variable for one pair, but only handles a few variables and gives no overall model fit; multiple regression handles many predictors simultaneously and yields both individual (partial) coefficients and overall fit statistics. Categorical predictors are allowed but the book recommends keeping the number of categorical predictor variables modest (roughly three or fewer) so the resulting dummy-variable equation stays manageable.
- OLS (ordinary least squares): finds the line minimizing the sum of squared residuals (observed minus predicted DV). Slope and intercept formulas are the standard covariance/variance-ratio forms.
- R² (coefficient of determination): share of DV variance explained by the model, 0 to 1, higher is better fit; in simple regression R² equals the squared bivariate correlation r². Adjusted R² penalizes adding predictors that don't genuinely improve fit (penalty shrinks as sample size grows relative to predictor count) — textbook recommends reporting adjusted R² by default, especially once more than one predictor is in the model.
- Overall F test: null hypothesis is that all slope coefficients are zero in the population; a significant F means the model as a whole has explanatory power.
- LINE assumptions for regression: Linearity (each predictor relates to the DV roughly linearly — check via scatterplots or residual plots; a funnel or curved residual pattern signals a problem; this requirement is relaxed for categorical/dummy predictors), Normality (residuals approximately normal — check via residual histogram and P-P plot), Independence (residuals uncorrelated across cases — check via Durbin-Watson, ideal value near 2; well below 2 suggests positive autocorrelation, well above 2 suggests negative autocorrelation), Equal variance/homoscedasticity (residual spread constant across predicted values — check via standardized-residual vs standardized-predicted-value scatterplot; a funnel shape signals heteroscedasticity, which the book suggests addressing with weighted least squares). Predictors themselves are treated as fixed/known values, not random variables to be modeled.
- Multicollinearity (multiple regression only): when predictors are highly correlated with each other, coefficient estimates become unstable and can even flip sign depending on the sample (textbook's refrigerator price/capacity-on-power-usage example). Diagnosed via tolerance, VIF, eigenvalues, and condition index in SPSS's Collinearity Diagnostics. Rule of thumb in this textbook: tolerance near 0 or VIF beyond roughly 10 signals strong collinearity; condition index above ~15 is a possible concern, above ~30 indicates clear collinearity, above ~100 indicates severe collinearity; a variance-proportion above .5 shared across two or more predictors on the same component also flags likely collinearity. Remedies: drop or merge a collinear predictor, or switch to ridge regression, principal-component regression, or partial least squares.
- Three model-building strategies (and SPSS's five entry methods — Enter, Remove, Forward, Backward, Stepwise):
  - Simultaneous/Enter regression: all theoretically-justified predictors enter at once and stay regardless of individual significance; used for explanatory (theory-testing) models where every predictor matters substantively even if not all are significant.
  - Stepwise regression (Forward adds one significant predictor at a time until no addition helps; Backward starts full and removes the weakest predictors until removal would hurt the model; Stepwise combines both, re-checking earlier predictors after each addition): exploratory, prediction-oriented, useful with many candidate predictors when the goal is the most parsimonious well-fitting model.
  - Hierarchical/block regression: predictors entered in theory-driven blocks (e.g., basic factors first, then intervening factors, then distal/structural factors); the key statistic is the R² change (ΔR²) at each block, and a predictor that becomes non-significant after a later block enters can indicate the earlier relationship was actually spurious/mediated. The book illustrates this with a hierarchical model of public perception of China's influence, where income's effect weakens once internet-use is added — suggesting income's apparent effect was partly carried by internet use.
- Worked one-IV example: regressing one country's favorability rating on another's, reading order is: variable-entry table, Model Summary (R², adjusted R², Durbin-Watson), ANOVA (F, Sig.), Coefficients (B, Beta, t, Sig.), Residuals Statistics, then residual histogram/P-P plot for normality and standardized-residual scatterplot for homoscedasticity. The book stresses that a coefficient's size is meaningless if it is not statistically significant.
- Worked multi-IV example: a 1955-era "third-country alignment with the US in the UN" model with predictors GNP, power rank, regime stability, and a dummy-coded "freedom of opposition groups" variable (two dummies, one reference category). Demonstrates: scatterplot matrix first to eyeball linearity across all pairs; collinearity diagnostics required for multiple (not simple) regression; reading order recommended for multiple regression specifically is residual histogram/P-P plot and residual scatterplot first (normality/homoscedasticity), then collinearity diagnostics (tolerance/VIF plus eigenvalue/condition index/variance proportions as a cross-check — different diagnostics can disagree without necessarily invalidating the model, especially in non-predictive/explanatory research), then Model Summary + ANOVA for overall fit and significance, then the Coefficients table to write the equation and compare standardized Beta magnitudes for relative predictor importance, and finally case diagnostics (Casewise Diagnostics) to flag potential outliers by standardized residual (default threshold ±3 SD) — the book cautions against reflexively deleting flagged cases, especially in small samples, since that can distort the standard deviation and bias results.
- Standardized coefficient (Beta) formula: Beta = unstandardized B × (SD of that predictor / SD of the DV); removes units so Beta magnitudes can be compared across predictors with different scales (the predictor with the largest |Beta| among significant predictors has the strongest relative effect).
- Chapter also models prompting DeepSeek/ChatGPT to generate SPSS syntax for simple and multiple regression (including scatterplots, collinearity diagnostics, case diagnostics, residual histogram/P-P plot), and how to paste back an SPSS error message to get a corrected syntax suggestion.
- End-of-chapter exercises (four problems, with accompanying `.sav` files referenced in the book): (1) Brazil 2005-2018 consumer inflation expectations regressed on macroeconomic predictors — write the equation, report R²/adjusted R², produce residual histogram/P-P plot/scatterplot, and identify the strongest predictor. (2) European interest-group representation cost vs. five binary social-media-engagement variables — convert the five binaries to dummies, log-transform the cost variable (`mean_cost` → `lnmean_cost`), and write the equation. (3) A 10-region cross-section relating population density, per-capita GDP, and Gini coefficient to violent crime rate — report R²/adjusted R², ANOVA significance, and which predictors matter and in which direction. (4) Four separate simple-regression results showing how different categories of sanction-threat issuer (government, trade/foreign-service bodies, legislature, international organizations) each predict an export-related outcome — write out the four simple regression equations from the reported coefficients/intercepts.
