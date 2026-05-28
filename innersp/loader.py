"""
Utilities for loading the Inner Speech Dataset (EDF and FIF formats).

Dataset layout expected on disk:
    <base>/
        Russian/
            sub1/  sub2/  ...  sub12/
                <id>.edf
                <id>_edited.edf
                <id>-epo.fif
                <id>-clean-epo.fif
        Spanish/
            sub0/  sub1/  ...  sub9/
                (same structure)
"""

from pathlib import Path
import mne

DEFAULT_BASE = Path(r'D:\Inner Speech Dataset\Inner Speech Dataset')

LANGUAGES = ('Russian', 'Spanish')


# ── EDF ──────────────────────────────────────────────────────────────────────

def load_raw(
    subject: str,
    language: str,
    base: Path = DEFAULT_BASE,
    edited: bool = True,
    preload: bool = False,
) -> mne.io.BaseRaw:
    """Load a raw EDF file for one subject.

    Parameters
    ----------
    subject  : e.g. 'sub1'
    language : 'Russian' or 'Spanish'
    edited   : if True load *_edited.edf, otherwise the original *.edf
    preload  : whether to read signal data into memory
    """
    suffix = '_edited' if edited else ''
    path = base / language / subject / f'{subject}{suffix}.edf'
    return mne.io.read_raw_edf(str(path), preload=preload, verbose=False)


def load_all_raw(
    language: str,
    base: Path = DEFAULT_BASE,
    edited: bool = True,
    preload: bool = False,
) -> dict[str, mne.io.BaseRaw]:
    """Load raw EDF for all subjects of a language.  Returns {subject: raw}."""
    pattern = '*_edited.edf' if edited else '*.edf'
    result = {}
    for edf in sorted((base / language).rglob(pattern)):
        subject = edf.parent.name
        result[subject] = mne.io.read_raw_edf(str(edf), preload=preload, verbose=False)
    return result


# ── Epochs (FIF) ──────────────────────────────────────────────────────────────

def load_epochs(
    subject: str,
    language: str,
    base: Path = DEFAULT_BASE,
    clean: bool = True,
    preload: bool = False,
) -> mne.Epochs:
    """Load an epochs FIF file for one subject.

    Parameters
    ----------
    clean : if True load *-clean-epo.fif, otherwise *-epo.fif
    """
    suffix = '-clean-epo' if clean else '-epo'
    path = base / language / subject / f'{subject}{suffix}.fif'
    return mne.read_epochs(str(path), preload=preload, verbose=False)


def load_all_epochs(
    language: str,
    base: Path = DEFAULT_BASE,
    clean: bool = True,
    preload: bool = False,
) -> dict[str, mne.Epochs]:
    """Load epochs for all subjects of a language.  Returns {subject: epochs}."""
    pattern = '*-clean-epo.fif' if clean else '*-epo.fif'
    result = {}
    for fif in sorted((base / language).rglob(pattern)):
        subject = fif.parent.name
        result[subject] = mne.read_epochs(str(fif), preload=preload, verbose=False)
    return result


def load_all_languages(
    base: Path = DEFAULT_BASE,
    clean: bool = True,
    preload: bool = False,
) -> dict[str, dict[str, mne.Epochs]]:
    """Load epochs for all languages and subjects.

    Returns
    -------
    {language: {subject: epochs}}
    """
    return {
        lang: load_all_epochs(lang, base=base, clean=clean, preload=preload)
        for lang in LANGUAGES
    }
