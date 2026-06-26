import json
import sys
import pandas as pd


def generate_stats(file: str, output: str) -> str:
    if file == '-':
        df = pd.read_csv(sys.stdin)
    else:
        df = pd.read_csv(file)

    column_stats = {}
    for col in df.columns:
        col_data = df[col]
        stats: dict = {
            'dtype': str(col_data.dtype),
            'count': int(col_data.count()),
            'nulls': int(col_data.isna().sum()),
            'null_pct': round(float(col_data.isna().mean() * 100), 2),
            'unique': int(col_data.nunique()),
        }
        if pd.api.types.is_numeric_dtype(col_data):
            stats.update({
                'mean': round(float(col_data.mean()), 2),
                'std': round(float(col_data.std()), 2),
                'min': float(col_data.min()),
                '25%': float(col_data.quantile(0.25)),
                '50%': float(col_data.quantile(0.5)),
                '75%': float(col_data.quantile(0.75)),
                'max': float(col_data.max()),
            })
        stats['samples'] = col_data.dropna().head(5).tolist()
        column_stats[col] = stats

    result = {
        'rows': len(df),
        'columns': len(df.columns),
        'memory_usage': f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB",
        'column_stats': column_stats,
    }

    with open(output, 'w') as f:
        json.dump(result, f, indent=2)
    return output
