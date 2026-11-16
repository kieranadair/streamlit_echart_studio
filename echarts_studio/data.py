from __future__ import annotations
import io
from dataclasses import dataclass
import pandas as pd

@dataclass(frozen=True)
class ColumnProfile:
    name: str; kind: str; dtype: str; nulls: int; unique: int

def kind(s: pd.Series) -> str:
    if pd.api.types.is_datetime64_any_dtype(s): return "datetime"
    if pd.api.types.is_bool_dtype(s): return "boolean"
    if pd.api.types.is_numeric_dtype(s): return "numeric"
    return "categorical"

def profile(df: pd.DataFrame):
    return [ColumnProfile(str(c), kind(df[c]), str(df[c].dtype), int(df[c].isna().sum()), int(df[c].nunique(dropna=True))) for c in df.columns]

def coerce_dates(df: pd.DataFrame) -> pd.DataFrame:
    out=df.copy()
    for c in out.select_dtypes(include=["object","string"]).columns:
        s=out[c]
        if len(s) and s.notna().mean()>.8:
            parsed=pd.to_datetime(s, errors="coerce")
            if parsed.notna().mean()>.9: out[c]=parsed
    return out

def altair_catalog():
    from altair.datasets import data
    return list(data.list_datasets())

def load_altair(name: str) -> pd.DataFrame:
    from altair.datasets import data
    value=getattr(data,name)()
    if not isinstance(value,pd.DataFrame):
        raise TypeError(f"{name} is not a tabular pandas dataset")
    return coerce_dates(value)

def load_upload(upload) -> pd.DataFrame:
    name=upload.name.lower(); raw=upload.getvalue()
    if name.endswith(".csv"): return coerce_dates(pd.read_csv(io.BytesIO(raw)))
    if name.endswith((".xlsx",".xls")): return coerce_dates(pd.read_excel(io.BytesIO(raw)))
    if name.endswith(".parquet"): return coerce_dates(pd.read_parquet(io.BytesIO(raw)))
    if name.endswith(".json"): return coerce_dates(pd.read_json(io.BytesIO(raw)))
    raise ValueError("Supported: CSV, XLSX/XLS, Parquet, JSON")
