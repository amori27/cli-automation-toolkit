import sys
import pandas as pd
from typing import Optional


def read_csv(path: str) -> pd.DataFrame:
    if path == '-':
        return pd.read_csv(sys.stdin)
    return pd.read_csv(path)


def write_csv(df: pd.DataFrame, path: str) -> None:
    if path == '-':
        df.to_csv(sys.stdout, index=False)
    else:
        df.to_csv(path, index=False)


def deduplicate(file: str, output: str) -> str:
    df = read_csv(file)
    df = df.drop_duplicates()
    write_csv(df, output)
    return output


def fillna(file: str, strategy: str, column: Optional[str], output: str) -> str:
    df = read_csv(file)

    if column:
        cols = [column]
    else:
        cols = df.select_dtypes(include='number').columns.tolist()

    for col in cols:
        if strategy == 'mean':
            df[col] = df[col].fillna(df[col].mean())
        elif strategy == 'median':
            df[col] = df[col].fillna(df[col].median())
        elif strategy == 'mode':
            mode_vals = df[col].mode()
            if not mode_vals.empty:
                df[col] = df[col].fillna(mode_vals[0])

    write_csv(df, output)
    return output


def filter_rows(file: str, column: str, value: str, output: str) -> str:
    df = read_csv(file)
    df = df[df[column].astype(str) == value]
    write_csv(df, output)
    return output
