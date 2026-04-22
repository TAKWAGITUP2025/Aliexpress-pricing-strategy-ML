"""
Smoke tests — verify core dependencies and basic module imports work correctly.
These run on every CI trigger before any deployment.
"""

import importlib
import pytest


REQUIRED_PACKAGES = [
    "pandas",
    "numpy",
    "sklearn",
    "xgboost",
    "streamlit",
    "plotly",
    "joblib",
    "scipy",
    "matplotlib",
    "seaborn",
]


@pytest.mark.parametrize("package", REQUIRED_PACKAGES)
def test_package_importable(package):
    """All required packages must be importable."""
    mod = importlib.import_module(package)
    assert mod is not None


def test_pandas_version():
    import pandas as pd
    major = int(pd.__version__.split(".")[0])
    assert major >= 1, f"pandas >= 1.x required, got {pd.__version__}"


def test_numpy_version():
    import numpy as np
    major = int(np.__version__.split(".")[0])
    assert major >= 1, f"numpy >= 1.x required, got {np.__version__}"


def test_sklearn_version():
    import sklearn
    parts = sklearn.__version__.split(".")
    assert (int(parts[0]), int(parts[1])) >= (1, 3), (
        f"scikit-learn >= 1.3 required, got {sklearn.__version__}"
    )


def test_requirements_file_exists():
    """requirements.txt must be present at the repo root."""
    from pathlib import Path
    repo_root = Path(__file__).resolve().parents[1]
    req_file = repo_root / "requirements.txt"
    assert req_file.exists(), "requirements.txt not found in repo root"


def test_app_file_exists():
    """Entry-point app.py must exist."""
    from pathlib import Path
    repo_root = Path(__file__).resolve().parents[1]
    app_file = repo_root / "notebooks" / "app.py"
    assert app_file.exists(), "notebooks/app.py not found"
