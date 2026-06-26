#!/usr/bin/env python3
"""Compute SPSS-exam statistics from CSV/XLSX/SAV data.

Outputs JSON so the agent can turn exact results into Chinese exam wording.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


def load_data(path: str, sheet: str | None = None) -> tuple[pd.DataFrame, dict]:
    file_path = Path(path)
    suffix = file_path.suffix.lower()
    meta: dict = {"file": str(file_path), "format": suffix.lstrip(".")}
    if suffix == ".csv":
        df = pd.read_csv(file_path)
    elif suffix in {".xlsx", ".xls"}:
        df = pd.read_excel(file_path, sheet_name=sheet or 0)
        meta["sheet"] = sheet or 0
    elif suffix == ".sav":
        try:
            import pyreadstat
        except ImportError as exc:
            raise SystemExit("pyreadstat is required for .sav files") from exc
        df, sav_meta = pyreadstat.read_sav(file_path, apply_value_formats=False, user_missing=True)
        meta["variable_labels"] = getattr(sav_meta, "column_labels", None)
        meta["value_labels"] = getattr(sav_meta, "variable_value_labels", None)
        meta["missing_ranges"] = getattr(sav_meta, "missing_ranges", None)
        meta["missing_user_values"] = getattr(sav_meta, "missing_user_values", None)
    else:
        raise SystemExit(f"Unsupported file type: {suffix}")
    return df, meta


def clean(df: pd.DataFrame, variables: list[str]) -> pd.DataFrame:
    missing = [v for v in variables if v not in df.columns]
    if missing:
        raise SystemExit(f"Missing variables: {', '.join(missing)}")
    return df[variables].dropna()


def as_numeric(series: pd.Series, name: str) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    if values.notna().sum() == 0:
        raise SystemExit(f"Variable is not numeric: {name}")
    return values


def round_float(value):
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except TypeError:
        pass
    if isinstance(value, (np.integer, int)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        number = float(value)
        if number != 0 and abs(number) < 0.000001:
            return number
        return round(number, 6)
    return value


def jsonify(obj):
    if isinstance(obj, dict):
        return {str(k): jsonify(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [jsonify(v) for v in obj]
    return round_float(obj)


def audit(df: pd.DataFrame, meta: dict) -> dict:
    columns = []
    for col in df.columns:
        s = df[col]
        numeric = pd.to_numeric(s, errors="coerce")
        columns.append(
            {
                "name": col,
                "dtype": str(s.dtype),
                "n": int(s.shape[0]),
                "missing": int(s.isna().sum()),
                "unique": int(s.nunique(dropna=True)),
                "numeric_nonmissing": int(numeric.notna().sum()),
                "min": numeric.min() if numeric.notna().any() else None,
                "max": numeric.max() if numeric.notna().any() else None,
                "sample_values": [round_float(v) for v in s.dropna().unique()[:8].tolist()],
            }
        )
    return {"analysis": "audit", "meta": meta, "rows": int(len(df)), "columns": columns}


def mode_values(series: pd.Series) -> list:
    modes = series.mode(dropna=True)
    return modes.tolist()


def frequency_rows(series: pd.Series) -> list[dict]:
    total = int(len(series))
    valid = series.dropna()
    valid_n = int(len(valid))
    rows = []
    counts = series.value_counts(dropna=False).sort_index()
    for value, count in counts.items():
        is_missing = bool(pd.isna(value))
        rows.append(
            {
                "value": None if is_missing else value,
                "count": int(count),
                "percent": count / total if total else None,
                "valid_percent": None if is_missing or not valid_n else count / valid_n,
            }
        )
    return rows


def descriptive(df: pd.DataFrame, variables: list[str]) -> dict:
    out = {"analysis": "descriptive", "variables": {}}
    for var in variables:
        s = df[var]
        numeric = pd.to_numeric(s, errors="coerce")
        item = {
            "n": int(s.notna().sum()),
            "missing": int(s.isna().sum()),
            "unique": int(s.nunique(dropna=True)),
            "mode": mode_values(s.dropna()),
            "frequencies": frequency_rows(s),
        }
        if numeric.notna().sum() > 0:
            item.update(
                {
                    "mean": numeric.mean(),
                    "std": numeric.std(ddof=1),
                    "median": numeric.median(),
                    "min": numeric.min(),
                    "max": numeric.max(),
                }
            )
        out["variables"][var] = item
    return out


def impute_series(series: pd.Series, method: str) -> tuple[pd.Series, float | None]:
    if method == "none":
        return series, None
    valid = series.dropna()
    if valid.empty:
        return series, None
    if method == "median":
        fill_value = float(valid.median())
    elif method == "mean":
        fill_value = float(valid.mean())
    elif method == "mode":
        fill_value = valid.mode(dropna=True).iloc[0]
    else:
        raise SystemExit(f"Unsupported imputation method: {method}")
    return series.fillna(fill_value), fill_value


def recoded_descriptive(df: pd.DataFrame, variables: list[str], missing_values: list[float], direction: str, impute: str) -> dict:
    out = {
        "analysis": "recoded-descriptive",
        "direction": direction,
        "imputation": impute,
        "missing_values": missing_values,
        "rule": "low end = smaller/weaker/negative/pejorative; high end = larger/stronger/positive/commendatory",
        "variables": {},
    }
    for var in variables:
        raw = pd.to_numeric(df[var], errors="coerce")
        cleaned = raw.mask(raw.isin(missing_values))
        valid = cleaned.dropna()
        mapping = None
        recoded = cleaned.copy()
        if valid.empty:
            raise SystemExit(f"No valid numeric data after missing handling: {var}")
        if direction == "high-to-low":
            valid_values = sorted(valid.unique().tolist())
            reversed_values = list(reversed(valid_values))
            mapping = {old: new for old, new in zip(valid_values, reversed_values)}
            recoded = cleaned.map(mapping)
        elif direction == "low-to-high":
            mapping = {value: value for value in sorted(valid.unique().tolist())}
        else:
            raise SystemExit(f"Unsupported direction: {direction}")
        imputed, fill_value = impute_series(recoded, impute)
        variable_result = {
            "raw_valid_n": int(valid.shape[0]),
            "raw_missing_or_excluded": int(cleaned.isna().sum()),
            "recode_mapping": mapping,
            "excluded_missing": descriptive(pd.DataFrame({f"r_{var}": recoded}), [f"r_{var}"])["variables"][f"r_{var}"],
        }
        if impute != "none":
            variable_result["imputed"] = {
                "method": impute,
                "fill_value": fill_value,
                "n": int(imputed.notna().sum()),
                "statistics": descriptive(pd.DataFrame({f"r_{var}_imp": imputed}), [f"r_{var}_imp"])["variables"][f"r_{var}_imp"],
            }
        out["variables"][var] = variable_result
    return out


def chi_square(df: pd.DataFrame, iv: str, dv: str) -> dict:
    data = clean(df, [iv, dv])
    table = pd.crosstab(data[iv], data[dv])
    chi2, p, dof, expected = stats.chi2_contingency(table)
    n = int(table.to_numpy().sum())
    r, c = table.shape
    phi_cramer = math.sqrt(chi2 / (n * max(1, min(r - 1, c - 1)))) if n else None
    low_expected = int((expected < 5).sum())
    total_cells = int(expected.size)
    return {
        "analysis": "chi-square",
        "iv": iv,
        "dv": dv,
        "n": n,
        "observed": table.to_dict(),
        "chi_square": chi2,
        "df": int(dof),
        "p": p,
        "cramers_v_or_phi": phi_cramer,
        "expected_min": expected.min(),
        "expected_cells_lt5": low_expected,
        "expected_cells_total": total_cells,
        "expected_lt5_percent": low_expected / total_cells if total_cells else None,
    }


def anova(df: pd.DataFrame, iv: str, dv: str) -> dict:
    data = clean(df, [iv, dv]).copy()
    data[dv] = as_numeric(data[dv], dv)
    groups = []
    descriptives = {}
    for name, group in data.groupby(iv, dropna=True):
        vals = group[dv].dropna()
        if len(vals) > 0:
            groups.append(vals)
            descriptives[str(name)] = {
                "n": int(len(vals)),
                "mean": vals.mean(),
                "std": vals.std(ddof=1),
                "min": vals.min(),
                "max": vals.max(),
            }
    if len(groups) < 2:
        raise SystemExit("ANOVA requires at least two non-empty groups")
    f_stat, p = stats.f_oneway(*groups)
    lev_stat, lev_p = stats.levene(*groups, center="median")
    grand = data[dv].mean()
    ss_between = sum(len(g) * (g.mean() - grand) ** 2 for g in groups)
    ss_total = sum((data[dv] - grand) ** 2)
    eta_sq = ss_between / ss_total if ss_total else None
    return {
        "analysis": "anova",
        "iv": iv,
        "dv": dv,
        "n": int(data[dv].notna().sum()),
        "groups": descriptives,
        "f": f_stat,
        "df_between": len(groups) - 1,
        "df_within": int(sum(len(g) for g in groups) - len(groups)),
        "p": p,
        "levene_stat": lev_stat,
        "levene_p": lev_p,
        "eta_squared": eta_sq,
    }


def correlation(df: pd.DataFrame, x: str, y: str, method: str) -> dict:
    data = clean(df, [x, y]).copy()
    xs = as_numeric(data[x], x)
    ys = as_numeric(data[y], y)
    if method == "spearman":
        coef, p = stats.spearmanr(xs, ys)
        label = "spearman"
    else:
        coef, p = stats.pearsonr(xs, ys)
        label = "pearson"
    return {"analysis": "correlation", "method": label, "x": x, "y": y, "n": int(len(data)), "r": coef, "p": p}


def partial_correlation(df: pd.DataFrame, x: str, y: str, controls: list[str]) -> dict:
    import statsmodels.api as sm

    variables = [x, y] + controls
    data = clean(df, variables).copy()
    for var in variables:
        data[var] = as_numeric(data[var], var)
    design = sm.add_constant(data[controls], has_constant="add")
    rx = sm.OLS(data[x], design).fit().resid
    ry = sm.OLS(data[y], design).fit().resid
    coef, p = stats.pearsonr(rx, ry)
    return {"analysis": "partial-correlation", "x": x, "y": y, "controls": controls, "n": int(len(data)), "partial_r": coef, "p": p}


def regression(df: pd.DataFrame, dv: str, predictors: list[str]) -> dict:
    import statsmodels.api as sm
    from statsmodels.stats.outliers_influence import variance_inflation_factor

    variables = [dv] + predictors
    data = clean(df, variables).copy()
    data[dv] = as_numeric(data[dv], dv)
    x = pd.get_dummies(data[predictors], drop_first=True, dtype=float)
    x = sm.add_constant(x, has_constant="add")
    model = sm.OLS(data[dv], x).fit()
    y_std = data[dv].std(ddof=1)
    coefficients = []
    for name in model.params.index:
        beta = None
        if name != "const" and y_std:
            beta = model.params[name] * x[name].std(ddof=1) / y_std
        coefficients.append(
            {
                "term": str(name),
                "b": model.params[name],
                "beta": beta,
                "se": model.bse[name],
                "t": model.tvalues[name],
                "p": model.pvalues[name],
            }
        )
    vif = []
    for idx, name in enumerate(x.columns):
        if name == "const":
            continue
        vif.append({"term": str(name), "vif": variance_inflation_factor(x.to_numpy(), idx)})
    return {
        "analysis": "linear-regression",
        "dv": dv,
        "predictors": predictors,
        "n": int(model.nobs),
        "r_squared": model.rsquared,
        "adjusted_r_squared": model.rsquared_adj,
        "f": model.fvalue,
        "model_p": model.f_pvalue,
        "coefficients": coefficients,
        "vif": vif,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", required=True)
    parser.add_argument("--sheet")
    parser.add_argument("--analysis", required=True, choices=["audit", "desc", "recode-desc", "chi2", "anova", "corr", "partial-corr", "regression"])
    parser.add_argument("--vars", nargs="*", default=[])
    parser.add_argument("--iv")
    parser.add_argument("--dv")
    parser.add_argument("--x")
    parser.add_argument("--y")
    parser.add_argument("--controls", nargs="*", default=[])
    parser.add_argument("--predictors", nargs="*", default=[])
    parser.add_argument("--corr-method", choices=["pearson", "spearman"], default="pearson")
    parser.add_argument("--missing-values", nargs="*", type=float, default=[])
    parser.add_argument("--direction", choices=["low-to-high", "high-to-low"], default="low-to-high")
    parser.add_argument("--impute", choices=["none", "median", "mean", "mode"], default="none")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    df, meta = load_data(args.file, args.sheet)
    if args.analysis == "audit":
        result = audit(df, meta)
    elif args.analysis == "desc":
        variables = args.vars or list(df.columns)
        result = descriptive(df, variables)
    elif args.analysis == "recode-desc":
        variables = args.vars or list(df.columns)
        result = recoded_descriptive(df, variables, args.missing_values, args.direction, args.impute)
    elif args.analysis == "chi2":
        result = chi_square(df, args.iv, args.dv)
    elif args.analysis == "anova":
        result = anova(df, args.iv, args.dv)
    elif args.analysis == "corr":
        result = correlation(df, args.x, args.y, args.corr_method)
    elif args.analysis == "partial-corr":
        result = partial_correlation(df, args.x, args.y, args.controls)
    elif args.analysis == "regression":
        result = regression(df, args.dv, args.predictors)
    else:
        raise SystemExit(f"Unsupported analysis: {args.analysis}")
    print(json.dumps(jsonify(result), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
