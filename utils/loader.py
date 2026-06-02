"""
Utilities for loading the Inner Speech Dataset v2.

Expected layout on disk:
    <base>/
        raw/
            russian/  spanish/
                subN/
                    subN_session.edf
        preprocessed/
            russian/  spanish/
                subN/
                    subN_epochs.fif
                    subN.xlsx

Set the base path once before using any loader function:

    import utils
    utils.DEFAULT_BASE = Path('/your/dataset/root')
"""

from __future__ import annotations

from pathlib import Path
import mne
import pandas as pd

DEFAULT_BASE: Path | None = None

LANGUAGES = ('Russian', 'Spanish')

_BASE_ERROR = (
    "Dataset base path is not set. "
    "Assign it before calling any loader:\n\n"
    "    import utils\n"
    "    utils.DEFAULT_BASE = Path('/path/to/dataset')\n\n"
    "or pass base= explicitly to each function."
)


def _resolve_base(base):
    if base is None:
        import utils
        base = utils.DEFAULT_BASE
    if base is None:
        raise ValueError(_BASE_ERROR)
    return Path(base)


# ── EDF ──────────────────────────────────────────────────────────────────────

def load_raw(
    subject: str,
    language: str,
    base: Path = None,
    preload: bool = False,
) -> mne.io.BaseRaw:
    """Load a raw EDF file for one subject.

    Parameters
    ----------
    subject  : e.g. 'sub1'
    language : 'Russian' or 'Spanish'
    preload  : whether to read signal data into memory
    """
    base = _resolve_base(base)
    path = base / 'raw' / language.lower() / subject / f'{subject}_session.edf'
    return mne.io.read_raw_edf(str(path), preload=preload, verbose=False)


def load_all_raw(
    language: str,
    base: Path = None,
    preload: bool = False,
) -> dict[str, mne.io.BaseRaw]:
    """Load raw EDF for all subjects of a language.  Returns {subject: raw}."""
    base = _resolve_base(base)
    result = {}
    for edf in sorted((base / 'raw' / language.lower()).rglob('*_session.edf')):
        subject = edf.parent.name
        result[subject] = mne.io.read_raw_edf(str(edf), preload=preload, verbose=False)
    return result


# ── Epochs (FIF) ──────────────────────────────────────────────────────────────

def load_epochs(
    subject: str,
    language: str,
    base: Path = None,
    preload: bool = False,
) -> mne.Epochs:
    """Load the cleaned epochs FIF file for one subject."""
    base = _resolve_base(base)
    path = base / 'preprocessed' / language.lower() / subject / f'{subject}_epochs.fif'
    return mne.read_epochs(str(path), preload=preload, verbose=False)


def load_all_epochs(
    language: str,
    base: Path = None,
    preload: bool = False,
) -> dict[str, mne.Epochs]:
    """Load epochs for all subjects of a language.  Returns {subject: epochs}."""
    base = _resolve_base(base)
    result = {}
    for fif in sorted((base / 'preprocessed' / language.lower()).rglob('*_epochs.fif')):
        subject = fif.parent.name
        result[subject] = mne.read_epochs(str(fif), preload=preload, verbose=False)
    return result


def load_all_languages(
    base: Path = None,
    preload: bool = False,
) -> dict[str, dict[str, mne.Epochs]]:
    """Load epochs for all languages and subjects.

    Returns
    -------
    {language: {subject: epochs}}
    """
    base = _resolve_base(base)
    return {
        lang: load_all_epochs(lang, base=base, preload=preload)
        for lang in LANGUAGES
    }


# ── Labels (XLSX) ─────────────────────────────────────────────────────────────

def load_labels(
    subject: str,
    language: str,
    base: Path = None,
) -> pd.DataFrame:
    """Load the trial labels spreadsheet for one subject."""
    base = _resolve_base(base)
    path = base / 'preprocessed' / language.lower() / subject / f'{subject}.xlsx'
    return pd.read_excel(str(path))


def load_all_labels(
    language: str,
    base: Path = None,
) -> dict[str, pd.DataFrame]:
    """Load label spreadsheets for all subjects of a language.  Returns {subject: df}."""
    base = _resolve_base(base)
    result = {}
    for xlsx in sorted((base / 'preprocessed' / language.lower()).rglob('*.xlsx')):
        subject = xlsx.parent.name
        result[subject] = pd.read_excel(str(xlsx))
    return result
