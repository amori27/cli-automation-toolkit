import sys
import pandas as pd
from pathlib import Path
from typing import List, Optional


def merge_csvs(files: List[str], output: str) -> str:
    dfs = [pd.read_csv(f) for f in files]
    merged = pd.concat(dfs, ignore_index=True)
    merged.to_csv(output, index=False)
    return output


def convert_file(input_path: str, fmt: str, output: Optional[str] = None) -> str:
    if output is None and input_path != '-':
        p = Path(input_path)
        new_suffix = '.json' if fmt == 'json' else '.csv'
        output = str(p.with_suffix(new_suffix))

    if fmt == 'json':
        if input_path == '-':
            df = pd.read_csv(sys.stdin)
        else:
            df = pd.read_csv(input_path)
        json_str = df.to_json(orient='records', indent=2)
        if output:
            Path(output).write_text(json_str)
            return output
        sys.stdout.write(json_str)
        return 'stdout'

    if input_path == '-':
        df = pd.read_json(sys.stdin)
    else:
        df = pd.read_json(input_path)
    if output:
        df.to_csv(output, index=False)
        return output
    df.to_csv(sys.stdout, index=False)
    return 'stdout'
