"""Testes do módulo de configuração."""
import pytest


def test_config_module_import():
    """Config pode ser importado e expõe paths e get_ingestion_paths."""
    from src import config

    assert hasattr(config, "RAW_PATH")
    assert hasattr(config, "BRONZE_PATH")
    assert hasattr(config, "SILVER_PATH")
    assert hasattr(config, "GOLD_PATH")
    assert hasattr(config, "get_ingestion_paths")
    assert config.SILVER_PATH == "data/silver"
    assert config.GOLD_PATH == "data/gold"


def test_get_ingestion_paths_raises_when_raw_or_bronze_missing():
    """get_ingestion_paths levanta ValueError se RAW_PATH ou BRONZE_PATH forem vazios."""
    from src import config

    original_raw, original_bronze = config.RAW_PATH, config.BRONZE_PATH
    try:
        config.RAW_PATH = None
        config.BRONZE_PATH = "data/bronze"
        with pytest.raises(ValueError, match="Variáveis de ambiente não configuradas"):
            config.get_ingestion_paths()

        config.RAW_PATH = "data/raw"
        config.BRONZE_PATH = None
        with pytest.raises(ValueError, match="Variáveis de ambiente não configuradas"):
            config.get_ingestion_paths()
    finally:
        config.RAW_PATH = original_raw
        config.BRONZE_PATH = original_bronze


def test_get_ingestion_paths_returns_tuple_when_configured():
    """get_ingestion_paths retorna (raw_path, bronze_path) quando ambos estão definidos."""
    from src import config

    original_raw, original_bronze = config.RAW_PATH, config.BRONZE_PATH
    try:
        config.RAW_PATH = "data/raw"
        config.BRONZE_PATH = "data/bronze"
        raw, bronze = config.get_ingestion_paths()
        assert raw == "data/raw"
        assert bronze == "data/bronze"
    finally:
        config.RAW_PATH = original_raw
        config.BRONZE_PATH = original_bronze
