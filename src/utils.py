"""
Utility functions for the E-commerce A/B Test Techbook project.

This module centralizes project path handling, CSV loading, table formatting,
and lightweight display helpers used by notebooks and Streamlit.

Project structure expected:

ECOMMERCE_AB_TEST_PROJECT/
├── app/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── outputs/
│   ├── charts/
│   └── tables/
└── src/
    └── utils.py
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Sequence

import numpy as np
import pandas as pd


# ============================================================
# 1. Path Helpers
# ============================================================

def get_project_root() -> Path:
    """
    Return the project root path.

    This function works whether it is called from:
    - project root
    - notebooks/
    - app/
    - src/
    """
    current_dir = Path.cwd().resolve()

    if current_dir.name in {"notebooks", "app", "src"}:
        return current_dir.parent

    return current_dir


def get_data_dir(project_root: Optional[Path] = None) -> Path:
    project_root = project_root or get_project_root()
    return project_root / "data"


def get_processed_dir(project_root: Optional[Path] = None) -> Path:
    return get_data_dir(project_root) / "processed"


def get_output_dir(project_root: Optional[Path] = None) -> Path:
    project_root = project_root or get_project_root()
    return project_root / "outputs"


def get_table_dir(project_root: Optional[Path] = None) -> Path:
    return get_output_dir(project_root) / "tables"


def get_chart_dir(project_root: Optional[Path] = None) -> Path:
    return get_output_dir(project_root) / "charts"


def ensure_project_dirs(project_root: Optional[Path] = None) -> dict[str, Path]:
    """
    Create and return frequently used project directories.
    """
    project_root = project_root or get_project_root()

    paths = {
        "project_root": project_root,
        "data": project_root / "data",
        "raw": project_root / "data" / "raw",
        "processed": project_root / "data" / "processed",
        "outputs": project_root / "outputs",
        "tables": project_root / "outputs" / "tables",
        "charts": project_root / "outputs" / "charts",
    }

    for path in paths.values():
        if path.name != project_root.name:
            path.mkdir(parents=True, exist_ok=True)

    return paths


# ============================================================
# 2. File and Data Loading Helpers
# ============================================================

def file_exists(path: Path | str) -> bool:
    return Path(path).exists()


def format_bytes(size_bytes: int | float) -> str:
    """
    Convert bytes to a human-readable string.
    """
    if pd.isna(size_bytes):
        return ""

    size_bytes = int(size_bytes)

    if size_bytes == 0:
        return "0 B"

    units = ["B", "KB", "MB", "GB", "TB"]
    idx = int(np.floor(np.log(size_bytes) / np.log(1024)))
    idx = min(idx, len(units) - 1)
    value = size_bytes / (1024 ** idx)

    return f"{value:,.2f} {units[idx]}"


def read_csv_safely(
    path: Path | str,
    *,
    required: bool = True,
    encoding: str = "utf-8-sig",
    **kwargs,
) -> pd.DataFrame:
    """
    Read a CSV file with a clean error message.

    Parameters
    ----------
    path:
        CSV path.
    required:
        If True, raise FileNotFoundError when missing.
        If False, return empty DataFrame when missing.
    encoding:
        Default encoding for Korean/Excel-compatible CSV files.
    kwargs:
        Additional keyword arguments passed to pd.read_csv.
    """
    path = Path(path)

    if not path.exists():
        if required:
            raise FileNotFoundError(f"CSV file not found: {path}")
        return pd.DataFrame()

    return pd.read_csv(path, encoding=encoding, **kwargs)


def read_project_table(
    filename: str,
    *,
    project_root: Optional[Path] = None,
    required: bool = True,
    **kwargs,
) -> pd.DataFrame:
    """
    Read a table from outputs/tables.
    """
    table_path = get_table_dir(project_root) / filename
    return read_csv_safely(table_path, required=required, **kwargs)


def read_processed_csv(
    filename: str,
    *,
    project_root: Optional[Path] = None,
    required: bool = True,
    **kwargs,
) -> pd.DataFrame:
    """
    Read a CSV file from data/processed.
    """
    processed_path = get_processed_dir(project_root) / filename
    return read_csv_safely(processed_path, required=required, **kwargs)


def read_chart_path(
    filename: str,
    *,
    project_root: Optional[Path] = None,
    required: bool = False,
) -> Optional[Path]:
    """
    Return a chart image path from outputs/charts.
    """
    chart_path = get_chart_dir(project_root) / filename

    if not chart_path.exists():
        if required:
            raise FileNotFoundError(f"Chart file not found: {chart_path}")
        return None

    return chart_path


def load_events_clean(
    *,
    project_root: Optional[Path] = None,
    usecols: Optional[Sequence[str]] = None,
    nrows: Optional[int] = None,
) -> pd.DataFrame:
    """
    Load processed event log.

    This file can be large. Use `usecols` and `nrows` when possible.
    """
    dtype_map = {
        "timestamp": "int64",
        "visitorid": "int64",
        "event": "category",
        "itemid": "int64",
        "transactionid": "float64",
    }

    kwargs = {}
    if usecols is not None:
        kwargs["usecols"] = list(usecols)
    if nrows is not None:
        kwargs["nrows"] = nrows

    df = read_processed_csv(
        "events_clean.csv",
        project_root=project_root,
        dtype={k: v for k, v in dtype_map.items() if usecols is None or k in usecols},
        **kwargs,
    )

    if "event_time" in df.columns:
        df["event_time"] = pd.to_datetime(df["event_time"], errors="coerce")

    if "event_date" in df.columns:
        df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce").dt.date

    return df


def load_item_latest_category(
    *,
    project_root: Optional[Path] = None,
) -> pd.DataFrame:
    """
    Load item-category mapping table from processed CSV.
    """
    df = read_processed_csv("item_latest_category.csv", project_root=project_root)

    if "property_time" in df.columns:
        df["property_time"] = pd.to_datetime(df["property_time"], errors="coerce")

    return df


# ============================================================
# 3. Save Helpers
# ============================================================

def save_table(
    df: pd.DataFrame,
    filename: str,
    *,
    project_root: Optional[Path] = None,
    index: bool = False,
) -> Path:
    """
    Save a DataFrame to outputs/tables.
    """
    table_dir = get_table_dir(project_root)
    table_dir.mkdir(parents=True, exist_ok=True)

    save_path = table_dir / filename
    df.to_csv(save_path, index=index, encoding="utf-8-sig")

    return save_path


def save_processed_csv(
    df: pd.DataFrame,
    filename: str,
    *,
    project_root: Optional[Path] = None,
    index: bool = False,
) -> Path:
    """
    Save a DataFrame to data/processed.
    """
    processed_dir = get_processed_dir(project_root)
    processed_dir.mkdir(parents=True, exist_ok=True)

    save_path = processed_dir / filename
    df.to_csv(save_path, index=index, encoding="utf-8-sig")

    return save_path


# ============================================================
# 4. Metric Helpers
# ============================================================

def safe_divide(numerator, denominator):
    """
    Safe division for scalar or array-like values.
    """
    return np.where(np.asarray(denominator) > 0, np.asarray(numerator) / np.asarray(denominator), np.nan)


def conversion_rate(success: int | float, total: int | float) -> float:
    """
    Return success / total. If total is 0, return NaN.
    """
    if total == 0 or pd.isna(total):
        return np.nan
    return success / total


def relative_lift(control_rate: float, treatment_rate: float) -> float:
    """
    Return relative lift: (treatment - control) / control.
    """
    if control_rate == 0 or pd.isna(control_rate):
        return np.nan
    return (treatment_rate - control_rate) / control_rate


def absolute_lift(control_rate: float, treatment_rate: float) -> float:
    """
    Return absolute lift: treatment - control.
    """
    return treatment_rate - control_rate


# ============================================================
# 5. Formatting Helpers
# ============================================================

def format_number(value, digits: int = 0) -> str:
    if pd.isna(value):
        return ""
    return f"{value:,.{digits}f}"


def format_percent(value, digits: int = 2, *, already_percent: bool = False) -> str:
    """
    Format a ratio or percent value.

    Examples
    --------
    format_percent(0.0269) -> '2.69%'
    format_percent(2.69, already_percent=True) -> '2.69%'
    """
    if pd.isna(value):
        return ""

    value = value if already_percent else value * 100
    return f"{value:,.{digits}f}%"


def format_pct_point(value, digits: int = 2) -> str:
    """
    Format a percentage-point value.
    """
    if pd.isna(value):
        return ""
    return f"{value:,.{digits}f}%p"


def format_table_for_display(
    df: pd.DataFrame,
    *,
    percent_cols: Optional[Sequence[str]] = None,
    number_cols: Optional[Sequence[str]] = None,
    already_percent_cols: Optional[Sequence[str]] = None,
    digits: int = 2,
) -> pd.DataFrame:
    """
    Return a copy of DataFrame with selected columns formatted as strings.

    Useful for Streamlit display tables.
    """
    formatted = df.copy()

    percent_cols = percent_cols or []
    number_cols = number_cols or []
    already_percent_cols = already_percent_cols or []

    for col in percent_cols:
        if col in formatted.columns:
            formatted[col] = formatted[col].apply(lambda x: format_percent(x, digits=digits))

    for col in already_percent_cols:
        if col in formatted.columns:
            formatted[col] = formatted[col].apply(lambda x: format_percent(x, digits=digits, already_percent=True))

    for col in number_cols:
        if col in formatted.columns:
            formatted[col] = formatted[col].apply(lambda x: format_number(x, digits=0))

    return formatted


# ============================================================
# 6. Streamlit-Oriented Loaders
# ============================================================

def load_dashboard_tables(project_root: Optional[Path] = None) -> dict[str, pd.DataFrame]:
    """
    Load lightweight summary tables used by Streamlit.

    Heavy files such as events_clean.csv and 02_user_event_counts.csv
    are intentionally excluded from the default loader.
    """
    table_files = {
        # Raw audit
        "raw_audit_summary": "01_raw_audit_summary.csv",

        # Funnel
        "funnel_summary": "02_user_level_funnel.csv",
        "conversion_summary": "02_user_level_conversion_summary.csv",
        "daily_funnel": "02_daily_funnel_trend.csv",
        "monthly_funnel": "02_monthly_funnel_trend.csv",
        "baseline_metric": "02_ab_test_baseline_metric_table.csv",

        # Item/category
        "category_performance": "03_category_performance_full.csv",
        "category_opportunity": "03_category_opportunity_summary.csv",
        "top_categories_by_views": "03_top_categories_by_views.csv",
        "top_categories_by_purchase": "03_top_categories_by_purchase.csv",
        "optimization_categories": "03_abtest_optimization_candidate_categories.csv",
        "expansion_categories": "03_abtest_expansion_candidate_categories.csv",
        "business_insight": "03_business_insight_summary.csv",

        # A/B test
        "abtest_baseline": "04_baseline_conversion_summary.csv",
        "sample_size": "04_sample_size_scenarios_view_to_cart.csv",
        "business_impact": "04_business_impact_scenarios.csv",
        "final_abtest_insight": "04_final_abtest_insight_summary.csv",

        # Business recommendation
        "executive_summary": "05_executive_summary.csv",
        "problem_diagnosis": "05_problem_diagnosis.csv",
        "opportunity_prioritization": "05_opportunity_prioritization_framework.csv",
        "abtest_roadmap": "05_abtest_roadmap.csv",
        "impact_100k": "05_business_impact_summary_per_100k.csv",
        "final_recommendation": "05_final_recommendation.csv",
        "decision_rule": "05_experiment_decision_rule.csv",
        "streamlit_storyline": "05_streamlit_storyline.csv",
        "readme_wikidocs_summary": "05_readme_wikidocs_summary.csv",
    }

    loaded: dict[str, pd.DataFrame] = {}

    for key, filename in table_files.items():
        loaded[key] = read_project_table(
            filename,
            project_root=project_root,
            required=False,
        )

    return loaded


def get_available_charts(project_root: Optional[Path] = None) -> dict[str, Path]:
    """
    Return available chart paths generated by notebooks.
    """
    chart_dir = get_chart_dir(project_root)

    if not chart_dir.exists():
        return {}

    return {path.stem: path for path in sorted(chart_dir.glob("*.png"))}


# ============================================================
# 7. Validation Helpers
# ============================================================

def required_columns_check(df: pd.DataFrame, required_columns: Sequence[str], name: str = "DataFrame") -> None:
    """
    Raise ValueError if required columns are missing.
    """
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"{name} is missing required columns: {missing}")


def summarize_dataframe(df: pd.DataFrame, name: str = "data") -> pd.DataFrame:
    """
    Return a simple column-level summary.
    """
    return pd.DataFrame({
        "data": name,
        "column": df.columns,
        "dtype": [str(dtype) for dtype in df.dtypes],
        "non_null_count": df.notna().sum().values,
        "null_count": df.isna().sum().values,
        "null_rate": df.isna().mean().values,
        "unique_count": [df[col].nunique(dropna=True) for col in df.columns],
    })
