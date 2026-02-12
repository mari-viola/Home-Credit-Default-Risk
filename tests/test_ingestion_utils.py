"""Testes de funções utilitárias da ingestão (escrita atômica, etc.)."""
import importlib
import tempfile
from pathlib import Path

import pandas as pd


def test_save_atomic_parquet_writes_valid_file():
    """save_atomic_parquet grava um Parquet válido e substitui atômico."""
    mod = importlib.import_module("src.01_ingestion")
    save_atomic = mod.save_atomic_parquet

    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "out.parquet"
        save_atomic(df, str(out))
        assert out.exists()
        back = pd.read_parquet(out)
        pd.testing.assert_frame_equal(back, df)
